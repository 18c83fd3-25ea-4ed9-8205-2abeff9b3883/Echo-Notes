# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2024-05-07

### Added

-   Added `prompts_config.json` to store customizable prompts for daily note processing and weekly summaries.
-   Extracted hard-coded prompts from scripts into the config file for easier customization.
-   Modified `ai_weekly_summary.py` and `ai_notes_nextcloud.py` to load prompts from the config file.

- Modular architecture with shared components
- Python package installation support
- Console entry points for commands
- Comprehensive setup.py configuration
- Project structure documentation

### Changed
- Restructured codebase for maintainability
- Unified configuration system
- Updated installation instructions
- Improved error logging
- Simplified cron job configuration

### Fixed
- Path handling across different environments
- Version compatibility issues
- Documentation inaccuracies

## [0.2.0] - 2024-05-07

### Added
- Weekly summary generation system
- Dual cron job support
- Timestamp fallback system

## [0.1.0] - 2024-05-06

### Added
- Initial note processing system
- Basic voice-to-text cleanup
- Hourly cron integration