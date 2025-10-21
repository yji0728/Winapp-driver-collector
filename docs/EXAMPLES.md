# Examples and Use Cases

This document provides practical examples and common use cases for the WinAppDriver Automation Framework.

## Table of Contents
1. [Basic Examples](#basic-examples)
2. [Advanced Examples](#advanced-examples)
3. [Real-World Use Cases](#real-world-use-cases)
4. [Best Practices](#best-practices)

## Basic Examples

### Example 1: Simple Button Click

Test a simple calculator operation:

```yaml
name: "Simple Addition"
description: "Click buttons to perform 1 + 1"
app:
  path: "C:\\Windows\\System32\\calc.exe"

steps:
  - action: "wait"
    duration: 2
  
  - action: "click"
    element:
      type: "Name"
      value: "One"
  
  - action: "click"
    element:
      type: "Name"
      value: "Plus"
  
  - action: "click"
    element:
      type: "Name"
      value: "One"
  
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
  
  - action: "screenshot"
    filename: "result.png"
```

**Run:**
```bash
python src/cli/main.py run --script examples/simple_addition.yaml
```

### Example 2: Text Input

Enter text into Notepad:

```yaml
name: "Text Input Test"
description: "Type text in Notepad"
app:
  path: "C:\\Windows\\System32\\notepad.exe"

steps:
  - action: "wait"
    duration: 2
  
  - action: "send_keys"
    element:
      type: "ClassName"
      value: "Edit"
    keys: "Hello, World!\nThis is a test."
  
  - action: "screenshot"
    filename: "notepad_test.png"
```

### Example 3: Element Verification

Verify calculator result:

```yaml
name: "Result Verification"
description: "Verify calculation result"
app:
  path: "C:\\Windows\\System32\\calc.exe"

steps:
  - action: "wait"
    duration: 2
  
  - action: "click"
    element:
      type: "Name"
      value: "Two"
  
  - action: "click"
    element:
      type: "Name"
      value: "Plus"
  
  - action: "click"
    element:
      type: "Name"
      value: "Two"
  
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
  
  - action: "verify"
    element:
      type: "AutomationId"
      value: "CalculatorResults"
    expected: "4"
```

## Advanced Examples

### Example 4: Multiple Operations with Error Handling

```yaml
name: "Calculator Stress Test"
description: "Perform multiple calculations with error handling"
app:
  path: "C:\\Windows\\System32\\calc.exe"

steps:
  # Test 1: Simple addition
  - action: "click"
    element:
      type: "Name"
      value: "Five"
  
  - action: "click"
    element:
      type: "Name"
      value: "Plus"
  
  - action: "click"
    element:
      type: "Name"
      value: "Three"
  
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
  
  - action: "screenshot"
    filename: "test1.png"
  
  # Clear for next test
  - action: "click"
    element:
      type: "Name"
      value: "Clear"
  
  # Test 2: Division by zero (expect error, but continue)
  - action: "click"
    element:
      type: "Name"
      value: "One"
    continue_on_error: true
  
  - action: "click"
    element:
      type: "Name"
      value: "Divide by"
    continue_on_error: true
  
  - action: "click"
    element:
      type: "Name"
      value: "Zero"
    continue_on_error: true
  
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
    continue_on_error: true
  
  - action: "screenshot"
    filename: "test2_error.png"
  
  # Continue with more tests...
  - action: "click"
    element:
      type: "Name"
      value: "Clear entry"
    continue_on_error: true
```

### Example 5: Using XPath Selectors

```yaml
name: "XPath Selector Example"
description: "Use XPath for complex element selection"
app:
  path: "C:\\Windows\\System32\\calc.exe"

steps:
  - action: "wait"
    duration: 2
  
  # Use XPath to find specific button
  - action: "click"
    element:
      type: "XPath"
      value: "//Button[@Name='One']"
  
  - action: "click"
    element:
      type: "XPath"
      value: "//Button[@Name='Plus']"
  
  # XPath with multiple conditions
  - action: "click"
    element:
      type: "XPath"
      value: "//Button[@AutomationId='num2Button' and @Name='Two']"
  
  - action: "click"
    element:
      type: "XPath"
      value: "//Button[@Name='Equals']"
```

### Example 6: Conditional Actions with Timeouts

```yaml
name: "Timeout and Retry Example"
description: "Handle slow-loading elements"
app:
  path: "C:\\Path\\To\\SlowApp.exe"

steps:
  - action: "wait"
    duration: 5  # Wait for app to load
  
  # Element with extended timeout
  - action: "click"
    element:
      type: "AutomationId"
      value: "loadingButton"
      timeout: 30  # Wait up to 30 seconds
  
  # Wait for processing
  - action: "wait"
    duration: 10
  
  # Another element with custom timeout
  - action: "send_keys"
    element:
      type: "ClassName"
      value: "TextBox"
      timeout: 20
    keys: "Processed data"
```

## Real-World Use Cases

### Use Case 1: Form Filling Automation

Automate filling out a complex form:

```yaml
name: "Form Automation"
description: "Fill out registration form"
app:
  path: "C:\\Path\\To\\FormApp.exe"

steps:
  - action: "wait"
    duration: 3
  
  # Fill first name
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "firstNameField"
    keys: "John"
  
  # Fill last name
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "lastNameField"
    keys: "Doe"
  
  # Fill email
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "emailField"
    keys: "john.doe@example.com"
  
  # Select dropdown option (if using combobox)
  - action: "click"
    element:
      type: "AutomationId"
      value: "countryDropdown"
  
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "countryDropdown"
    keys: "United States"
  
  # Submit form
  - action: "click"
    element:
      type: "Name"
      value: "Submit"
  
  - action: "wait"
    duration: 2
  
  # Verify success
  - action: "screenshot"
    filename: "form_submitted.png"
```

### Use Case 2: Regression Testing

Create regression tests for your application:

```yaml
name: "Feature X Regression Test"
description: "Verify Feature X works correctly after updates"
app:
  path: "C:\\Path\\To\\YourApp.exe"

steps:
  # Setup
  - action: "wait"
    duration: 2
  
  # Navigate to feature
  - action: "click"
    element:
      type: "Name"
      value: "File"
  
  - action: "click"
    element:
      type: "Name"
      value: "Open Feature X"
  
  - action: "wait"
    duration: 1
  
  # Test feature functionality
  - action: "click"
    element:
      type: "AutomationId"
      value: "featureXButton"
  
  - action: "wait"
    duration: 2
  
  # Verify expected result
  - action: "verify"
    element:
      type: "AutomationId"
      value: "resultLabel"
    expected: "Success"
  
  # Take evidence screenshot
  - action: "screenshot"
    filename: "regression_test_passed.png"
  
  # Cleanup
  - action: "click"
    element:
      type: "Name"
      value: "Close"
```

### Use Case 3: Data Entry Validation

Test data validation rules:

```yaml
name: "Data Validation Test"
description: "Test input validation rules"
app:
  path: "C:\\Path\\To\\App.exe"

steps:
  - action: "wait"
    duration: 2
  
  # Test 1: Invalid email format
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "emailInput"
    keys: "invalid-email"
  
  - action: "click"
    element:
      type: "Name"
      value: "Validate"
  
  - action: "verify"
    element:
      type: "AutomationId"
      value: "errorMessage"
    expected: "Invalid email format"
  
  - action: "screenshot"
    filename: "invalid_email_test.png"
  
  # Clear and test valid email
  - action: "clear"
    element:
      type: "AutomationId"
      value: "emailInput"
  
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "emailInput"
    keys: "valid@example.com"
  
  - action: "click"
    element:
      type: "Name"
      value: "Validate"
  
  - action: "verify"
    element:
      type: "AutomationId"
      value: "successMessage"
    expected: "Valid email"
  
  - action: "screenshot"
    filename: "valid_email_test.png"
```

### Use Case 4: Performance Testing

Monitor application responsiveness:

```yaml
name: "Performance Test"
description: "Measure application response times"
app:
  path: "C:\\Path\\To\\App.exe"

steps:
  - action: "wait"
    duration: 2
  
  # Operation 1
  - action: "click"
    element:
      type: "Name"
      value: "Heavy Operation"
  
  - action: "screenshot"
    filename: "operation_start.png"
  
  # Wait for completion (30 sec max)
  - action: "wait"
    duration: 30
  
  - action: "screenshot"
    filename: "operation_complete.png"
  
  # Verify completion
  - action: "verify"
    element:
      type: "AutomationId"
      value: "statusLabel"
    expected: "Completed"
```

## Best Practices

### 1. Use Meaningful Names

**Good:**
```yaml
name: "User Login - Valid Credentials"
description: "Test successful login with valid username and password"
```

**Bad:**
```yaml
name: "Test1"
description: "test"
```

### 2. Add Wait Times Strategically

**Good:**
```yaml
steps:
  # Wait after app start
  - action: "wait"
    duration: 2
  
  - action: "click"
    element:
      type: "Name"
      value: "Load Data"
  
  # Wait for data to load
  - action: "wait"
    duration: 3
```

**Bad:**
```yaml
steps:
  - action: "wait"
    duration: 10  # Arbitrary long wait
  
  - action: "click"
    element:
      type: "Name"
      value: "Button"
  
  - action: "wait"
    duration: 10  # Another arbitrary wait
```

### 3. Use AutomationId When Possible

**Good:**
```yaml
element:
  type: "AutomationId"
  value: "submitButton"
```

**Less Reliable:**
```yaml
element:
  type: "Name"
  value: "Submit"  # Names can change with translations
```

### 4. Take Screenshots at Key Points

```yaml
steps:
  - action: "click"
    element:
      type: "Name"
      value: "Process"
  
  - action: "screenshot"
    filename: "before_processing.png"
  
  - action: "wait"
    duration: 5
  
  - action: "screenshot"
    filename: "after_processing.png"
```

### 5. Handle Errors Gracefully

```yaml
steps:
  # Critical step - stop on error
  - action: "click"
    element:
      type: "Name"
      value: "Critical Button"
  
  # Optional step - continue on error
  - action: "click"
    element:
      type: "Name"
      value: "Optional Button"
    continue_on_error: true
```

### 6. Organize Tests Logically

```
tests/
├── login/
│   ├── valid_login.yaml
│   ├── invalid_password.yaml
│   └── locked_account.yaml
├── data_entry/
│   ├── create_record.yaml
│   ├── edit_record.yaml
│   └── delete_record.yaml
└── reporting/
    ├── generate_report.yaml
    └── export_data.yaml
```

### 7. Use Configuration Files

```yaml
# config/staging.yaml
winappdriver:
  server_url: "http://staging-server:4723"
  
# config/production.yaml
winappdriver:
  server_url: "http://prod-server:4723"
```

Run with specific config:
```bash
python src/cli/main.py run --script test.yaml --config config/staging.yaml
```

## Programmatic Usage

For more complex scenarios, use the framework programmatically:

```python
from src.core.controller import WinAppDriverController
from src.core.executor import ScriptExecutor

# Initialize controller
controller = WinAppDriverController(
    server_url="http://127.0.0.1:4723",
    implicit_wait=10
)

# Manual control
controller.start_app("C:\\Windows\\System32\\calc.exe")

# Find and interact with elements
button_one = controller.find_element("Name", "One")
controller.click(button_one)

button_plus = controller.find_element("Name", "Plus")
controller.click(button_plus)

button_two = controller.find_element("Name", "Two")
controller.click(button_two)

button_equals = controller.find_element("Name", "Equals")
controller.click(button_equals)

# Take screenshot
controller.screenshot("result.png")

# Clean up
controller.stop_app()

# Or use script executor
executor = ScriptExecutor(controller)
result = executor.execute_script_file("examples/calculator_test.yaml")

print(f"Status: {result['status']}")
print(f"Duration: {result['duration']:.2f}s")
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: UI Tests

on: [push, pull_request]

jobs:
  ui-tests:
    runs-on: windows-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Start WinAppDriver
        run: |
          Start-Process "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
          Start-Sleep -Seconds 5
      
      - name: Run tests
        run: python src/cli/main.py batch --scripts-dir tests
      
      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: screenshots
          path: screenshots/
```

---

For more examples, see the [examples/](../examples/) directory in the repository.
