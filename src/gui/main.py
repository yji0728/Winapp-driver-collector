"""
GUI Main - Graphical interface for WinAppDriver automation
"""

import sys
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import yaml
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.controller import WinAppDriverController
from core.executor import ScriptExecutor


class WinAppDriverGUI:
    """Main GUI application for WinAppDriver automation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("WinAppDriver Automation Framework")
        self.root.geometry("1000x700")
        
        # Variables
        self.server_url = tk.StringVar(value="http://127.0.0.1:4723")
        self.app_path = tk.StringVar()
        self.script_path = tk.StringVar()
        self.status = tk.StringVar(value="Ready")
        
        self.controller = None
        self.executor = None
        self.is_running = False
        
        # Setup logging
        self._setup_logging()
        
        # Create UI
        self._create_ui()
        
        logging.info("GUI initialized")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/gui.log'),
                logging.StreamHandler()
            ]
        )
    
    def _create_ui(self):
        """Create the user interface."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.tab_execute = ttk.Frame(notebook)
        self.tab_script_editor = ttk.Frame(notebook)
        self.tab_results = ttk.Frame(notebook)
        self.tab_settings = ttk.Frame(notebook)
        
        notebook.add(self.tab_execute, text="Execute Script")
        notebook.add(self.tab_script_editor, text="Script Editor")
        notebook.add(self.tab_results, text="Results")
        notebook.add(self.tab_settings, text="Settings")
        
        # Setup tabs
        self._create_execute_tab()
        self._create_script_editor_tab()
        self._create_results_tab()
        self._create_settings_tab()
        
        # Status bar
        self._create_status_bar()
    
    def _create_execute_tab(self):
        """Create the execution tab."""
        frame = self.tab_execute
        
        # Script selection
        script_frame = ttk.LabelFrame(frame, text="Script Selection", padding=10)
        script_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(script_frame, text="Script File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(script_frame, textvariable=self.script_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(script_frame, text="Browse...", command=self._browse_script).grid(row=0, column=2)
        
        # Control buttons
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.btn_run = ttk.Button(control_frame, text="▶ Run Script", command=self._run_script)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = ttk.Button(control_frame, text="■ Stop", command=self._stop_execution, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="🔍 Inspect App", command=self._inspect_app).pack(side=tk.LEFT, padx=5)
        
        # Log output
        log_frame = ttk.LabelFrame(frame, text="Execution Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add log handler
        self._add_log_handler()
    
    def _create_script_editor_tab(self):
        """Create the script editor tab."""
        frame = self.tab_script_editor
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="New", command=self._new_script).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Open", command=self._open_script).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Save", command=self._save_script).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Save As...", command=self._save_script_as).pack(side=tk.LEFT, padx=2)
        
        # Editor
        editor_frame = ttk.LabelFrame(frame, text="Script Editor (YAML)", padding=10)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.script_editor = scrolledtext.ScrolledText(editor_frame, height=25, wrap=tk.WORD)
        self.script_editor.pack(fill=tk.BOTH, expand=True)
        
        # Load example
        self._load_example_script()
    
    def _create_results_tab(self):
        """Create the results tab."""
        frame = self.tab_results
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="Clear", command=self._clear_results).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Export", command=self._export_results).pack(side=tk.LEFT, padx=2)
        
        # Results display
        results_frame = ttk.LabelFrame(frame, text="Execution Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=25, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_settings_tab(self):
        """Create the settings tab."""
        frame = self.tab_settings
        
        # Server settings
        server_frame = ttk.LabelFrame(frame, text="WinAppDriver Settings", padding=10)
        server_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(server_frame, text="Server URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(server_frame, textvariable=self.server_url, width=40).grid(row=0, column=1, padx=5)
        
        # Application settings
        app_frame = ttk.LabelFrame(frame, text="Application Settings", padding=10)
        app_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(app_frame, text="Default App Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(app_frame, textvariable=self.app_path, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(app_frame, text="Browse...", command=self._browse_app).grid(row=0, column=2)
        
        # About section
        about_frame = ttk.LabelFrame(frame, text="About", padding=10)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        about_text = """WinAppDriver Automation Framework
Version: 1.0.0

A comprehensive automation framework for Windows applications
using Microsoft WinAppDriver.

Features:
• Visual script editing
• Real-time execution monitoring
• Element inspection
• Batch execution
• Detailed reporting

For more information, visit:
https://github.com/yji0728/Winapp-driver-collector
"""
        ttk.Label(about_frame, text=about_text, justify=tk.LEFT).pack(anchor=tk.W)
    
    def _create_status_bar(self):
        """Create the status bar."""
        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Label(status_bar, textvariable=self.status, relief=tk.SUNKEN).pack(fill=tk.X, padx=2, pady=2)
    
    def _add_log_handler(self):
        """Add custom log handler to display logs in GUI."""
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)
        
        handler = TextHandler(self.log_text)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(handler)
    
    def _browse_script(self):
        """Browse for script file."""
        filename = filedialog.askopenfilename(
            title="Select Script File",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")]
        )
        if filename:
            self.script_path.set(filename)
    
    def _browse_app(self):
        """Browse for application executable."""
        filename = filedialog.askopenfilename(
            title="Select Application",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.app_path.set(filename)
    
    def _run_script(self):
        """Run the selected script."""
        script_file = self.script_path.get()
        
        if not script_file:
            messagebox.showerror("Error", "Please select a script file")
            return
        
        if not Path(script_file).exists():
            messagebox.showerror("Error", f"Script file not found: {script_file}")
            return
        
        # Run in separate thread
        self.is_running = True
        self.btn_run.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.status.set("Running...")
        
        thread = threading.Thread(target=self._execute_script, args=(script_file,))
        thread.daemon = True
        thread.start()
    
    def _execute_script(self, script_file):
        """Execute script in background thread."""
        try:
            # Initialize controller
            server = self.server_url.get()
            self.controller = WinAppDriverController(server_url=server)
            self.executor = ScriptExecutor(self.controller)
            
            # Execute
            result = self.executor.execute_script_file(script_file)
            
            # Display results
            self._display_results(result)
            
            self.status.set(f"Completed: {result['status']}")
            
            if result['status'] == 'success':
                messagebox.showinfo("Success", "Script executed successfully!")
            else:
                messagebox.showwarning("Failed", f"Script execution failed: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            logging.exception("Execution failed")
            messagebox.showerror("Error", f"Execution failed: {str(e)}")
            self.status.set("Error")
        
        finally:
            self.is_running = False
            self.btn_run.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
    
    def _stop_execution(self):
        """Stop the current execution."""
        if self.controller:
            try:
                self.controller.stop_app()
            except:
                pass
        
        self.is_running = False
        self.status.set("Stopped")
    
    def _inspect_app(self):
        """Launch app in inspect mode."""
        app = self.app_path.get()
        
        if not app:
            messagebox.showinfo("Info", 
                "Please set the application path in Settings tab.\n\n"
                "Alternatively, use Windows Inspect.exe tool directly to explore UI elements.")
            return
        
        if not Path(app).exists():
            messagebox.showerror("Error", f"Application not found: {app}")
            return
        
        try:
            server = self.server_url.get()
            self.controller = WinAppDriverController(server_url=server)
            self.controller.start_app(app)
            
            messagebox.showinfo("Inspect Mode", 
                f"Application started: {app}\n\n"
                "Use Windows Inspect.exe to explore UI elements.\n"
                "Click OK to close the application.")
            
            self.controller.stop_app()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start application: {str(e)}")
    
    def _display_results(self, result):
        """Display execution results."""
        self.results_text.delete(1.0, tk.END)
        
        # Format results
        output = f"""
{'='*60}
Script: {result['name']}
Status: {result['status'].upper()}
Duration: {result['duration']:.2f}s
{'='*60}

Steps: {len(result['steps'])} total
"""
        
        for step in result['steps']:
            status_icon = "✓" if step['success'] else "✗"
            output += f"\n{status_icon} Step {step['step']}: {step['action']}"
            if not step['success']:
                output += f"\n  Error: {step['error']}"
        
        if result.get('error'):
            output += f"\n\nScript Error: {result['error']}"
        
        self.results_text.insert(1.0, output)
    
    def _clear_results(self):
        """Clear the results display."""
        self.results_text.delete(1.0, tk.END)
    
    def _export_results(self):
        """Export results to file."""
        filename = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            content = self.results_text.get(1.0, tk.END)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Results exported to:\n{filename}")
    
    def _new_script(self):
        """Create a new script."""
        if messagebox.askyesno("New Script", "Clear current script?"):
            self._load_example_script()
    
    def _open_script(self):
        """Open a script file."""
        filename = filedialog.askopenfilename(
            title="Open Script",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.script_editor.delete(1.0, tk.END)
                self.script_editor.insert(1.0, content)
                self.script_path.set(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def _save_script(self):
        """Save the current script."""
        script_file = self.script_path.get()
        
        if not script_file:
            self._save_script_as()
        else:
            self._save_to_file(script_file)
    
    def _save_script_as(self):
        """Save the script to a new file."""
        filename = filedialog.asksaveasfilename(
            title="Save Script As",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if filename:
            self._save_to_file(filename)
            self.script_path.set(filename)
    
    def _save_to_file(self, filename):
        """Save script content to file."""
        try:
            content = self.script_editor.get(1.0, tk.END)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Script saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def _load_example_script(self):
        """Load an example script."""
        example = """name: "Calculator Test"
description: "Basic calculator operations"
app:
  path: "C:\\\\Windows\\\\System32\\\\calc.exe"
  arguments: ""

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
      value: "Two"
    
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
    
  - action: "screenshot"
    filename: "calculator_result.png"
"""
        self.script_editor.delete(1.0, tk.END)
        self.script_editor.insert(1.0, example)


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = WinAppDriverGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
