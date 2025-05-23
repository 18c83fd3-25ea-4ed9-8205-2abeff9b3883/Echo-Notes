#!/usr/bin/env python3
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from echo_notes.shared.llm_client import query_llm

def main():
    test_prompt = "What is the capital of France?"
    system_message = "You are a helpful assistant that provides accurate information."

    print("Testing Phi-2 integration...")
    try:
        result = query_llm(test_prompt, system_message)
        print("\nResult from LLM:")
        print("-" * 40)
        print(result)
        print("-" * 40)
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    main()