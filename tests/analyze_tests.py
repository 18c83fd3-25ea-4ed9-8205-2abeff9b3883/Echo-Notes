#!/usr/bin/env python3
"""
Echo-Notes Test Analysis Script

This script analyzes the test files in the Echo-Notes project to:
1. Identify which tests are essential for ensuring core functionality
2. Determine which tests are redundant or only used for development
3. Create a plan to consolidate or remove unnecessary test files

Usage:
    python analyze_tests.py [--output OUTPUT_FILE] [--dry-run]

Options:
    --output OUTPUT_FILE    Write the results to the specified file (default: test_analysis.md)
    --dry-run               Show what would be done without making changes
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
import re
import ast


class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_color(color, message):
    """Print colored message if supported"""
    if sys.platform != "win32" or os.environ.get("TERM") == "xterm":
        print(f"{color}{message}{Colors.NC}")
    else:
        print(message)


def get_project_root():
    """Get the project root directory"""
    return os.path.dirname(os.path.abspath(__file__))


def find_test_files(project_root):
    """Find all test files in the project"""
    test_files = []
    
    # Walk through the project directory
    for root, dirs, files in os.walk(project_root):
        # Skip virtual environment directories
        if 'venv' in root or 'echo_notes_venv' in root or 'test_venv' in root:
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_root)
            
            # Check if it's a test file
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(rel_path)
            elif 'test' in file.lower() and file.endswith('.py'):
                test_files.append(rel_path)
            elif 'test' in file.lower() and file.endswith('.sh'):
                test_files.append(rel_path)
            elif os.path.basename(root) == 'tests' and file.endswith('.py'):
                test_files.append(rel_path)
    
    return sorted(test_files)


def read_file_content(file_path):
    """Read the content of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print_color(Colors.RED, f"Error reading file {file_path}: {e}")
        return ""


