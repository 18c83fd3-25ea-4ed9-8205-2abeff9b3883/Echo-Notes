# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] 2025-05-07

### Added
- New `ai_weekly_summary.py` script for automated weekly reports
- Weekly summary generation with cron scheduling support
- Date-based note collection system with timestamp fallback
- Integrated weekly summary documentation in README.md
- Error logging for summary generation process

### Changed
- Updated README with dual cron job examples (hourly + weekly)
- Restructured "How It Works" section to include weekly summaries
- Improved prompt engineering for consistent heading formats
- File handling to prefer embedded timestamps over filesystem dates

### Fixed
- Removed duplicate headings in weekly summary output
- Resolved f-string syntax error in prompt generation
- Improved error handling for note date parsing
- Fixed markdown formatting in documentation examples

## [0.1.0] - 2025-05-06

### Added
- Initial release of core note processing system
- Basic voice-to-text cleanup functionality
- Hourly cron job integration
- LM Studio local endpoint support
- Structured note template with tasks/suggestions

### Changed
- Initial project documentation
- Privacy-first design principles established

### Fixed
- Initial bug fixes for Nextcloud file syncing
