# Architecture Overview

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Layer                           │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │   CLI Interface      │    │   GUI Interface      │      │
│  │   (Click-based)      │    │   (Tkinter-based)    │      │
│  └──────────────────────┘    └──────────────────────┘      │
└───────────────────┬───────────────────┬─────────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    Core Layer                             │
│  ┌──────────────────────────────────────────────────┐    │
│  │         Script Executor                          │    │
│  │  • YAML Parser                                   │    │
│  │  • Step Orchestrator                             │    │
│  │  • Result Aggregator                             │    │
│  └──────────────────────────────────────────────────┘    │
│                         │                                 │
│  ┌──────────────────────▼──────────────────────────┐    │
│  │    WinAppDriver Controller                      │    │
│  │  • Session Manager                               │    │
│  │  • Element Finder                                │    │
│  │  • Action Executor                               │    │
│  │  • Validator                                     │    │
│  └──────────────────────────────────────────────────┘    │
└───────────────────────────┬───────────────────────────────┘
                            │
                    (HTTP/JSON)
                            │
┌───────────────────────────▼───────────────────────────────┐
│              WinAppDriver Service                         │
│  • Windows Application Driver                             │
│  • UI Automation API                                      │
│  • WebDriver Protocol                                     │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│              Target Application                           │
│  • Calculator, Notepad, Custom Apps                       │
│  • UWP, WinForms, WPF, Win32                             │
└───────────────────────────────────────────────────────────┘
```

## Component Diagram

### Core Components

```
┌─────────────────────────────────────────────┐
│        WinAppDriverController               │
├─────────────────────────────────────────────┤
│ Properties:                                 │
│  - server_url: str                          │
│  - implicit_wait: int                       │
│  - driver: WebDriver                        │
├─────────────────────────────────────────────┤
│ Methods:                                    │
│  + start_app(app_path, args)                │
│  + stop_app()                               │
│  + find_element(by, value, timeout)         │
│  + click(element)                           │
│  + double_click(element)                    │
│  + send_keys(element, keys)                 │
│  + clear(element)                           │
│  + get_text(element)                        │
│  + get_attribute(element, attr)             │
│  + screenshot(filename)                     │
│  + wait(duration)                           │
│  + verify_element_text(element, expected)   │
│  + is_element_displayed(element)            │
│  + is_element_enabled(element)              │
│  + get_window_title()                       │
└─────────────────────────────────────────────┘
                    △
                    │ uses
                    │
┌─────────────────────────────────────────────┐
│           ScriptExecutor                    │
├─────────────────────────────────────────────┤
│ Properties:                                 │
│  - controller: WinAppDriverController       │
│  - config: dict                             │
│  - results: list                            │
├─────────────────────────────────────────────┤
│ Methods:                                    │
│  + load_script(path)                        │
│  + execute_script(script)                   │
│  + execute_script_file(path)                │
│  + get_results()                            │
│  - _execute_step(step, num)                 │
│  - _find_element(config)                    │
│  - _action_click(step)                      │
│  - _action_double_click(step)               │
│  - _action_send_keys(step)                  │
│  - _action_clear(step)                      │
│  - _action_wait(step)                       │
│  - _action_verify(step)                     │
│  - _action_screenshot(step)                 │
└─────────────────────────────────────────────┘
```

## Data Flow

### Script Execution Flow

```
1. User Input
   │
   ├─> CLI: Command line arguments
   │   └─> Click argument parser
   │
   └─> GUI: Button clicks & file selection
       └─> Tkinter event handlers

2. Script Loading
   │
   └─> Load YAML file
       └─> Parse YAML structure
           └─> Validate script format

3. Initialization
   │
   ├─> Create WinAppDriverController
   │   └─> Connect to WinAppDriver service (HTTP)
   │
   └─> Create ScriptExecutor
       └─> Load configuration

4. Application Start
   │
   └─> Send start command to WinAppDriver
       └─> WinAppDriver launches target app
           └─> Return session ID

5. Step Execution Loop
   │
   └─> For each step in script:
       │
       ├─> Find element (if needed)
       │   └─> Send element query to WinAppDriver
       │       └─> WinAppDriver queries UI Automation API
       │           └─> Return element reference
       │
       ├─> Execute action
       │   └─> Send action command to WinAppDriver
       │       └─> WinAppDriver performs action
       │           └─> Return result
       │
       └─> Record result
           ├─> Success: Continue to next step
           └─> Failure: Stop or continue based on config

6. Cleanup
   │
   └─> Stop application
       └─> Close WinAppDriver session
           └─> Aggregate results

7. Output
   │
   ├─> CLI: Print results to console
   │   └─> Optional: Export to JSON
   │
   └─> GUI: Display in Results tab
       └─> Optional: Export to file
```

## Communication Protocol

### WinAppDriver Communication

```
┌──────────────┐                           ┌──────────────┐
│              │  HTTP POST /session        │              │
│              │  (desired capabilities)    │              │
│  Controller  ├───────────────────────────>│ WinAppDriver │
│              │                            │              │
│              │<───────────────────────────┤              │
│              │  200 OK (session_id)       │              │
└──────────────┘                           └──────────────┘

┌──────────────┐                           ┌──────────────┐
│              │  POST /session/:id/element │              │
│              │  (locator strategy)        │              │
│  Controller  ├───────────────────────────>│ WinAppDriver │
│              │                            │              │
│              │<───────────────────────────┤              │
│              │  200 OK (element ref)      │              │
└──────────────┘                           └──────────────┘

