# API Reference

## Core Module

### WinAppDriverController

Main controller class for interacting with WinAppDriver.

#### Constructor

```python
WinAppDriverController(server_url="http://127.0.0.1:4723", implicit_wait=10)
```

**Parameters:**
- `server_url` (str): WinAppDriver server URL
- `implicit_wait` (int): Implicit wait time in seconds

#### Methods

##### start_app(app_path, app_arguments="")

Start the target application.

**Parameters:**
- `app_path` (str): Full path to application executable
- `app_arguments` (str): Optional command line arguments

**Example:**
```python
controller = WinAppDriverController()
controller.start_app("C:\\Windows\\System32\\calc.exe")
```

##### stop_app()

Stop the application and close the session.

**Example:**
```python
controller.stop_app()
```

##### find_element(by, value, timeout=10)

Find an element using specified locator strategy.

**Parameters:**
- `by` (str): Locator strategy ("Name", "AutomationId", "ClassName", "XPath", "AccessibilityId")
- `value` (str): Locator value
- `timeout` (int): Maximum wait time in seconds

**Returns:** WebElement

**Example:**
```python
button = controller.find_element("Name", "Calculate")
```

##### click(element)

Click on an element.

**Parameters:**
- `element`: WebElement to click

**Example:**
```python
element = controller.find_element("Name", "Button")
controller.click(element)
```

##### double_click(element)

Double-click on an element.

**Parameters:**
- `element`: WebElement to double-click

##### send_keys(element, keys)

Send keys to an element.

**Parameters:**
- `element`: WebElement to send keys to
- `keys` (str): Text to send

**Example:**
```python
textbox = controller.find_element("AutomationId", "textBox1")
controller.send_keys(textbox, "Hello World")
```

##### clear(element)

Clear an input element.

**Parameters:**
- `element`: WebElement to clear

##### get_text(element)

Get text from an element.

**Parameters:**
- `element`: WebElement to get text from

**Returns:** str - Element text

**Example:**
```python
result = controller.find_element("AutomationId", "CalculatorResults")
text = controller.get_text(result)
```

##### get_attribute(element, attribute)

Get an attribute value from an element.

**Parameters:**
- `element`: WebElement to get attribute from
- `attribute` (str): Attribute name

**Returns:** str - Attribute value

##### screenshot(filename)

Take a screenshot and save to file.

**Parameters:**
- `filename` (str): Path to save screenshot

**Returns:** bool - True if successful

**Example:**
```python
controller.screenshot("screenshots/result.png")
```

##### wait(duration)

Wait for specified duration.

**Parameters:**
- `duration` (float): Time to wait in seconds

**Example:**
```python
controller.wait(2.5)
```

##### verify_element_text(element, expected_text)

Verify element text matches expected value.

**Parameters:**
- `element`: WebElement to verify
- `expected_text` (str): Expected text value

**Returns:** bool - True if text matches

**Example:**
```python
result = controller.find_element("Name", "Display")
is_correct = controller.verify_element_text(result, "42")
```

##### is_element_displayed(element)

Check if element is displayed.

**Parameters:**
- `element`: WebElement to check

**Returns:** bool - True if element is displayed

##### is_element_enabled(element)

Check if element is enabled.

**Parameters:**
- `element`: WebElement to check

**Returns:** bool - True if element is enabled

##### get_window_title()

Get the current window title.

**Returns:** str - Window title

### ScriptExecutor

Executes automation scripts defined in YAML format.

#### Constructor

```python
ScriptExecutor(controller, config=None)
```

**Parameters:**
- `controller` (WinAppDriverController): Controller instance
- `config` (dict): Optional configuration dictionary

#### Methods

##### load_script(script_path)

Load a script from YAML file.

**Parameters:**
- `script_path` (str): Path to script file

**Returns:** dict - Script dictionary

**Example:**
```python
executor = ScriptExecutor(controller)
script = executor.load_script("examples/calculator_test.yaml")
```

##### execute_script(script)

Execute an automation script.

**Parameters:**
- `script` (dict): Script dictionary

**Returns:** dict - Execution results

**Example:**
```python
result = executor.execute_script(script)
print(f"Status: {result['status']}")
print(f"Duration: {result['duration']}s")
```

##### execute_script_file(script_path)

Load and execute a script file.

**Parameters:**
- `script_path` (str): Path to script file

**Returns:** dict - Execution results

**Example:**
```python
result = executor.execute_script_file("examples/test.yaml")
```

##### get_results()

Get all execution results.

**Returns:** list - List of result dictionaries

## Script Format

### Structure

```yaml
name: "Script Name"
description: "Script description"
app:
  path: "C:\\Path\\To\\App.exe"
  arguments: "optional arguments"

steps:
  - action: "action_name"
    # action-specific parameters
```

### Actions

#### click

Click on an element.

```yaml
- action: "click"
  element:
    type: "Name"  # or AutomationId, ClassName, XPath, AccessibilityId
    value: "ButtonName"
    timeout: 10  # optional, default 10
```

#### double_click

Double-click on an element.

```yaml
- action: "double_click"
  element:
    type: "Name"
    value: "Element"
```

#### send_keys

Send text to an element.

```yaml
- action: "send_keys"
  element:
    type: "AutomationId"
    value: "textBox1"
  keys: "Text to enter"
```

#### clear

Clear an input element.

