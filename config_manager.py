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
            self.config = self.get_defaults()
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
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "hotkey": "ctrl+shift+alt+a",         # Main analysis hotkey
            "capture_hotkey": "ctrl+shift+alt+c", # New: Capture-only hotkey
            "gemini": {
                "api_keys": [],
                "current_key_index": 0,
                "auto_rotate_on_quota_error": True,
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
        """Get configured main analysis hotkey."""
        return self.get('hotkey', 'ctrl+shift+alt+a')
    
    def get_capture_hotkey(self) -> str:
        """Get configured capture-only hotkey."""
        return self.get('capture_hotkey', 'ctrl+shift+alt+c')
    
    def get_system_prompt(self) -> str:
        """Get AI system prompt."""
        return self.get('gemini.system_prompt', '')
    
    def get_api_key(self) -> str:
        """Get current active API key."""
        keys = self.get('gemini.api_keys', [])
        if not keys:
            return ''
        index = self.get('gemini.current_key_index', 0)
        if index >= len(keys):
            index = 0
            self.set('gemini.current_key_index', 0)
        return keys[index]
    
    def get_all_api_keys(self) -> list:
        """Get all configured API keys."""
        return self.get('gemini.api_keys', [])
    
    def add_api_key(self, api_key: str) -> None:
        """Add a new API key to the rotation list.
        
        Args:
            api_key: API key to add
        """
        keys = self.get_all_api_keys()
        if api_key and api_key not in keys:
            keys.append(api_key)
            self.set('gemini.api_keys', keys)
    
    def remove_api_key(self, api_key: str) -> None:
        """Remove an API key from the rotation list.
        
        Args:
            api_key: API key to remove
        """
        keys = self.get_all_api_keys()
        if api_key in keys:
            keys.remove(api_key)
            self.set('gemini.api_keys', keys)
            # Reset index if needed
            current_index = self.get('gemini.current_key_index', 0)
            if current_index >= len(keys):
                self.set('gemini.current_key_index', 0)
    
    def rotate_to_next_key(self) -> str:
        """Rotate to the next API key in the list.
        
        Returns:
            The new current API key
        """
        keys = self.get_all_api_keys()
        if len(keys) <= 1:
            return self.get_api_key()
        
        current_index = self.get('gemini.current_key_index', 0)
        next_index = (current_index + 1) % len(keys)
        self.set('gemini.current_key_index', next_index)
        
        return keys[next_index]
    
    def is_auto_rotate_enabled(self) -> bool:
        """Check if automatic rotation on quota error is enabled."""
        return self.get('gemini.auto_rotate_on_quota_error', True)
    
    def is_auto_paste_enabled(self) -> bool:
        """Check if auto-paste is enabled."""
        return self.get('auto_paste.enabled', True)
    
    def get_paste_delay(self) -> int:
        """Get paste delay in milliseconds."""
        return self.get('auto_paste.delay_ms', 500)