def analyze_python_test(file_path, content):
    """Analyze a Python test file"""
    test_info = {
        'path': file_path,
        'test_functions': [],
        'imports': [],
        'tested_modules': [],
        'is_pytest': False,
        'is_unittest': False,
        'complexity': 0,
    }
    
    # Check if it's a pytest or unittest file
    if 'import pytest' in content or 'from pytest' in content:
        test_info['is_pytest'] = True
    if 'import unittest' in content or 'from unittest' in content:
        test_info['is_unittest'] = True
    
    # Try to parse the Python file
    try:
        tree = ast.parse(content)
        
        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    test_info['imports'].append(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for name in node.names:
                        test_info['imports'].append(f"{node.module}.{name.name}")
            
            # Extract test functions
            if isinstance(node, ast.FunctionDef) and (node.name.startswith('test_') or 'test' in node.name.lower()):
                test_info['test_functions'].append(node.name)
        
        # Estimate complexity by counting nodes
        test_info['complexity'] = sum(1 for _ in ast.walk(tree))
        
    except SyntaxError:
        print_color(Colors.YELLOW, f"Could not parse {file_path} as Python")
    
    # Try to determine which modules are being tested
    for imp in test_info['imports']:
        if 'echo_notes' in imp:
            module = imp.split('.')[-1]
            test_info['tested_modules'].append(module)
    
    return test_info


def analyze_shell_test(file_path, content):
    """Analyze a shell test script"""
    test_info = {
        'path': file_path,
        'commands': [],
        'tested_components': [],
        'complexity': len(content.split('\n')),
    }
    
    # Extract commands
    command_pattern = re.compile(r'^[^#]*\b(python|\.\/|bash|sh|echo_notes|process-notes|generate-summary)\b.*$', re.MULTILINE)
    for match in command_pattern.finditer(content):
        command = match.group(0).strip()
        if command:
            test_info['commands'].append(command)
    
    # Try to determine which components are being tested
    component_patterns = [
        (r'install', 'installation'),
        (r'uninstall', 'uninstallation'),
        (r'daemon', 'daemon'),
        (r'dashboard', 'dashboard'),
        (r'process-notes', 'note processing'),
        (r'generate-summary', 'summary generation'),
    ]
    
    for pattern, component in component_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            test_info['tested_components'].append(component)
    
    return test_info


def analyze_test_file(file_path, project_root):
    """Analyze a test file"""
    full_path = os.path.join(project_root, file_path)
    content = read_file_content(full_path)
    
    if file_path.endswith('.py'):
        return analyze_python_test(file_path, content)
    elif file_path.endswith('.sh'):
        return analyze_shell_test(file_path, content)
    else:
        return {
            'path': file_path,
            'content': content,
            'complexity': len(content.split('\n')),
        }


def find_duplicate_tests(test_files_info):
    """Find duplicate test files"""
    duplicates = []
    
    # Group by filename
    by_filename = {}
    for info in test_files_info:
        filename = os.path.basename(info['path'])
        if filename not in by_filename:
            by_filename[filename] = []
        by_filename[filename].append(info)
    
    # Check for duplicates
    for filename, infos in by_filename.items():
        if len(infos) > 1:
            duplicates.append({
                'filename': filename,
                'instances': [info['path'] for info in infos],
            })
    
    return duplicates


def categorize_tests(test_files_info):
    """Categorize tests as essential, development-only, or redundant"""
    essential_tests = []
    dev_tests = []
    redundant_tests = []
    
    # First, identify redundant tests (duplicates)
    duplicates = find_duplicate_tests(test_files_info)
    duplicate_paths = set()
    for dup in duplicates:
        # Keep the one in the tests directory if it exists
        instances = dup['instances']
        tests_dir_instance = next((p for p in instances if p.startswith('tests/')), None)
        
        if tests_dir_instance:
            # Keep the one in the tests directory
            for path in instances:
                if path != tests_dir_instance:
                    duplicate_paths.add(path)
        else:
            # Keep the first one, mark others as duplicates
            for path in instances[1:]:
                duplicate_paths.add(path)
    
    # Categorize each test
    for info in test_files_info:
        path = info['path']
        
        # Check if it's a duplicate
        if path in duplicate_paths:
            redundant_tests.append(info)
            continue
        
        # Check if it's a development-only test
        if 'installer' in path.lower() or 'uninstall' in path.lower():
            dev_tests.append(info)
            continue
        
        if path.startswith('Echo-Notes/test_'):
            dev_tests.append(info)
            continue
        
        # Otherwise, consider it essential
        essential_tests.append(info)
    
    return {
        'essential': essential_tests,
        'development': dev_tests,
        'redundant': redundant_tests,
    }


def generate_test_analysis_report(test_categories, output_file=None):
    """Generate a report of the test analysis"""
    report = []
    
    report.append("# Echo-Notes Test Analysis Report\n")
    report.append("This report analyzes the test files in the Echo-Notes project and categorizes them as essential, development-only, or redundant.\n")
    
    # Essential tests
    report.append("## Essential Tests\n")
    report.append("These tests are essential for ensuring core functionality:\n")
    for test in test_categories['essential']:
        path = test['path']
        if 'test_functions' in test:
            functions = len(test['test_functions'])
            report.append(f"- `{path}` ({functions} test functions)")
        else:
            report.append(f"- `{path}`")
    report.append("\n")
    
    # Development-only tests
    report.append("## Development-Only Tests\n")
    report.append("These tests are only used during development and could be moved to a separate directory:\n")
    for test in test_categories['development']:
        path = test['path']
        report.append(f"- `{path}`")
    report.append("\n")
    
    # Redundant tests
    report.append("## Redundant Tests\n")
    report.append("These tests are redundant and could be removed or consolidated:\n")
    for test in test_categories['redundant']:
        path = test['path']
        report.append(f"- `{path}`")
    report.append("\n")
    
    # Consolidation plan
    report.append("## Test Consolidation Plan\n")
    report.append("### 1. Move Essential Tests to tests/ Directory\n")
    for test in test_categories['essential']:
        path = test['path']
        if not path.startswith('tests/'):
            new_path = f"tests/{os.path.basename(path)}"
            report.append(f"- Move `{path}` to `{new_path}`")
    report.append("\n")
    
    report.append("### 2. Move Development-Only Tests to tools/dev_tests/ Directory\n")
    for test in test_categories['development']:
        path = test['path']
        new_path = f"tools/dev_tests/{os.path.basename(path)}"
        report.append(f"- Move `{path}` to `{new_path}`")
    report.append("\n")
    
    report.append("### 3. Remove or Archive Redundant Tests\n")
    for test in test_categories['redundant']:
        path = test['path']
        report.append(f"- Remove `{path}`")
    report.append("\n")
    
    # Summary
    report.append("## Summary\n")
    report.append(f"- Essential Tests: {len(test_categories['essential'])}\n")
    report.append(f"- Development-Only Tests: {len(test_categories['development'])}\n")
    report.append(f"- Redundant Tests: {len(test_categories['redundant'])}\n")
    report.append(f"- Total Tests: {sum(len(tests) for tests in test_categories.values())}\n")
    
    report_text = "\n".join(report)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print_color(Colors.GREEN, f"Report written to {output_file}")
    else:
        print(report_text)
    
    return report_text


def consolidate_tests(test_categories, project_root, dry_run=False):
    """Consolidate test files according to the plan"""
    print_color(Colors.BLUE, "Consolidating test files...")
    
    # Create directories if they don't exist
    tests_dir = os.path.join(project_root, "tests")
    dev_tests_dir = os.path.join(project_root, "tools", "dev_tests")
    
    if not dry_run:
        os.makedirs(tests_dir, exist_ok=True)
        os.makedirs(dev_tests_dir, exist_ok=True)
    
    # Move essential tests to tests/ directory
    for test in test_categories['essential']:
        path = test['path']
        if not path.startswith('tests/'):
            src_path = os.path.join(project_root, path)
            dst_path = os.path.join(tests_dir, os.path.basename(path))
            
            if not dry_run:
                if os.path.exists(src_path):
                    if not os.path.exists(dst_path):
                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                        shutil.copy2(src_path, dst_path)
                        print_color(Colors.GREEN, f"Copied {src_path} to {dst_path}")
                    else:
                        print_color(Colors.YELLOW, f"Destination already exists: {dst_path}")
                else:
                    print_color(Colors.YELLOW, f"Source file not found: {src_path}")
            else:
                print_color(Colors.YELLOW, f"Would copy {src_path} to {dst_path}")
    
    # Move development-only tests to tools/dev_tests/ directory
    for test in test_categories['development']:
        path = test['path']
        src_path = os.path.join(project_root, path)
        dst_path = os.path.join(dev_tests_dir, os.path.basename(path))
        
        if not dry_run:
            if os.path.exists(src_path):
                if not os.path.exists(dst_path):
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    print_color(Colors.GREEN, f"Copied {src_path} to {dst_path}")
                else:
                    print_color(Colors.YELLOW, f"Destination already exists: {dst_path}")
            else:
                print_color(Colors.YELLOW, f"Source file not found: {src_path}")
        else:
            print_color(Colors.YELLOW, f"Would copy {src_path} to {dst_path}")
    
    print_color(Colors.GREEN, "Test consolidation completed successfully!")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Echo-Notes Test Analysis Script")
    parser.add_argument("--output", help="Output file for the report", default="test_analysis.md")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--consolidate", action="store_true", help="Consolidate test files according to the plan")
    args = parser.parse_args()
    
    project_root = get_project_root()
    print_color(Colors.BLUE, f"Analyzing tests in: {project_root}")
    
    # Find all test files
    test_files = find_test_files(project_root)
    print_color(Colors.BLUE, f"Found {len(test_files)} test files")
    
    # Analyze each test file
    test_files_info = []
    for test_file in test_files:
        info = analyze_test_file(test_file, project_root)
        test_files_info.append(info)
    
    # Categorize tests
    test_categories = categorize_tests(test_files_info)
    
    # Generate report
    generate_test_analysis_report(test_categories, args.output)
    
    # Consolidate tests if requested
    if args.consolidate:
        if args.dry_run:
            print_color(Colors.YELLOW, "DRY RUN MODE: No changes will be made")
        consolidate_tests(test_categories, project_root, args.dry_run)
    
    print_color(Colors.GREEN, "Analysis completed successfully!")


if __name__ == "__main__":
    main()