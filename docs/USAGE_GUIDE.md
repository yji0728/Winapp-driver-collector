# Usage Guide - Step by Step

This guide walks you through using the WinAppDriver Automation Framework from start to finish.

## Prerequisites Checklist

Before starting, ensure you have:

- ✅ Windows 10 or later
- ✅ Python 3.8+ installed and in PATH
- ✅ WinAppDriver installed
- ✅ Developer Mode enabled
- ✅ Framework dependencies installed (`pip install -r requirements.txt`)

## Part 1: First Time Setup

### Step 1: Install WinAppDriver

1. Download from: https://github.com/microsoft/WinAppDriver/releases
2. Run the installer (e.g., `WindowsApplicationDriver_1.2.1.msi`)
3. Default installation path: `C:\Program Files (x86)\Windows Application Driver\`

### Step 2: Enable Developer Mode

1. Press `Win + I` to open Settings
2. Navigate to: **Update & Security** → **For developers**
3. Select **Developer Mode**
4. Accept the prompt and wait for installation
5. Restart your computer

### Step 3: Clone and Install Framework

```bash
# Open Command Prompt or PowerShell
cd C:\Projects  # or your preferred directory

# Clone the repository
git clone https://github.com/yji0728/Winapp-driver-collector.git
cd Winapp-driver-collector

# Install dependencies
pip install -r requirements.txt

# Verify installation
python src/cli/main.py version
```

Expected output:
```
WinAppDriver Automation Framework
Version: 1.0.0

Dependencies:
  - Appium-Python-Client: 2.9.0 (or similar)
  - Selenium: 4.x.x
  - Click: 8.x.x
  - PyYAML: installed
```

## Part 2: Starting WinAppDriver

### Method 1: Manual Start

```bash
# Open a new Command Prompt
"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
```

You should see:
```
Windows Application Driver listening for requests at: http://127.0.0.1:4723/
Press ENTER to exit.
```

**Keep this window open!**

### Method 2: Background Start (PowerShell)

```powershell
Start-Process "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
```

### Method 3: Run as Administrator (for apps requiring elevation)

1. Right-click `WinAppDriver.exe`
2. Select **Run as administrator**

## Part 3: Using the CLI Interface

### Your First CLI Command

```bash
# Navigate to the framework directory
cd C:\Projects\Winapp-driver-collector

# Run the calculator example
python src/cli/main.py run --script examples/calculator_test.yaml
```

**What happens:**
1. CLI connects to WinAppDriver
2. Calculator opens
3. Script executes (clicks buttons: 1 + 2 =)
4. Screenshots are saved
5. Results are displayed

**Expected output:**
```
Loading script: examples/calculator_test.yaml
Connecting to WinAppDriver at: http://127.0.0.1:4723
Executing script...

============================================================
Script: Calculator Test - Basic Operations
Status: SUCCESS
Duration: 12.34s
Steps: 15 total
  - Success: 15
  - Failed: 0
============================================================
```

### CLI Command Reference

#### Run Single Script
```bash
python src/cli/main.py run --script PATH_TO_SCRIPT
```

**Examples:**
```bash
# Basic usage
python src/cli/main.py run --script examples/calculator_test.yaml

# With custom config
python src/cli/main.py run --script test.yaml --config config/default.yaml

# With JSON output
python src/cli/main.py run --script test.yaml --output results.json

# With debug logging
python src/cli/main.py --log-level DEBUG run --script test.yaml
```

#### Run Multiple Scripts (Batch Mode)
```bash
python src/cli/main.py batch --scripts-dir DIRECTORY
```

**Examples:**
```bash
# Run all scripts in examples folder
python src/cli/main.py batch --scripts-dir examples

# With custom output directory
python src/cli/main.py batch --scripts-dir tests --output-dir test-results

# With configuration
python src/cli/main.py batch --scripts-dir tests --config config/default.yaml
```

#### Inspect Application
```bash
python src/cli/main.py inspect --app-path "PATH_TO_EXE"
```

**Examples:**
```bash
# Inspect Calculator
python src/cli/main.py inspect --app-path "C:\Windows\System32\calc.exe"

