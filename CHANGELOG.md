# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-21

### Added

#### Core Framework
- WinAppDriverController class for automation control
- ScriptExecutor for YAML-based script execution
- Support for multiple element selectors (Name, AutomationId, ClassName, XPath, AccessibilityId)
- Comprehensive error handling and logging
- Screenshot capture functionality
- Element verification and validation

#### Actions Supported
- `click` - Click on elements
- `double_click` - Double-click on elements
- `send_keys` - Send text to elements
- `clear` - Clear input fields
- `wait` - Wait for specified duration
- `verify` - Verify element text
- `screenshot` - Take screenshots

#### CLI Interface
- `run` command - Execute single script
- `batch` command - Execute multiple scripts
- `inspect` command - Inspect application mode
- `version` command - Display version information
- Configurable log levels
- JSON output support
- Configuration file support

#### GUI Interface
- Visual script editor with syntax support
- Real-time execution monitoring
- Results dashboard
- Settings configuration
- Element inspector integration
- Multi-tab interface
  - Execute Script tab
  - Script Editor tab
  - Results tab
  - Settings tab

#### Documentation
- Comprehensive README with bilingual support (English/Korean)
- Detailed specifications document (SPECIFICATIONS.md)
- Quick start guide (QUICKSTART.md)
- Complete API reference (API_REFERENCE.md)
- Contributing guidelines (CONTRIBUTING.md)

#### Examples
- Calculator test script
- Notepad test script
- Default configuration file

#### Development Tools
- requirements.txt with all dependencies
- setup.py for package installation
- .gitignore for clean repository
- Windows batch scripts for easy launching
- MIT License

### Features by Component

#### Core (src/core/)
- WinAppDriver session management
- Element finding with multiple strategies
- Action execution with error handling
- Script parsing and execution
- Result reporting

#### CLI (src/cli/)
- Command-line argument parsing with Click
- Script execution with detailed output
- Batch processing capabilities
- Configuration file support
- Export results to JSON

#### GUI (src/gui/)
- Tkinter-based graphical interface
- Script editor with file operations
- Real-time log display
- Visual execution monitoring
- Settings management

### Technical Details

#### Dependencies
- Python 3.8+
- Appium-Python-Client >=2.9.0
- Selenium >=4.0.0
- Click >=8.0.0
- PyYAML >=6.0
- Tkinter (included with Python)

#### Platform Support
- Windows 10 and later
- Requires WinAppDriver installation
- Developer Mode must be enabled

### Known Limitations
- Windows platform only
- Requires WinAppDriver service running
- Limited support for some legacy Win32 controls
- GUI runs in single thread (blocking during execution)

### Future Plans
- [ ] Add more element locator strategies
- [ ] Implement parallel script execution
- [ ] Add report generation (HTML/PDF)
- [ ] Enhanced GUI with async execution
- [ ] Support for mobile app testing (via Appium)
- [ ] Integration with test frameworks (pytest, unittest)
- [ ] Visual element picker for GUI
- [ ] Recording functionality
- [ ] Test data management
- [ ] CI/CD templates

## [Unreleased]

### Planned Features
- Advanced element selectors
- Custom action definitions
- Plugin system
- Enhanced reporting
- Performance monitoring
- Test data management
- Cloud execution support

---

[1.0.0]: https://github.com/yji0728/Winapp-driver-collector/releases/tag/v1.0.0
