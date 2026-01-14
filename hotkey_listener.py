"""Global hotkey listener for triggering AI assistant."""
import keyboard
from typing import Callable, Optional
from logger import logger


class HotkeyListener:
    """Manages global hotkey registration and callbacks."""
    
    def __init__(self):
        """Initialize hotkey listener."""
        # Use dictionary to support multiple hotkeys
        self.registered_hotkeys: dict[str, Callable] = {}
        self.is_enabled = False
        
        # Backward compatibility: track "main" hotkey
        self.current_hotkey: Optional[str] = None
        self.callback: Optional[Callable] = None
    
    def register(self, hotkey: str, callback: Callable, replace: bool = False) -> bool:
        """Register a global hotkey.
        
        Args:
            hotkey: Hotkey combination (e.g., 'ctrl+shift+alt+a')
            callback: Function to call when hotkey is pressed
            replace: If True, unregister all previous hotkeys (legacy behavior)
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Legacy mode: unregister all previous hotkeys
            if replace and self.registered_hotkeys:
                self.unregister()
            
            # Check if this specific hotkey is already registered
            if hotkey in self.registered_hotkeys:
                logger.warning(f"Hotkey '{hotkey}' already registered, replacing callback")
                keyboard.remove_hotkey(hotkey)
            
            # Register new hotkey
            keyboard.add_hotkey(hotkey, callback, suppress=False)
            
            # Store in dictionary
            self.registered_hotkeys[hotkey] = callback
            self.is_enabled = True
            
            # Backward compatibility: track as current hotkey
            self.current_hotkey = hotkey
            self.callback = callback
            
            logger.info(f"Hotkey registered: {hotkey}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register hotkey '{hotkey}': {e}")
            return False
    
    def unregister_hotkey(self, hotkey: str) -> None:
        """Unregister a specific hotkey.
        
        Args:
            hotkey: Hotkey combination to unregister
        """
        if hotkey in self.registered_hotkeys:
            try:
                keyboard.remove_hotkey(hotkey)
                del self.registered_hotkeys[hotkey]
                logger.info(f"Hotkey unregistered: {hotkey}")
                
                # Update current_hotkey if it was this one
                if self.current_hotkey == hotkey:
                    self.current_hotkey = None
                    self.callback = None
                    
            except Exception as e:
                logger.warning(f"Error unregistering hotkey '{hotkey}': {e}")
    
    def unregister(self) -> None:
        """Unregister all hotkeys."""
        for hotkey in list(self.registered_hotkeys.keys()):
            try:
                keyboard.remove_hotkey(hotkey)
                logger.info(f"Hotkey unregistered: {hotkey}")
            except Exception as e:
                logger.warning(f"Error unregistering hotkey '{hotkey}': {e}")
        
        self.registered_hotkeys.clear()
        self.current_hotkey = None
        self.callback = None
        self.is_enabled = False
    
    def enable(self) -> bool:
        """Enable all registered hotkeys (re-register with same callbacks)."""
        if not self.registered_hotkeys:
            logger.warning("Cannot enable: no hotkeys registered")
            return False
        
        if self.is_enabled:
            logger.info("Hotkeys already enabled")
            return True
        
        # Re-register all hotkeys
        success = True
        hotkeys_snapshot = dict(self.registered_hotkeys)  # Copy to avoid modification during iteration
        self.registered_hotkeys.clear()
        
        for hotkey, callback in hotkeys_snapshot.items():
            if not self.register(hotkey, callback):
                success = False
        
        return success
    
    def disable(self) -> None:
        """Disable all hotkeys temporarily (without unregistering)."""
        for hotkey in self.registered_hotkeys.keys():
            try:
                keyboard.remove_hotkey(hotkey)
            except Exception as e:
                logger.warning(f"Error disabling hotkey '{hotkey}': {e}")
        
        self.is_enabled = False
        logger.info("All hotkeys disabled")
    
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