# Inspect Notepad
python src/cli/main.py inspect --app-path "C:\Windows\System32\notepad.exe"

# Inspect custom app
python src/cli/main.py inspect --app-path "C:\MyApp\MyApp.exe"
```

**Usage:**
1. App opens and stays open
2. Use Windows Inspect.exe to explore elements
3. Press Enter in terminal to close app

#### Display Version
```bash
python src/cli/main.py version
```

## Part 4: Using the GUI Interface

### Starting the GUI

```bash
# Method 1: Python command
python src/gui/main.py

# Method 2: Batch file (Windows)
run_gui.bat
```

### GUI Walkthrough

#### Tab 1: Execute Script

**Purpose:** Run automation scripts

**Steps:**
1. Click **Browse...** button
2. Select a script file (e.g., `examples/calculator_test.yaml`)
3. Click **▶ Run Script**
4. Watch the **Execution Log** for real-time updates
5. Click **■ Stop** to halt execution (if needed)

**Additional Features:**
- **🔍 Inspect App**: Quick app inspection (requires app path in Settings)
- **Log Output**: Real-time logging of all actions

#### Tab 2: Script Editor

**Purpose:** Create and edit automation scripts

**Steps:**
1. **New Script:**
   - Click **New** to start fresh
   - Edit the YAML content
   - Click **Save As...** to save

2. **Open Existing:**
   - Click **Open**
   - Select a `.yaml` file
   - Edit as needed
   - Click **Save** to update

3. **Example Template:**
   Default example is loaded on startup

**Tips:**
- Use proper YAML syntax (indentation matters!)
- Refer to [API_REFERENCE.md](API_REFERENCE.md) for available actions
- Test frequently with small scripts

#### Tab 3: Results

**Purpose:** View execution results

**Features:**
- Detailed execution summary
- Step-by-step results
- Success/failure indicators
- Error messages for failed steps

**Actions:**
- **Clear**: Remove current results
- **Export**: Save results to file (JSON or TXT)

#### Tab 4: Settings

**Purpose:** Configure framework

**Settings:**
- **Server URL**: WinAppDriver server address (default: http://127.0.0.1:4723)
- **Default App Path**: Set for quick inspection

**About Section:**
- Framework version
- Features list
- GitHub link

## Part 5: Writing Your First Script

### Script Structure

Every script has this structure:

```yaml
name: "Script Name"
description: "What this script does"
app:
  path: "C:\\Path\\To\\Application.exe"
  arguments: ""  # Optional command-line arguments

steps:
  - action: "action_name"
    # action-specific parameters
```

### Example 1: Simple Script

Create `my_first_script.yaml`:

```yaml
name: "My First Test"
description: "Open calculator and press a button"
app:
  path: "C:\\Windows\\System32\\calc.exe"

steps:
  # Wait for app to load
  - action: "wait"
    duration: 2
  
  # Click the number 5
  - action: "click"
    element:
      type: "Name"
      value: "Five"
  
  # Take a screenshot
  - action: "screenshot"
    filename: "my_first_screenshot.png"
```

**Run it:**
```bash
python src/cli/main.py run --script my_first_script.yaml
```

### Example 2: Text Input

Create `text_input_test.yaml`:

```yaml
name: "Text Input Test"
description: "Enter text in Notepad"
app:
  path: "C:\\Windows\\System32\\notepad.exe"

steps:
  - action: "wait"
    duration: 2
  
  - action: "send_keys"
    element:
      type: "ClassName"
      value: "Edit"
    keys: "Hello from WinAppDriver!\nThis is my first automation script."
  
  - action: "screenshot"
    filename: "notepad_result.png"
```

### Example 3: Multiple Operations

Create `calculator_sequence.yaml`:

```yaml
name: "Calculator Sequence"
description: "Perform 10 + 20 - 5"
app:
  path: "C:\\Windows\\System32\\calc.exe"

