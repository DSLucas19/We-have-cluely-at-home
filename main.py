"""
AI Assistant - Background Screenshot Analysis Application

A system tray application that captures screenshots via global hotkeys,
analyzes them with Gemini AI, and auto-pastes solutions.
"""
import os
import sys
import asyncio
import threading
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import ConfigManager
from logger import setup_logger, logger
from screenshot_capture import ScreenshotCapture
from gemini_integration import GeminiIntegration
from auto_paste import AutoPaste
from hotkey_listener import HotkeyListener
from system_tray import SystemTray
from startup_manager import StartupManager
from settings_window import SettingsWindow


class AIAssistant:
    """Main application orchestrating all components."""
    
    def __init__(self):
        """Initialize AI Assistant application."""
        # Change to application directory
        os.chdir(Path(__file__).parent)
        
        # Initialize components
        self.config = ConfigManager()
        
        # Setup logger
        log_level = self.config.get('logging.level', 'INFO')
        save_logs = self.config.get('logging.save_logs', True)
        global logger
        logger = setup_logger(log_level=log_level, save_logs=save_logs)
        
        logger.info("="*50)
        logger.info("AI Assistant Starting...")
        logger.info("="*50)
        
        # Initialize screenshot capture
        save_screenshots = self.config.get('screenshot.save_to_disk', False)
        self.screenshot = ScreenshotCapture(save_to_disk=save_screenshots)
        
        # Initialize Gemini with config manager for key rotation
        model = self.config.get('gemini.model', 'gemini-3-flash-preview')
        self.gemini = GeminiIntegration(self.config, model)
        
        # Initialize auto-paste
        paste_delay = self.config.get_paste_delay()
        restore_clipboard = self.config.get('auto_paste.restore_clipboard', False)
        self.auto_paste = AutoPaste(delay_ms=paste_delay, restore_clipboard=restore_clipboard)
        
        # Initialize hotkey listener
        self.hotkey_listener = HotkeyListener()
        
        # Initialize system tray
        self.system_tray = SystemTray(
            on_toggle=self.on_toggle,
            on_settings=self.on_settings,
            on_exit=self.on_exit
        )
        
        # Initialize startup manager
        self.startup_manager = StartupManager()
        
        # State
        self.is_enabled = True
        self.is_processing = False
        
        # Register hotkey
        self._register_hotkey()
        
        # Update system tray with hotkey
        self.system_tray.update_hotkey_display(self.config.get_hotkey())
        
        # Check and apply startup setting
        startup_enabled = self.config.get('startup.launch_on_boot', False)
        if startup_enabled and not self.startup_manager.is_enabled():
            self.startup_manager.enable()
        elif not startup_enabled and self.startup_manager.is_enabled():
            self.startup_manager.disable()
        
        logger.info("AI Assistant initialized successfully")
    
    def _register_hotkey(self) -> None:
        """Register global hotkey with listener."""
        hotkey = self.config.get_hotkey()
        
        if self.hotkey_listener.register(hotkey, self.on_hotkey_pressed):
            logger.info(f"Hotkey registered: {hotkey}")
        else:
            logger.error(f"Failed to register hotkey: {hotkey}")
    
    def on_hotkey_pressed(self) -> None:
        """Handle hotkey press event."""
        if not self.is_enabled:
            logger.info("Hotkey pressed but assistant is disabled")
            return
        
        if self.is_processing:
            logger.info("Already processing a request, ignoring hotkey")
            return
        
        logger.info("Hotkey pressed! Starting capture and analysis...")
        
        # Run async processing in a new thread to avoid blocking
        thread = threading.Thread(target=self._process_screenshot, daemon=True)
        thread.start()
    
    def _process_screenshot(self) -> None:
        """Process screenshot (capture, analyze, paste)."""
        try:
            self.is_processing = True
            
            # 1. Capture screenshot
            logger.info("Capturing screenshot...")
            image = self.screenshot.capture_full_screen()
            
            # 2. Analyze with Gemini
            logger.info("Analyzing with Gemini...")
            prompt = self.config.get_system_prompt()
            response = self.gemini.analyze_screenshot_sync(image, prompt)
            
            logger.info(f"Received response: {response[:100]}...")
            
            # 3. Auto-paste or copy to clipboard
            if self.config.is_auto_paste_enabled():
                logger.info("Auto-pasting response...")
                if self.auto_paste.paste_text(response):
                    self.system_tray.show_notification(
                        "AI Assistant",
                        "Response pasted!"
                    )
                else:
                    # Fallback to clipboard
                    self.auto_paste.copy_to_clipboard(response)
                    self.system_tray.show_notification(
                        "AI Assistant",
                        "Response copied to clipboard"
                    )
            else:
                logger.info("Copying to clipboard...")
                self.auto_paste.copy_to_clipboard(response)
                self.system_tray.show_notification(
                    "AI Assistant",
                    "Response copied to clipboard"
                )
            
        except Exception as e:
            logger.error(f"Error processing screenshot: {e}")
            self.system_tray.show_notification(
                "AI Assistant Error",
                f"Failed: {str(e)[:50]}"
            )
        finally:
            self.is_processing = False
    
    def on_toggle(self, enabled: bool) -> None:
        """Handle enable/disable toggle from system tray.
        
        Args:
            enabled: New enabled state
        """
        self.is_enabled = enabled
        
        if enabled:
            self.hotkey_listener.enable()
        else:
            self.hotkey_listener.disable()
        
        logger.info(f"Assistant {'enabled' if enabled else 'disabled'}")
    
    def on_settings(self) -> None:
        """Handle settings menu click."""
        logger.info("Opening settings window...")
        
        # Create and show settings window in a new thread
        def show_settings():
            settings = SettingsWindow(
                config_manager=self.config,
                on_save=self.on_settings_saved,
                on_test_capture=self.on_test_capture
            )
            settings.show()
            settings.run()
        
        thread = threading.Thread(target=show_settings, daemon=True)
        thread.start()
    
    def on_settings_saved(self) -> None:
        """Handle settings saved event."""
        logger.info("Settings saved, reloading configuration...")
        
        # Note: Full reload would require restart
        # For now, just log
        logger.info("Please restart the application for changes to take effect")
    
    def on_test_capture(self) -> None:
        """Handle test capture button click."""
        try:
            logger.info("Test capture initiated...")
            
            # Temporarily enable saving to disk
            original_save = self.screenshot.save_to_disk
            self.screenshot.save_to_disk = True
            
            # Capture screenshot
            image = self.screenshot.capture_full_screen()
            
            # Restore original setting
            self.screenshot.save_to_disk = original_save
            
            logger.info("Test capture completed successfully")
            
        except Exception as e:
            logger.error(f"Test capture failed: {e}")
    
    def on_exit(self) -> None:
        """Handle exit from system tray."""
        logger.info("Shutting down AI Assistant...")
        
        # Unregister hotkey
        self.hotkey_listener.unregister()
        
        # Exit
        sys.exit(0)
    
    def run(self) -> None:
        """Run the application."""
        logger.info("Starting system tray...")
        
        try:
            # Run system tray (blocking)
            self.system_tray.run()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            self.on_exit()
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise


def main():
    """Main entry point."""
    try:
        app = AIAssistant()
        app.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
