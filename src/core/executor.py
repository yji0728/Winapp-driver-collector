"""
Script Executor - Executes automation scripts
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from .controller import WinAppDriverController

logger = logging.getLogger(__name__)


class ScriptExecutor:
    """
    Executes automation scripts defined in YAML format.
    """

    def __init__(self, controller: WinAppDriverController, config: Dict[str, Any] = None):
        """
        Initialize script executor.
        
        Args:
            controller: WinAppDriver controller instance
            config: Optional configuration dictionary
        """
        self.controller = controller
        self.config = config or {}
        self.results: List[Dict[str, Any]] = []
        logger.info("Initialized script executor")

    def load_script(self, script_path: str) -> Dict[str, Any]:
        """
        Load a script from YAML file.
        
        Args:
            script_path: Path to script file
            
        Returns:
            Script dictionary
        """
        try:
            logger.info(f"Loading script: {script_path}")
            with open(script_path, 'r', encoding='utf-8') as f:
                script = yaml.safe_load(f)
            logger.info(f"Script loaded: {script.get('name', 'Unnamed')}")
            return script
        except Exception as e:
            logger.error(f"Failed to load script: {e}")
            raise

    def execute_script(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an automation script.
        
        Args:
            script: Script dictionary
            
        Returns:
            Execution results
        """
        start_time = datetime.now()
        script_name = script.get('name', 'Unnamed Script')
        
        logger.info(f"=== Starting execution: {script_name} ===")
        
        result = {
            'name': script_name,
            'description': script.get('description', ''),
            'start_time': start_time.isoformat(),
            'steps': [],
            'status': 'success',
            'error': None
        }
        
        try:
            # Start application
            app_config = script.get('app', {})
            app_path = app_config.get('path')
            app_arguments = app_config.get('arguments', '')
            
            if not app_path:
                raise ValueError("Application path not specified in script")
            
            self.controller.start_app(app_path, app_arguments)
            
            # Execute steps
            steps = script.get('steps', [])
            for i, step in enumerate(steps):
                step_result = self._execute_step(step, i + 1)
                result['steps'].append(step_result)
                
                if not step_result['success']:
                    result['status'] = 'failed'
                    if step.get('continue_on_error', False):
                        logger.warning(f"Step failed but continuing: {step_result['error']}")
                    else:
                        logger.error(f"Step failed, stopping execution: {step_result['error']}")
                        break
            
        except Exception as e:
            logger.error(f"Script execution failed: {e}")
            result['status'] = 'error'
            result['error'] = str(e)
        
        finally:
            # Stop application
            try:
                self.controller.stop_app()
            except Exception as e:
                logger.warning(f"Error stopping application: {e}")
        
        end_time = datetime.now()
        result['end_time'] = end_time.isoformat()
        result['duration'] = (end_time - start_time).total_seconds()
        
        logger.info(f"=== Execution completed: {script_name} ({result['status']}) ===")
        
        self.results.append(result)
        return result

    def _execute_step(self, step: Dict[str, Any], step_number: int) -> Dict[str, Any]:
        """
        Execute a single step.
        
        Args:
            step: Step dictionary
            step_number: Step number
            
        Returns:
            Step result dictionary
        """
        action = step.get('action')
        logger.info(f"Step {step_number}: {action}")
        
        result = {
            'step': step_number,
            'action': action,
            'success': False,
            'error': None
        }
        
        try:
            if action == 'click':
                self._action_click(step)
            elif action == 'double_click':
                self._action_double_click(step)
            elif action == 'send_keys':
                self._action_send_keys(step)
            elif action == 'clear':
                self._action_clear(step)
            elif action == 'wait':
                self._action_wait(step)
            elif action == 'verify':
                self._action_verify(step)
            elif action == 'screenshot':
                self._action_screenshot(step)
            else:
                raise ValueError(f"Unknown action: {action}")
            
            result['success'] = True
            logger.info(f"Step {step_number} completed successfully")
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Step {step_number} failed: {e}")
        
        return result

    def _find_element(self, element_config: Dict[str, Any]):
        """Find element based on configuration."""
        element_type = element_config.get('type')
        element_value = element_config.get('value')
        timeout = element_config.get('timeout', 10)
        
        return self.controller.find_element(element_type, element_value, timeout)

    def _action_click(self, step: Dict[str, Any]) -> None:
        """Execute click action."""
        element = self._find_element(step['element'])
        self.controller.click(element)

    def _action_double_click(self, step: Dict[str, Any]) -> None:
        """Execute double-click action."""
        element = self._find_element(step['element'])
        self.controller.double_click(element)

    def _action_send_keys(self, step: Dict[str, Any]) -> None:
        """Execute send keys action."""
        element = self._find_element(step['element'])
        keys = step.get('keys', '')
        self.controller.send_keys(element, keys)

    def _action_clear(self, step: Dict[str, Any]) -> None:
        """Execute clear action."""
        element = self._find_element(step['element'])
        self.controller.clear(element)

    def _action_wait(self, step: Dict[str, Any]) -> None:
        """Execute wait action."""
        duration = step.get('duration', 1)
        self.controller.wait(duration)

    def _action_verify(self, step: Dict[str, Any]) -> None:
        """Execute verify action."""
        element = self._find_element(step['element'])
        expected = step.get('expected', '')
        
        if not self.controller.verify_element_text(element, expected):
            raise AssertionError(f"Verification failed: expected '{expected}'")

    def _action_screenshot(self, step: Dict[str, Any]) -> None:
        """Execute screenshot action."""
        filename = step.get('filename', f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        screenshots_dir = self.config.get('screenshots', {}).get('directory', 'screenshots')
        filepath = Path(screenshots_dir) / filename
        self.controller.screenshot(str(filepath))

    def execute_script_file(self, script_path: str) -> Dict[str, Any]:
        """
        Load and execute a script file.
        
        Args:
            script_path: Path to script file
            
        Returns:
            Execution results
        """
        script = self.load_script(script_path)
        return self.execute_script(script)

    def get_results(self) -> List[Dict[str, Any]]:
        """
        Get all execution results.
        
        Returns:
            List of result dictionaries
        """
        return self.results