steps:
  - action: "wait"
    duration: 2
  
  # Enter 10
  - action: "click"
    element:
      type: "Name"
      value: "One"
  
  - action: "click"
    element:
      type: "Name"
      value: "Zero"
  
  # Add
  - action: "click"
    element:
      type: "Name"
      value: "Plus"
  
  # Enter 20
  - action: "click"
    element:
      type: "Name"
      value: "Two"
  
  - action: "click"
    element:
      type: "Name"
      value: "Zero"
  
  # Equals
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
  
  - action: "screenshot"
    filename: "step1_30.png"
  
  # Subtract 5
  - action: "click"
    element:
      type: "Name"
      value: "Minus"
  
  - action: "click"
    element:
      type: "Name"
      value: "Five"
  
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
  
  - action: "screenshot"
    filename: "step2_25.png"
```

## Part 6: Finding UI Elements

### Using Windows Inspect Tool

1. **Open Inspect.exe:**
   ```
   C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\inspect.exe
   ```
   Or search for "Inspect" in Start Menu

2. **Explore Elements:**
   - Hover over UI elements
   - Note the properties:
     - **Name**: Use for `type: "Name"`
     - **AutomationId**: Use for `type: "AutomationId"` (preferred)
     - **ClassName**: Use for `type: "ClassName"`

3. **Example Properties:**
   ```
   Calculator Button "One":
   - Name: "One"
   - AutomationId: "num1Button"
   - ClassName: "Button"
   ```

### Using Framework Inspect Mode

```bash
python src/cli/main.py inspect --app-path "C:\Windows\System32\calc.exe"
```

While app is open:
1. Use Inspect.exe to explore
2. Note element properties
3. Press Enter in terminal when done

## Part 7: Common Patterns

### Pattern 1: Login Form

```yaml
steps:
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "usernameField"
    keys: "myusername"
  
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "passwordField"
    keys: "mypassword"
  
  - action: "click"
    element:
      type: "Name"
      value: "Login"
  
  - action: "wait"
    duration: 2
  
  - action: "screenshot"
    filename: "logged_in.png"
```

### Pattern 2: Menu Navigation

```yaml
steps:
  # Click menu
  - action: "click"
    element:
      type: "Name"
      value: "File"
  
  - action: "wait"
    duration: 0.5
  
  # Click submenu item
  - action: "click"
    element:
      type: "Name"
      value: "Save As..."
```

### Pattern 3: Error Handling

```yaml
steps:
  # Critical action
  - action: "click"
    element:
      type: "Name"
      value: "Important Button"
  
  # Optional action - don't fail if missing
  - action: "click"
    element:
      type: "Name"
      value: "Optional Button"
    continue_on_error: true
```

## Part 8: Troubleshooting

### Issue: Script doesn't run

**Check:**
1. Is WinAppDriver running?
   ```bash
   curl http://127.0.0.1:4723/status
   ```

2. Is Python in PATH?
   ```bash
   python --version
   ```

3. Are dependencies installed?
   ```bash
   pip list | findstr Appium
   ```

### Issue: Element not found

**Solutions:**
1. Increase timeout:
   ```yaml
   element:
     type: "Name"
     value: "Button"
     timeout: 20  # Increase from default 10
   ```

2. Add wait before action:
   ```yaml
   - action: "wait"
     duration: 2
   ```

3. Verify element name with Inspect.exe

### Issue: Screenshots not saved

**Check:**
- Screenshots directory exists
- Correct path in filename
- Write permissions

**Create directory:**
```bash
mkdir screenshots
```

## Part 9: Best Practices

### ✅ DO:
- Use AutomationId when available
- Add waits after slow operations
- Take screenshots at key points
- Use meaningful script names
- Test scripts incrementally

### ❌ DON'T:
- Use excessively long waits
- Rely only on Name selectors
- Skip error handling
- Create overly complex scripts
- Hardcode environment-specific paths

## Part 10: Next Steps

### Continue Learning:
1. Read [EXAMPLES.md](EXAMPLES.md) for more patterns
2. Study [API_REFERENCE.md](API_REFERENCE.md) for all actions
3. Review [SPECIFICATIONS.md](SPECIFICATIONS.md) for details

### Contribute:
1. Share your scripts
2. Report bugs
3. Suggest features
4. Improve documentation

### Get Help:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open GitHub Issue
- Review existing Issues

---

**You're ready to automate! 🎉**

Start with simple scripts and gradually build complexity. Happy automating!
