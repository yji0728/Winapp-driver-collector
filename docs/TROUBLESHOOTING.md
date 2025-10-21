# Troubleshooting Guide

Common issues and their solutions for WinAppDriver Automation Framework.

## Installation Issues

### Issue: Python not found

**Symptom:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
1. Install Python 3.8 or later from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation: `python --version`

### Issue: pip not found

**Symptom:**
```
'pip' is not recognized as an internal or external command
```

**Solution:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Issue: Dependencies installation fails

**Symptom:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies one by one
pip install Appium-Python-Client
pip install selenium
pip install click
pip install PyYAML

# Or from requirements.txt
pip install -r requirements.txt --no-cache-dir
```

## WinAppDriver Issues

### Issue: WinAppDriver not starting

**Symptom:**
```
Error: Cannot connect to WinAppDriver at http://127.0.0.1:4723
```

**Solutions:**

1. **Check if WinAppDriver is installed:**
   - Look for `C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe`
   - If not found, download from [WinAppDriver Releases](https://github.com/microsoft/WinAppDriver/releases)

2. **Start WinAppDriver manually:**
   ```bash
   "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
   ```

3. **Check if port 4723 is already in use:**
   ```bash
   netstat -ano | findstr :4723
   ```
   If occupied, kill the process:
   ```bash
   taskkill /PID <process_id> /F
   ```

4. **Run as Administrator:**
   - Right-click WinAppDriver.exe
   - Select "Run as administrator"

### Issue: Developer Mode not enabled

**Symptom:**
```
Error: Developer Mode is not enabled
```

**Solution:**
1. Open Windows Settings (Win + I)
2. Go to Update & Security → For developers
3. Select "Developer Mode"
4. Restart Windows
5. Restart WinAppDriver

### Issue: Firewall blocking WinAppDriver

**Symptom:**
```
Connection timeout when connecting to WinAppDriver
```

**Solution:**
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Add WinAppDriver.exe to allowed apps
4. Check both Private and Public network boxes

## Application Issues

### Issue: Application not starting

**Symptom:**
```
Error: Failed to start application
```

**Solutions:**

1. **Verify application path:**
   ```yaml
   app:
     path: "C:\\Windows\\System32\\calc.exe"  # Use double backslashes
   ```

2. **Check if application requires admin rights:**
   - Run WinAppDriver as administrator
   - Or change app to not require admin

3. **Verify application architecture:**
   - Ensure WinAppDriver architecture matches app (32-bit vs 64-bit)

4. **Check for multiple instances:**
   - Close any running instances of the app
   - Or use app-specific identifiers

### Issue: Application closes immediately

**Symptom:**
Application starts but closes before automation can begin

**Solution:**
Add wait time at the beginning of your script:
```yaml
steps:
  - action: "wait"
    duration: 3  # Wait for app to fully load
