"""
WinAppDriver Controller - Core automation controller
"""

import logging
import time
from typing import Optional, Dict, Any
from pathlib import Path

try:
    from appium import webdriver
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    # Graceful degradation if appium is not installed
    webdriver = None
    AppiumBy = None
    WebDriverWait = None
    EC = None
    TimeoutException = Exception
    NoSuchElementException = Exception

logger = logging.getLogger(__name__)


class WinAppDriverController:
    """
    Main controller for WinAppDriver automation.
    Provides high-level interface for Windows application automation.
    """

    def __init__(self, server_url: str = "http://127.0.0.1:4723", 
                 implicit_wait: int = 10):
        """
        Initialize WinAppDriver controller.
        
        Args:
            server_url: WinAppDriver server URL
            implicit_wait: Implicit wait time in seconds
        """
        if webdriver is None:
            raise ImportError(
                "Appium-Python-Client is not installed. "
                "Install it with: pip install Appium-Python-Client"
            )
        
        self.server_url = server_url
        self.implicit_wait = implicit_wait
        self.driver: Optional[Any] = None
        logger.info(f"Initialized WinAppDriver controller with server: {server_url}")

    def start_app(self, app_path: str, app_arguments: str = "") -> None:
        """
        Start the target application.
        
        Args:
            app_path: Full path to the application executable
            app_arguments: Optional command line arguments
        """
        desired_caps = {
            "app": app_path,
            "platformName": "Windows",
            "deviceName": "WindowsPC",
        }
        
        if app_arguments:
            desired_caps["appArguments"] = app_arguments
        
        try:
            logger.info(f"Starting application: {app_path}")
            self.driver = webdriver.Remote(
                command_executor=self.server_url,
                desired_capabilities=desired_caps
            )
            self.driver.implicitly_wait(self.implicit_wait)
            logger.info("Application started successfully")
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            raise

    def stop_app(self) -> None:
        """Stop the application and close the session."""
        if self.driver:
            try:
                logger.info("Stopping application")
                self.driver.quit()
                self.driver = None
                logger.info("Application stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping application: {e}")
                raise

    def find_element(self, by: str, value: str, timeout: int = 10):
        """
        Find an element using specified locator strategy.
        
        Args:
            by: Locator strategy (Name, AutomationId, ClassName, XPath, etc.)
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if found
        """
        if not self.driver:
            raise RuntimeError("Application not started. Call start_app() first.")
        
        locator_map = {
            "Name": AppiumBy.NAME,
            "AutomationId": AppiumBy.ACCESSIBILITY_ID,
            "ClassName": AppiumBy.CLASS_NAME,
            "XPath": AppiumBy.XPATH,
            "AccessibilityId": AppiumBy.ACCESSIBILITY_ID,
        }
        
        by_type = locator_map.get(by, by)
        
        try:
            logger.debug(f"Finding element by {by}='{value}'")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(
                EC.presence_of_element_located((by_type, value))
            )
            logger.debug(f"Element found: {by}='{value}'")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {timeout}s: {by}='{value}'")
            raise
        except Exception as e:
            logger.error(f"Error finding element: {e}")
            raise

    def click(self, element) -> None:
        """
        Click on an element.
        
        Args:
            element: WebElement to click
        """
        try:
            logger.debug("Clicking element")
            element.click()
            logger.debug("Element clicked successfully")
        except Exception as e:
            logger.error(f"Error clicking element: {e}")
            raise

    def double_click(self, element) -> None:
        """
        Double-click on an element.
        
        Args:
            element: WebElement to double-click
        """
        try:
            logger.debug("Double-clicking element")
            self.driver.execute_script("mobile: doubleClick", {"element": element})
            logger.debug("Element double-clicked successfully")
        except Exception as e:
            logger.error(f"Error double-clicking element: {e}")
            raise

    def send_keys(self, element, keys: str) -> None:
        """
        Send keys to an element.
        
        Args:
            element: WebElement to send keys to
            keys: Text to send
        """
        try:
            logger.debug(f"Sending keys: '{keys}'")
            element.send_keys(keys)
            logger.debug("Keys sent successfully")
        except Exception as e:
            logger.error(f"Error sending keys: {e}")
            raise

    def clear(self, element) -> None:
        """
        Clear an input element.
        
        Args:
            element: WebElement to clear
        """
        try:
            logger.debug("Clearing element")
            element.clear()
            logger.debug("Element cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing element: {e}")
            raise

    def get_text(self, element) -> str:
        """
        Get text from an element.
        
        Args:
            element: WebElement to get text from
            
        Returns:
            Element text
        """
        try:
            text = element.text
            logger.debug(f"Got text: '{text}'")
            return text
        except Exception as e:
            logger.error(f"Error getting text: {e}")
            raise

    def get_attribute(self, element, attribute: str) -> str:
        """
        Get an attribute value from an element.
        
        Args:
            element: WebElement to get attribute from
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        try:
            value = element.get_attribute(attribute)
            logger.debug(f"Got attribute '{attribute}': '{value}'")
            return value
        except Exception as e:
            logger.error(f"Error getting attribute: {e}")
            raise

    def screenshot(self, filename: str) -> bool:
        """
        Take a screenshot and save to file.
        
        Args:
            filename: Path to save screenshot
            
        Returns:
            True if successful
        """
        if not self.driver:
            raise RuntimeError("Application not started. Call start_app() first.")
        
        try:
            logger.info(f"Taking screenshot: {filename}")
            # Ensure directory exists
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            result = self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return result
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            raise

    def wait(self, duration: float) -> None:
        """
        Wait for specified duration.
        
        Args:
            duration: Time to wait in seconds
        """
        logger.debug(f"Waiting for {duration} seconds")
        time.sleep(duration)

    def verify_element_text(self, element, expected_text: str) -> bool:
        """
        Verify element text matches expected value.
        
        Args:
            element: WebElement to verify
            expected_text: Expected text value
            
        Returns:
            True if text matches
        """
        actual_text = self.get_text(element)
        matches = expected_text in actual_text
        
        if matches:
            logger.info(f"Verification passed: '{expected_text}' found in '{actual_text}'")
        else:
            logger.warning(f"Verification failed: '{expected_text}' not in '{actual_text}'")
        
        return matches

    def is_element_displayed(self, element) -> bool:
        """
        Check if element is displayed.
        
        Args:
            element: WebElement to check
            
        Returns:
            True if element is displayed
        """
        try:
            return element.is_displayed()
        except Exception:
            return False

    def is_element_enabled(self, element) -> bool:
        """
        Check if element is enabled.
        
        Args:
            element: WebElement to check
            
        Returns:
            True if element is enabled
        """
        try:
            return element.is_enabled()
        except Exception:
            return False

    def get_window_title(self) -> str:
        """
        Get the current window title.
        
        Returns:
            Window title
        """
        if not self.driver:
            raise RuntimeError("Application not started. Call start_app() first.")
        
        try:
            title = self.driver.title
            logger.debug(f"Window title: '{title}'")
            return title
        except Exception as e:
            logger.error(f"Error getting window title: {e}")
            raise