```yaml
- action: "clear"
  element:
    type: "AutomationId"
    value: "textBox1"
```

#### wait

Wait for specified duration.

```yaml
- action: "wait"
  duration: 2.5  # seconds
```

#### verify

Verify element text.

```yaml
- action: "verify"
  element:
    type: "Name"
    value: "Display"
  expected: "Expected text"
```

#### screenshot

Take a screenshot.

```yaml
- action: "screenshot"
  filename: "screenshot.png"  # optional, auto-generated if not provided
```

### Element Selectors

- **Name**: Element name attribute
- **AutomationId**: Automation ID (preferred for stable identification)
- **ClassName**: Element class name
- **XPath**: XPath expression
- **AccessibilityId**: Accessibility ID (alias for AutomationId)

### Configuration Options

#### Per-Step Options

```yaml
- action: "click"
  element:
    type: "Name"
    value: "Button"
    timeout: 15  # Override default timeout for this element
  continue_on_error: true  # Continue even if this step fails
```

## CLI Reference

### Commands

#### run

Run an automation script.

```bash
python src/cli/main.py run [OPTIONS]
```

**Options:**
- `--script, -s`: Path to automation script (required)
- `--config, -c`: Path to configuration file
- `--server-url`: WinAppDriver server URL (default: http://127.0.0.1:4723)
- `--output, -o`: Output file for results (JSON)
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR)

**Example:**
```bash
python src/cli/main.py run --script test.yaml --config config.yaml --output results.json
```

#### inspect

Launch application in inspect mode.

```bash
python src/cli/main.py inspect [OPTIONS]
```

**Options:**
- `--app-path, -a`: Path to application executable (required)
- `--server-url`: WinAppDriver server URL

**Example:**
```bash
python src/cli/main.py inspect --app-path "C:\Windows\System32\calc.exe"
```

#### batch

Run multiple scripts in batch mode.

```bash
python src/cli/main.py batch [OPTIONS]
```

**Options:**
- `--scripts-dir, -d`: Directory containing scripts (default: examples)
- `--config, -c`: Path to configuration file
- `--server-url`: WinAppDriver server URL
- `--output-dir, -o`: Output directory for results (default: results)

**Example:**
```bash
python src/cli/main.py batch --scripts-dir tests --output-dir test-results
```

#### version

Display version information.

```bash
python src/cli/main.py version
```

## GUI Reference

### Tabs

#### Execute Script
- Select and run automation scripts
- View real-time execution logs
- Monitor execution progress

#### Script Editor
- Create new scripts
- Edit existing scripts
- Save scripts to file
- YAML syntax highlighting (basic)

#### Results
- View detailed execution results
- Export results to file
- Clear results history

#### Settings
- Configure WinAppDriver server URL
- Set default application path
- View about information

### Keyboard Shortcuts

- **Ctrl+O**: Open script
- **Ctrl+S**: Save script
- **Ctrl+N**: New script
- **F5**: Run script

## Configuration File Reference

```yaml
winappdriver:
  server_url: "http://127.0.0.1:4723"
  implicit_wait: 10
  connection_timeout: 30

logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/automation.log"

screenshots:
  enabled: true
  on_error: true
  directory: "screenshots"

reporting:
  format: "html"  # html, json, text
  directory: "reports"

element_wait:
  timeout: 10
  poll_frequency: 0.5

execution:
  continue_on_error: false
  screenshot_before_action: false
  screenshot_after_action: false
```

## Error Handling

### Common Exceptions

- `RuntimeError`: Application not started
- `TimeoutException`: Element not found within timeout
- `NoSuchElementException`: Element not found
- `ImportError`: Appium-Python-Client not installed

### Error Handling in Scripts

```yaml
steps:
  - action: "click"
    element:
      type: "Name"
      value: "Button"
    continue_on_error: true  # Don't stop on failure
```

## Best Practices

1. **Use AutomationId when possible** - More stable than Name or ClassName
2. **Add explicit waits** - After actions that trigger async operations
3. **Take screenshots** - For debugging and documentation
4. **Use meaningful names** - For scripts and elements
5. **Configure timeouts appropriately** - Based on app performance
6. **Handle errors gracefully** - Use continue_on_error when appropriate

## Examples

### Complete Script Example

```yaml
name: "Notepad Save Test"
description: "Test saving a file in Notepad"
app:
  path: "C:\\Windows\\System32\\notepad.exe"

steps:
  - action: "wait"
    duration: 1
  
  - action: "send_keys"
    element:
      type: "ClassName"
      value: "Edit"
    keys: "Hello, WinAppDriver!"
  
  - action: "screenshot"
    filename: "notepad_text_entered.png"
  
  # File -> Save (Ctrl+S)
  - action: "send_keys"
    element:
      type: "ClassName"
      value: "Edit"
    keys: "\ue009s"  # Ctrl+S
  
  - action: "wait"
    duration: 1
```

### Programmatic Usage Example

```python
from core.controller import WinAppDriverController
from core.executor import ScriptExecutor

# Initialize
controller = WinAppDriverController()

# Manual control
controller.start_app("C:\\Windows\\System32\\calc.exe")
button = controller.find_element("Name", "One")
controller.click(button)
controller.screenshot("test.png")
controller.stop_app()

# Script execution
executor = ScriptExecutor(controller)
result = executor.execute_script_file("test.yaml")
print(f"Status: {result['status']}")
```
