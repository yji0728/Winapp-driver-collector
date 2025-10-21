"""
CLI Main - Command-line interface for WinAppDriver automation
"""

import sys
import logging
import click
import yaml
import json
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.controller import WinAppDriverController
from core.executor import ScriptExecutor


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('automation.log')
        ]
    )


def load_config(config_path: Optional[str]) -> dict:
    """Load configuration from file."""
    if not config_path or not Path(config_path).exists():
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


@click.group()
@click.option('--log-level', default='INFO', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
              help='Set logging level')
def cli(log_level):
    """WinAppDriver Automation Framework CLI"""
    setup_logging(log_level)


@cli.command()
@click.option('--script', '-s', required=True, help='Path to automation script (YAML)')
@click.option('--config', '-c', help='Path to configuration file')
@click.option('--server-url', default='http://127.0.0.1:4723', 
              help='WinAppDriver server URL')
@click.option('--output', '-o', help='Output file for results (JSON)')
def run(script: str, config: Optional[str], server_url: str, output: Optional[str]):
    """
    Run an automation script.
    
    Example:
        python main.py run --script examples/calculator_test.yaml
    """
    try:
        click.echo(f"Loading script: {script}")
        
        # Load configuration
        config_dict = load_config(config)
        
        # Override server URL if provided
        if server_url:
            config_dict.setdefault('winappdriver', {})['server_url'] = server_url
        
        # Initialize controller
        server = config_dict.get('winappdriver', {}).get('server_url', server_url)
        implicit_wait = config_dict.get('winappdriver', {}).get('implicit_wait', 10)
        
        click.echo(f"Connecting to WinAppDriver at: {server}")
        controller = WinAppDriverController(server_url=server, implicit_wait=implicit_wait)
        
        # Initialize executor
        executor = ScriptExecutor(controller, config_dict)
        
        # Execute script
        click.echo(f"Executing script...")
        result = executor.execute_script_file(script)
        
        # Display results
        click.echo("\n" + "="*60)
        click.echo(f"Script: {result['name']}")
        click.echo(f"Status: {result['status'].upper()}")
        click.echo(f"Duration: {result['duration']:.2f}s")
        click.echo(f"Steps: {len(result['steps'])} total")
        
        success_count = sum(1 for s in result['steps'] if s['success'])
        click.echo(f"  - Success: {success_count}")
        click.echo(f"  - Failed: {len(result['steps']) - success_count}")
        
        if result['error']:
            click.echo(f"Error: {result['error']}", err=True)
        
        # Show failed steps
        failed_steps = [s for s in result['steps'] if not s['success']]
        if failed_steps:
            click.echo("\nFailed Steps:")
            for step in failed_steps:
                click.echo(f"  Step {step['step']} ({step['action']}): {step['error']}")
        
        click.echo("="*60)
        
        # Save results if output specified
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            click.echo(f"\nResults saved to: {output}")
        
        # Exit with appropriate code
        sys.exit(0 if result['status'] == 'success' else 1)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        logging.exception("Execution failed")
        sys.exit(1)


@cli.command()
@click.option('--app-path', '-a', required=True, help='Path to application executable')
@click.option('--server-url', default='http://127.0.0.1:4723', 
              help='WinAppDriver server URL')
def inspect(app_path: str, server_url: str):
    """
    Launch application in inspect mode.
    Use Windows Inspect.exe to explore UI elements.
    
    Example:
        python main.py inspect --app-path "C:\\Windows\\System32\\calc.exe"
    """
    try:
        click.echo(f"Starting application: {app_path}")
        click.echo(f"Server URL: {server_url}")
        click.echo("\nUse Windows Inspect.exe to explore UI elements.")
        click.echo("Press Ctrl+C to stop...\n")
        
        controller = WinAppDriverController(server_url=server_url)
        controller.start_app(app_path)
        
        click.echo("Application started. Use Inspect.exe to explore elements.")
        click.echo("Window title: " + controller.get_window_title())
        
        # Keep alive
        input("\nPress Enter to stop application...")
        
        controller.stop_app()
        click.echo("Application stopped.")
        
    except KeyboardInterrupt:
        click.echo("\nStopping application...")
        if controller:
            controller.stop_app()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        logging.exception("Inspect mode failed")
        sys.exit(1)