```

## Element Location Issues

### Issue: Element not found

**Symptom:**
```
TimeoutException: Element not found within timeout
```

**Solutions:**

1. **Use Windows Inspect.exe to verify element properties:**
   ```bash
   "C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\inspect.exe"
   ```

2. **Increase timeout:**
   ```yaml
   - action: "click"
     element:
       type: "Name"
       value: "Button"
       timeout: 30  # Increase from default 10
   ```

3. **Try different locator strategies:**
   ```yaml
   # Instead of Name
   element:
     type: "AutomationId"
     value: "button1"
   
   # Or ClassName
   element:
     type: "ClassName"
     value: "Button"
   
   # Or XPath
   element:
     type: "XPath"
     value: "//Button[@Name='OK']"
   ```

4. **Add explicit wait before finding element:**
   ```yaml
   - action: "wait"
     duration: 2
   
   - action: "click"
     element:
       type: "Name"
       value: "Button"
   ```

5. **Check element visibility:**
   - Ensure element is visible on screen
   - Scroll to element if needed
   - Check if element is in a different window/tab

### Issue: Wrong element selected

**Symptom:**
Action is performed on wrong element

**Solution:**
1. **Use more specific locators:**
   ```yaml
   # Too generic
   element:
     type: "Name"
     value: "OK"
   
   # More specific with XPath
   element:
     type: "XPath"
     value: "//Window[@Name='Dialog']/Button[@Name='OK']"
   ```

2. **Use AutomationId (most reliable):**
   ```yaml
   element:
     type: "AutomationId"
     value: "OkButton"
   ```

## Script Execution Issues

### Issue: Script fails to load

**Symptom:**
```
Error: Failed to load script
```

**Solutions:**

1. **Verify YAML syntax:**
   ```bash
   python -c "import yaml; yaml.safe_load(open('your_script.yaml'))"
   ```

2. **Check file encoding:**
   - Save file as UTF-8
   - Avoid special characters in file path

3. **Validate YAML structure:**
   ```yaml
   name: "Test"  # Required
   description: "Description"  # Required
   app:  # Required
     path: "C:\\Path\\To\\App.exe"
   steps:  # Required
     - action: "wait"
       duration: 1
   ```

### Issue: Script execution hangs

**Symptom:**
Script execution stops responding

**Solutions:**

1. **Add timeouts to elements:**
   ```yaml
   element:
     type: "Name"
     value: "Button"
     timeout: 15  # Prevent infinite wait
   ```

2. **Reduce implicit wait:**
   ```yaml
   winappdriver:
     implicit_wait: 5  # Reduce from 10
   ```

3. **Check for modal dialogs:**
   - Application might show unexpected dialog
   - Add steps to handle dialogs

### Issue: Screenshots not saved

**Symptom:**
Screenshot action executes but file not found

**Solutions:**

1. **Check directory exists:**
   ```bash
   mkdir screenshots
   ```

2. **Use absolute path:**
   ```yaml
   - action: "screenshot"
     filename: "C:\\Users\\YourName\\screenshots\\test.png"
   ```

3. **Check permissions:**
   - Ensure write permissions in directory
   - Run as administrator if needed

## GUI Issues

### Issue: GUI not starting

**Symptom:**
```
Error: Tk not available
```

**Solution:**
1. Tkinter is included with Python on Windows
2. If missing, reinstall Python with Tkinter option checked

### Issue: GUI freezes during execution

**Symptom:**
GUI becomes unresponsive while script runs

**Solution:**
This is expected behavior in version 1.0.0. The GUI runs in the main thread and blocks during script execution. Future versions will implement asynchronous execution.

**Workaround:**
Use CLI for long-running scripts:
```bash
python src/cli/main.py run --script your_script.yaml
```

### Issue: Script editor doesn't show syntax highlighting

**Symptom:**
YAML script appears as plain text

**Solution:**
This is expected in version 1.0.0. Basic text editing is supported. For syntax highlighting:
1. Use external editor (VS Code, Notepad++, etc.)
2. Copy/paste into GUI editor
3. Or edit files directly and open in GUI

## CLI Issues

### Issue: Command not recognized

**Symptom:**
```
Error: No such command 'run'
```

**Solution:**
Check command syntax:
```bash
python src/cli/main.py run --script examples/calculator_test.yaml
#                       ^^^
#                       command name
```

### Issue: Log level not working

**Symptom:**
Debug messages not showing despite --log-level DEBUG

**Solution:**
1. Clear any existing log files
2. Use correct syntax:
   ```bash
   python src/cli/main.py --log-level DEBUG run --script test.yaml
   #                      ^^^^^^^^^^^^^^^^^^^
   #                      Before the command
   ```

## Performance Issues

### Issue: Script execution is slow

**Symptom:**
Script takes much longer than expected

**Solutions:**

1. **Reduce unnecessary waits:**
   ```yaml
   # Don't use arbitrary waits
   - action: "wait"
     duration: 10  # Too long
   
   # Use element-based waits instead
   - action: "click"
     element:
       type: "Name"
       value: "Button"
       timeout: 10  # Only wait until element found
   ```

2. **Reduce implicit wait:**
   ```yaml
   winappdriver:
     implicit_wait: 5  # Lower value for faster failures
   ```

3. **Disable unnecessary screenshots:**
   ```yaml
   screenshots:
     enabled: false  # Disable if not needed
   ```

4. **Use specific locators:**
   - AutomationId is fastest
   - XPath can be slower
   - Name is moderate

## Network Issues

### Issue: Cannot connect to remote WinAppDriver

**Symptom:**
```
Error: Connection refused when connecting to remote server
```

**Solutions:**

1. **Verify server URL:**
   ```yaml
   winappdriver:
     server_url: "http://192.168.1.100:4723"  # Include http://
   ```

2. **Check firewall on remote machine:**
   - Allow incoming connections on port 4723
   - Allow WinAppDriver.exe through firewall

3. **Test connectivity:**
   ```bash
   curl http://remote-ip:4723/status
   ```

4. **Use correct network adapter:**
   - Ensure using correct IP address
   - Try localhost first: http://127.0.0.1:4723

## Debugging Tips

### Enable Debug Logging

**CLI:**
```bash
python src/cli/main.py --log-level DEBUG run --script test.yaml
```

**Configuration:**
```yaml
logging:
  level: "DEBUG"
```

### Take Screenshots on Each Step

```yaml
execution:
  screenshot_after_action: true
```

### Use Inspect Mode

```bash
python src/cli/main.py inspect --app-path "C:\Windows\System32\calc.exe"
```

Then use Windows Inspect.exe to explore elements.

### Check Logs

```
# Check automation.log
tail -f automation.log  # Linux/Mac
type automation.log     # Windows

# Or GUI logs
tail -f logs/gui.log    # Linux/Mac
type logs\gui.log       # Windows
```

### Verify WinAppDriver Status

```bash
curl http://127.0.0.1:4723/status
```

Expected response:
```json
{
  "value": {
    "ready": true,
    "message": "WinAppDriver is ready"
  }
}
```

## Getting Help

If you're still experiencing issues:

1. **Check existing GitHub Issues:**
   - [Open Issues](https://github.com/yji0728/Winapp-driver-collector/issues)
   - Search for similar problems

2. **Create a new Issue with:**
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment information:
     ```
     Windows Version: 
     Python Version: 
     WinAppDriver Version: 
     Framework Version: 
     ```
   - Relevant logs/screenshots
   - Script that reproduces the issue (if applicable)

3. **Community Resources:**
   - [WinAppDriver GitHub](https://github.com/microsoft/WinAppDriver)
   - [Stack Overflow - winappdriver tag](https://stackoverflow.com/questions/tagged/winappdriver)
   - Microsoft documentation

## Reporting Bugs

When reporting bugs, include:

```
**Environment:**
- OS: Windows 10 21H2
- Python: 3.10.5
- Framework: 1.0.0
- WinAppDriver: 1.2.1

**Steps to Reproduce:**
1. Start WinAppDriver
2. Run: python src/cli/main.py run --script test.yaml
3. Observe error

**Expected Behavior:**
Script should execute successfully

**Actual Behavior:**
Error: Element not found

**Logs:**
[Paste relevant log output]

**Script:**
```yaml
[Paste minimal script that reproduces issue]
```

---

For more help, see:
- [Quick Start Guide](QUICKSTART.md)
- [API Reference](API_REFERENCE.md)
- [Specifications](SPECIFICATIONS.md)
