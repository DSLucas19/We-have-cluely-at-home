"""Configuration management for AI Assistant application."""
import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # Create default configuration
            self.config = self._get_defaults()
            self.save()
    
    def save(self) -> None:
        """Save configuration to file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'gemini.api_key')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'gemini.api_key')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        self.save()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "hotkey": "ctrl+shift+alt+a",
            "gemini": {
                "api_key": "",
                "model": "gemini-3-flash-preview",
                "system_prompt": "You are a helpful assistant. Analyze this screenshot and provide a concise solution. Be direct and actionable."
            },
            "auto_paste": {
                "enabled": True,
                "delay_ms": 500,
                "restore_clipboard": False
            },
            "screenshot": {
                "mode": "full_screen",
                "save_to_disk": False
            },
            "startup": {
                "launch_on_boot": False
            },
            "logging": {
                "level": "INFO",
                "save_logs": True
            }
        }
    
    def get_hotkey(self) -> str:
        """Get configured hotkey combination."""
        return self.get('hotkey', 'ctrl+shift+alt+a')
    
    def get_system_prompt(self) -> str:
        """Get AI system prompt."""
        return self.get('gemini.system_prompt', '')
    
    def get_api_key(self) -> str:
        """Get Gemini API key."""
        return self.get('gemini.api_key', '')
    
    def is_auto_paste_enabled(self) -> bool:
        """Check if auto-paste is enabled."""
        return self.get('auto_paste.enabled', True)
    
    def get_paste_delay(self) -> int:
        """Get paste delay in milliseconds."""
        return self.get('auto_paste.delay_ms', 500)
