"""Windows startup management."""
import os
import sys
import winreg
from pathlib import Path
from logger import logger


class StartupManager:
    """Manages Windows startup registration."""
    
    def __init__(self, app_name: str = "AIAssistant"):
        """Initialize startup manager.
        
        Args:
            app_name: Application name for registry
        """
        self.app_name = app_name
        self.registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    def is_enabled(self) -> bool:
        """Check if application is set to run on startup.
        
        Returns:
            True if startup is enabled, False otherwise
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.registry_key,
                0,
                winreg.KEY_READ
            )
            
            try:
                value, _ = winreg.QueryValueEx(key, self.app_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
                
        except Exception as e:
            logger.error(f"Error checking startup status: {e}")
            return False
    
    def enable(self) -> bool:
        """Enable application to run on Windows startup.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get path to current executable or script
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                app_path = sys.executable
            else:
                # Running as Python script
                app_path = f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
            
            # Open registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.registry_key,
                0,
                winreg.KEY_WRITE
            )
            
            # Set value
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            
            logger.info(f"Startup enabled: {app_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error enabling startup: {e}")
            return False
    
    def disable(self) -> bool:
        """Disable application from running on Windows startup.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.registry_key,
                0,
                winreg.KEY_WRITE
            )
            
            try:
                winreg.DeleteValue(key, self.app_name)
                logger.info("Startup disabled")
            except FileNotFoundError:
                logger.info("Startup was already disabled")
            
            winreg.CloseKey(key)
            return True
            
        except Exception as e:
            logger.error(f"Error disabling startup: {e}")
            return False
    
    def toggle(self) -> bool:
        """Toggle startup setting.
        
        Returns:
            New state (True = enabled, False = disabled)
        """
        if self.is_enabled():
            self.disable()
            return False
        else:
            self.enable()
            return True
