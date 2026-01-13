"""Global hotkey listener for triggering AI assistant."""
import keyboard
from typing import Callable, Optional
from logger import logger


class HotkeyListener:
    """Manages global hotkey registration and callbacks."""
    
    def __init__(self):
        """Initialize hotkey listener."""
        self.current_hotkey: Optional[str] = None
        self.callback: Optional[Callable] = None
        self.is_enabled = False
    
    def register(self, hotkey: str, callback: Callable) -> bool:
        """Register a global hotkey.
        
        Args:
            hotkey: Hotkey combination (e.g., 'ctrl+shift+alt+a')
            callback: Function to call when hotkey is pressed
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Unregister previous hotkey if exists
            if self.current_hotkey:
                self.unregister()
            
            # Register new hotkey
            keyboard.add_hotkey(hotkey, callback, suppress=False)
            
            self.current_hotkey = hotkey
            self.callback = callback
            self.is_enabled = True
            
            logger.info(f"Hotkey registered: {hotkey}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register hotkey '{hotkey}': {e}")
            return False
    
    def unregister(self) -> None:
        """Unregister current hotkey."""
        if self.current_hotkey:
            try:
                keyboard.remove_hotkey(self.current_hotkey)
                logger.info(f"Hotkey unregistered: {self.current_hotkey}")
            except Exception as e:
                logger.warning(f"Error unregistering hotkey: {e}")
            
            self.current_hotkey = None
            self.callback = None
            self.is_enabled = False
    
    def enable(self) -> bool:
        """Enable hotkey (re-register with same callback)."""
        if not self.current_hotkey or not self.callback:
            logger.warning("Cannot enable: no hotkey registered")
            return False
        
        if self.is_enabled:
            logger.info("Hotkey already enabled")
            return True
        
        return self.register(self.current_hotkey, self.callback)
    
    def disable(self) -> None:
        """Disable hotkey temporarily (without unregistering)."""
        if self.current_hotkey:
            try:
                keyboard.remove_hotkey(self.current_hotkey)
                self.is_enabled = False
                logger.info("Hotkey disabled")
            except Exception as e:
                logger.warning(f"Error disabling hotkey: {e}")
    
    def is_hotkey_valid(self, hotkey: str) -> bool:
        """Check if hotkey string is valid.
        
        Args:
            hotkey: Hotkey string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Try parsing the hotkey
            keyboard.parse_hotkey(hotkey)
            return True
        except Exception:
            return False
    
    def get_current_hotkey(self) -> Optional[str]:
        """Get currently registered hotkey.
        
        Returns:
            Current hotkey string or None
        """
        return self.current_hotkey
    
    def wait(self) -> None:
        """Block and wait for hotkey events.
        
        Note: This is a blocking call. Use in main thread.
        """
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            logger.info("Hotkey listener stopped")
            self.unregister()