@cli.command()
@click.option('--scripts-dir', '-d', default='examples', 
              help='Directory containing scripts')
@click.option('--config', '-c', help='Path to configuration file')
@click.option('--server-url', default='http://127.0.0.1:4723', 
              help='WinAppDriver server URL')
@click.option('--output-dir', '-o', default='results', 
              help='Output directory for results')
def batch(scripts_dir: str, config: Optional[str], server_url: str, output_dir: str):
    """
    Run multiple scripts in batch mode.
    
    Example:
        python main.py batch --scripts-dir examples
    """
    try:
        scripts_path = Path(scripts_dir)
        if not scripts_path.exists():
            click.echo(f"Error: Directory not found: {scripts_dir}", err=True)
            sys.exit(1)
        
        # Find all YAML scripts
        script_files = list(scripts_path.glob("*.yaml")) + list(scripts_path.glob("*.yml"))
        
        if not script_files:
            click.echo(f"No script files found in: {scripts_dir}")
            sys.exit(1)
        
        click.echo(f"Found {len(script_files)} script(s)")
        
        # Load configuration
        config_dict = load_config(config)
        if server_url:
            config_dict.setdefault('winappdriver', {})['server_url'] = server_url
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Execute scripts
        results = []
        for i, script_file in enumerate(script_files, 1):
            click.echo(f"\n[{i}/{len(script_files)}] Executing: {script_file.name}")
            
            try:
                server = config_dict.get('winappdriver', {}).get('server_url', server_url)
                implicit_wait = config_dict.get('winappdriver', {}).get('implicit_wait', 10)
                
                controller = WinAppDriverController(server_url=server, implicit_wait=implicit_wait)
                executor = ScriptExecutor(controller, config_dict)
                
                result = executor.execute_script_file(str(script_file))
                results.append(result)
                
                status_icon = "✓" if result['status'] == 'success' else "✗"
                click.echo(f"{status_icon} {result['name']}: {result['status']} ({result['duration']:.2f}s)")
                
            except Exception as e:
                click.echo(f"✗ Error executing {script_file.name}: {e}", err=True)
                results.append({
                    'name': script_file.name,
                    'status': 'error',
                    'error': str(e)
                })
        
        # Summary
        click.echo("\n" + "="*60)
        click.echo("BATCH EXECUTION SUMMARY")
        click.echo("="*60)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        click.echo(f"Total scripts: {len(results)}")
        click.echo(f"Success: {success_count}")
        click.echo(f"Failed: {len(results) - success_count}")
        
        # Save results
        summary_file = output_path / f"batch_results_{Path(scripts_dir).name}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        click.echo(f"\nResults saved to: {summary_file}")
        
        # Exit with appropriate code
        sys.exit(0 if success_count == len(results) else 1)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        logging.exception("Batch execution failed")
        sys.exit(1)


@cli.command()
def version():
    """Display version information."""
    click.echo("WinAppDriver Automation Framework")
    click.echo("Version: 1.0.0")
    click.echo("\nDependencies:")
    
    try:
        import appium
        click.echo(f"  - Appium-Python-Client: {appium.__version__}")
    except ImportError:
        click.echo("  - Appium-Python-Client: Not installed")
    
    try:
        import selenium
        click.echo(f"  - Selenium: {selenium.__version__}")
    except ImportError:
        click.echo("  - Selenium: Not installed")
    
    click.echo(f"  - Click: {click.__version__}")
    click.echo(f"  - PyYAML: installed")


if __name__ == '__main__':
    cli()
