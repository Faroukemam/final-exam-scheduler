# Changelog

All notable changes to Final Exam Scheduler will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2025-12-28

### Added
- **Layered Architecture**: Complete refactoring into 5-layer architecture
  - Models layer for data structures
  - Utils layer for shared utilities
  - Data layer for file I/O and templates
  - Business layer for optimization logic
  - Presentation layer for GUI components
- **Template Generation**: Auto-generate Excel templates with README documentation
- **Professional Branding**: Custom gradient logo (indigo/cyan)
- **About Dialog**: Professional copyright and contact information
- **Assets Organization**: Dedicated `assets/` folder for static files
- **Comprehensive Documentation**: README.md, LICENSE, .gitignore

### Changed
- Reorganized all code into proper layer modules
- Updated imports to use layered structure
- Moved logo files to `assets/` folder
- Enhanced GUI with tooltips and section headers
- Improved window sizing and layout

### Technical
- Extracted ModernButton widget to presentation layer
- Extracted AppBase widget to presentation layer
- Created package structure with __init__.py files  
- Added proper Python packaging structure
- Updated PyInstaller build configuration

## [1.0.0] - Initial Release

### Added
- Exam scheduling with CP-SAT optimization
- Invigilation scheduling
- Diagnostics and validation
- Courses report generation
- Excel file I/O
- Tkinter GUI
- Windows EXE build