┌──────────────┐                           ┌──────────────┐
│              │  POST /session/:id/        │              │
│              │  element/:id/click         │              │
│  Controller  ├───────────────────────────>│ WinAppDriver │
│              │                            │              │
│              │<───────────────────────────┤              │
│              │  200 OK                    │              │
└──────────────┘                           └──────────────┘
```

## File Structure

```
Winapp-driver-collector/
│
├── src/                        # Source code
│   ├── core/                   # Core automation engine
│   │   ├── __init__.py
│   │   ├── controller.py       # WinAppDriver controller
│   │   └── executor.py         # Script executor
│   │
│   ├── cli/                    # CLI interface
│   │   ├── __init__.py
│   │   └── main.py             # CLI entry point
│   │
│   └── gui/                    # GUI interface
│       ├── __init__.py
│       └── main.py             # GUI entry point
│
├── config/                     # Configuration files
│   └── default.yaml            # Default configuration
│
├── examples/                   # Example scripts
│   ├── calculator_test.yaml
│   ├── notepad_test.yaml
│   └── advanced_example.yaml
│
├── docs/                       # Documentation
│   ├── SPECIFICATIONS.md       # Detailed specifications
│   ├── QUICKSTART.md          # Quick start guide
│   ├── API_REFERENCE.md       # API documentation
│   ├── ARCHITECTURE.md        # This file
│   └── CONTRIBUTING.md        # Contributing guide
│
├── logs/                       # Log files (runtime)
├── screenshots/               # Screenshots (runtime)
├── results/                   # Test results (runtime)
│
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── README.md                  # Main documentation
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

## Technology Stack Details

### Core Technologies

```
┌─────────────────────────────────────────┐
│            Python 3.8+                  │
│  • Modern Python features               │
│  • Type hints support                   │
│  • Strong standard library              │
└─────────────────────────────────────────┘
              │
              ├─> Appium-Python-Client
              │   • WebDriver protocol implementation
              │   • Element location strategies
              │   • Session management
              │
              ├─> Selenium
              │   • WebDriver base classes
              │   • Wait conditions
              │   • Exception handling
              │
              ├─> Click
              │   • Command-line interface
              │   • Argument parsing
              │   • Help generation
              │
              ├─> PyYAML
              │   • YAML parsing
              │   • Configuration loading
              │   • Script definition
              │
              └─> Tkinter
                  • GUI framework (standard library)
                  • Cross-platform support
                  • Event-driven programming
```

### External Dependencies

```
┌─────────────────────────────────────────┐
│      WinAppDriver (External)            │
│  • Microsoft's Windows automation tool  │
│  • WebDriver protocol server            │
│  • UI Automation API wrapper            │
└─────────────────────────────────────────┘
              │
              └─> Windows UI Automation
                  • Native Windows API
                  • Element tree inspection
                  • Accessibility support
```

## Extensibility Points

### 1. Custom Actions

Add new actions by extending ScriptExecutor:

```python
class CustomExecutor(ScriptExecutor):
    def _execute_step(self, step, step_number):
        action = step.get('action')
        if action == 'my_custom_action':
            self._action_my_custom(step)
        else:
            super()._execute_step(step, step_number)
    
    def _action_my_custom(self, step):
        # Custom implementation
        pass
```

### 2. Custom Locators

Add new element locator strategies:

```python
class CustomController(WinAppDriverController):
    def find_element(self, by, value, timeout=10):
        if by == "CustomLocator":
            # Custom locator logic
            pass
        else:
            return super().find_element(by, value, timeout)
```

### 3. Custom Reporters

Implement custom result reporting:

```python
class CustomReporter:
    def generate_report(self, results):
        # Generate HTML, PDF, etc.
        pass
```

## Security Considerations

1. **No Credential Storage**: Never store passwords in scripts
2. **Local Execution**: WinAppDriver runs locally by default
3. **File Permissions**: Scripts should not modify system files
4. **Input Validation**: All user inputs are validated
5. **Safe Defaults**: Secure default configurations

## Performance Considerations

1. **Wait Times**: Optimize implicit/explicit waits
2. **Element Caching**: Cache frequently used elements
3. **Screenshot Optimization**: Only capture when needed
4. **Parallel Execution**: Future enhancement for multiple apps
5. **Memory Management**: Clean up resources after each test

## Error Handling Strategy

```
Error Occurrence
     │
     ├─> Log error details
     │
     ├─> Take screenshot (if configured)
     │
     ├─> Check continue_on_error flag
     │   ├─> true: Continue to next step
     │   └─> false: Stop execution
     │
     └─> Return error in results
         └─> Display to user
             ├─> CLI: Console output
             └─> GUI: Message box/log
```

## Future Enhancements

1. **Plugin System**: Load custom actions/reporters dynamically
2. **Remote Execution**: Support for remote WinAppDriver instances
3. **Parallel Testing**: Run multiple tests simultaneously
4. **Visual Element Picker**: GUI tool for element selection
5. **Test Recording**: Record user actions as scripts
6. **Cloud Integration**: Integration with cloud testing platforms
7. **CI/CD Templates**: Pre-built templates for popular CI systems
8. **Performance Profiling**: Built-in performance metrics
9. **Test Data Management**: Support for external test data
10. **Advanced Reporting**: HTML/PDF reports with charts

---

This architecture provides a solid foundation for Windows application automation while remaining extensible for future enhancements.
