"""Auto-paste functionality with clipboard management."""
import time
import pyautogui
import pyperclip
from typing import Optional
from logger import logger


class AutoPaste:
    """Handles automatic pasting of AI responses."""
    
    def __init__(self, delay_ms: int = 500, restore_clipboard: bool = False):
        """Initialize auto-paste handler.
        
        Args:
            delay_ms: Delay before pasting in milliseconds
            restore_clipboard: Whether to restore original clipboard after paste
        """
        self.delay_ms = delay_ms
        self.restore_clipboard = restore_clipboard
        
        # Disable pyautogui fail-safe (can interfere with automation)
        pyautogui.FAILSAFE = False
    
    def paste_text(self, text: str) -> bool:
        """Paste text at current cursor position.
        
        Args:
            text: Text to paste
            
        Returns:
            True if successful, False otherwise
        """
        original_clipboard = None
        
        try:
            # Store original clipboard content if needed
            if self.restore_clipboard:
                try:
                    original_clipboard = pyperclip.paste()
                except Exception as e:
                    logger.warning(f"Could not read original clipboard: {e}")
            
            # Copy AI response to clipboard
            pyperclip.copy(text)
            logger.info(f"Copied {len(text)} characters to clipboard")
            
            # Wait for specified delay
            time.sleep(self.delay_ms / 1000.0)
            
            # Simulate Ctrl+V keypress
            pyautogui.hotkey('ctrl', 'v')
            logger.info("Paste command sent")
            
            # Small delay to ensure paste completes
            time.sleep(0.1)
            
            # Restore original clipboard if needed
            if self.restore_clipboard and original_clipboard is not None:
                time.sleep(0.2)  # Wait a bit before restoring
                pyperclip.copy(original_clipboard)
                logger.info("Original clipboard restored")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to paste text: {e}")
            return False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard without pasting.
        
        Args:
            text: Text to copy
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pyperclip.copy(text)
            logger.info(f"Copied {len(text)} characters to clipboard")
            return True
        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {e}")
            return False
    
    def set_delay(self, delay_ms: int) -> None:
        """Update paste delay.
        
        Args:
            delay_ms: New delay in milliseconds
        """
        self.delay_ms = delay_ms
        logger.info(f"Paste delay updated to {delay_ms}ms")
    
    def set_restore_clipboard(self, restore: bool) -> None:
        """Update clipboard restore setting.
        
        Args:
            restore: Whether to restore clipboard
        """
        self.restore_clipboard = restore
        logger.info(f"Restore clipboard: {restore}")
