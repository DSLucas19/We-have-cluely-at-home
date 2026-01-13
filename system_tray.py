"""System tray integration for AI Assistant."""
import os
import pystray
from PIL import Image
from typing import Callable, Optional
from logger import logger


class SystemTray:
    """Manages system tray icon and menu."""
    
    def __init__(
        self,
        on_toggle: Optional[Callable] = None,
        on_settings: Optional[Callable] = None,
        on_exit: Optional[Callable] = None
    ):
        """Initialize system tray.
        
        Args:
            on_toggle: Callback for enable/disable toggle
            on_settings: Callback for settings menu item
            on_exit: Callback for exit menu item
        """
        self.on_toggle = on_toggle
        self.on_settings = on_settings
        self.on_exit = on_exit
        
        self.icon: Optional[pystray.Icon] = None
        self.is_enabled = True
        self.hotkey_text = "Ctrl+Shift+Alt+A"
        
        # Load icons
        self.icon_enabled = self._load_icon("assets/icon.png")
        self.icon_disabled = self._load_icon("assets/icon_disabled.png")
    
    def _load_icon(self, path: str) -> Image.Image:
        """Load icon from file or create default.
        
        Args:
            path: Path to icon file
            
        Returns:
            PIL Image object
        """
        try:
            if os.path.exists(path):
                return Image.open(path)
            else:
                logger.warning(f"Icon not found: {path}, using default")
                # Create a simple default icon (blue circle)
                img = Image.new('RGB', (64, 64), color=(70, 130, 180))
                return img
        except Exception as e:
            logger.error(f"Error loading icon: {e}")
            # Return a simple colored square as fallback
            return Image.new('RGB', (64, 64), color=(70, 130, 180))
    
    def _create_menu(self) -> pystray.Menu:
        """Create system tray menu.
        
        Returns:
            pystray Menu object
        """
        return pystray.Menu(
            pystray.MenuItem(
                lambda text: f"{'✓' if self.is_enabled else '✗'} AI Assistant",
                lambda: None,
                enabled=False
            ),
            pystray.MenuItem(
                lambda text: f"Hotkey: {self.hotkey_text}",
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                lambda text: f"{'Disable' if self.is_enabled else 'Enable'} Assistant",
                self._handle_toggle
            ),
            pystray.MenuItem(
                "Settings...",
                self._handle_settings
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Exit",
                self._handle_exit
            )
        )
    
    def _handle_toggle(self, icon, item) -> None:
        """Handle enable/disable toggle."""
        self.is_enabled = not self.is_enabled
        
        # Update icon
        icon.icon = self.icon_enabled if self.is_enabled else self.icon_disabled
        
        # Update tooltip
        status = "Enabled" if self.is_enabled else "Disabled"
        icon.title = f"AI Assistant - {status}"
        
        # Call callback
        if self.on_toggle:
            self.on_toggle(self.is_enabled)
        
        logger.info(f"AI Assistant {'enabled' if self.is_enabled else 'disabled'}")
        
        # Update menu
        icon.update_menu()
    
    def _handle_settings(self, icon, item) -> None:
        """Handle settings menu click."""
        if self.on_settings:
            self.on_settings()
    
    def _handle_exit(self, icon, item) -> None:
        """Handle exit menu click."""
        logger.info("Exiting AI Assistant")
        
        # Call exit callback first
        if self.on_exit:
            self.on_exit()
        
        # Stop the icon
        icon.stop()
    
    def run(self) -> None:
        """Run the system tray icon (blocking)."""
        try:
            self.icon = pystray.Icon(
                "ai_assistant",
                self.icon_enabled,
                "AI Assistant - Enabled",
                menu=self._create_menu()
            )
            
            logger.info("System tray icon started")
            self.icon.run()
            
        except Exception as e:
            logger.error(f"Error running system tray: {e}")
            raise
    
    def run_detached(self) -> None:
        """Run system tray in a separate thread (non-blocking)."""
        try:
            self.icon = pystray.Icon(
                "ai_assistant",
                self.icon_enabled,
                "AI Assistant - Enabled",
                menu=self._create_menu()
            )
            
            # Run in detached mode
            self.icon.run_detached()
            logger.info("System tray icon started (detached)")
            
        except Exception as e:
            logger.error(f"Error running system tray: {e}")
            raise
    
    def stop(self) -> None:
        """Stop the system tray icon."""
        if self.icon:
            self.icon.stop()
            logger.info("System tray icon stopped")
    
    def update_hotkey_display(self, hotkey: str) -> None:
        """Update hotkey display in menu.
        
        Args:
            hotkey: Hotkey string to display
        """
        self.hotkey_text = hotkey
        if self.icon:
            self.icon.update_menu()
    
    def show_notification(self, title: str, message: str, duration: int = 3) -> None:
        """Show a system notification.
        
        Args:
            title: Notification title
            message: Notification message
            duration: Duration in seconds
        """
        if self.icon:
            try:
                self.icon.notify(message, title)
            except Exception as e:
                logger.warning(f"Could not show notification: {e}")
