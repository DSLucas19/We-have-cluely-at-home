"""Settings window for configuring AI Assistant with multi-API key support."""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Callable, Optional
from logger import logger


class Settings Window:
    """GUI window for application settings including multiple API keys."""
    
    def __init__(
        self,
        config_manager,
        on_save: Optional[Callable] = None,
        on_test_capture: Optional[Callable] = None
    ):
        """Initialize settings window.
        
        Args:
            config_manager: ConfigManager instance
            on_save: Callback when settings are saved
            on_test_capture: Callback for test capture button
        """
        self.config = config_manager
        self.on_save = on_save
        self.on_test_capture = on_test_capture
        
        self.window: Optional[tk.Tk] = None
        self.is_recording_hotkey = False
    
    def show(self) -> None:
        """Show settings window."""
        if self.window is not None:
            # Window already exists, just focus it
            self.window.lift()
            self.window.focus_force()
            return
        
        self._create_window()
    
    def _create_window(self) -> None:
        """Create and configure the settings window."""
        self.window = tk.Tk()
        self.window.title("AI Assistant Settings")
        self.window.geometry("550x700")
        self.window.resizable(False, False)
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        row = 0
        
        # Hotkey Section
        ttk.Label(main_frame, text="Hotkey Configuration", font=('', 10, 'bold')).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        ttk.Label(main_frame, text="Hotkey:").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        hotkey_frame = ttk.Frame(main_frame)
        hotkey_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.hotkey_var = tk.StringVar(value=self.config.get_hotkey())
        self.hotkey_entry = ttk.Entry(hotkey_frame, textvariable=self.hotkey_var, width=25)
        self.hotkey_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        self.record_btn = ttk.Button(hotkey_frame, text="Record", command=self._record_hotkey)
        self.record_btn.pack(side=tk.LEFT)
        
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15
        )
        row += 1
        
        # Gemini API Section
        ttk.Label(main_frame, text="Gemini API Configuration", font=('', 10, 'bold')).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        # API Keys List
        ttk.Label(main_frame, text="API Keys:", font=('', 9)).grid(
            row=row, column=0, sticky=tk.NW, pady=5
        )
        
        keys_frame = ttk.Frame(main_frame)
        keys_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Listbox for API keys
        self.keys_listbox = tk.Listbox(keys_frame, height=4, width=40)
        self.keys_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Load existing keys
        for key in self.config.get_all_api_keys():
            masked_key = key[:10] + "..." + key[-4:] if len(key) > 14 else key
            self.keys_listbox.insert(tk.END, masked_key)
            self.keys_listbox.itemconfig(tk.END, {'fg': 'gray'})
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(keys_frame, orient=tk.VERTICAL, command=self.keys_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.keys_listbox.config(yscrollcommand=scrollbar.set)
        
        row += 1
        
        # Buttons for key management
        key_buttons_frame = ttk.Frame(main_frame)
        key_buttons_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(key_buttons_frame, text="Add Key", command=self._add_key).pack(side=tk.LEFT, padx=2)
        ttk.Button(key_buttons_frame, text="Remove", command=self._remove_key).pack(side=tk.LEFT, padx=2)
        ttk.Button(key_buttons_frame, text="Test", command=self._test_api).pack(side=tk.LEFT, padx=2)
        
        row += 1
        
        # Auto-rotation checkbox
        self.auto_rotate_var = tk.BooleanVar(value=self.config.is_auto_rotate_enabled())
        ttk.Checkbutton(
            main_frame,
            text="Auto-rotate keys on quota error",
            variable=self.auto_rotate_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Current key indicator
        current_index = self.config.get('gemini.current_key_index', 0)
        ttk.Label(
            main_frame,
            text=f"Current active key: #{current_index + 1}",
            font=('', 8),
            foreground='blue'
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15
        )
        row += 1
        
        # System Prompt
        ttk.Label(main_frame, text="System Prompt:", font=('', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.NW, pady=5
        )
        row += 1
        
        self.prompt_text = scrolledtext.ScrolledText(main_frame, height=4, width=50, wrap=tk.WORD)
        self.prompt_text.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.prompt_text.insert('1.0', self.config.get_system_prompt())
        
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15
        )
        row += 1
        
        # Options Section
        ttk.Label(main_frame, text="Options", font=('', 10, 'bold')).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        row += 1
        
        self.auto_paste_var = tk.BooleanVar(value=self.config.is_auto_paste_enabled())
        ttk.Checkbutton(
            main_frame,
            text="Auto-paste response",
            variable=self.auto_paste_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.startup_var = tk.BooleanVar(value=self.config.get('startup.launch_on_boot', False))
        ttk.Checkbutton(
            main_frame,
            text="Launch on Windows startup",
            variable=self.startup_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.restore_clipboard_var = tk.BooleanVar(value=self.config.get('auto_paste.restore_clipboard', False))
        ttk.Checkbutton(
            main_frame,
            text="Restore clipboard after paste",
            variable=self.restore_clipboard_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Paste Delay
        ttk.Label(main_frame, text="Paste delay (ms):").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        self.delay_var = tk.IntVar(value=self.config.get_paste_delay())
        delay_spinbox = ttk.Spinbox(
            main_frame,
            from_=0,
            to=5000,
            increment=100,
            textvariable=self.delay_var,
            width=10
        )
        delay_spinbox.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15
        )
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(button_frame, text="Save", command=self._save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._close_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test Capture", command=self._test_capture).pack(side=tk.LEFT, padx=5)
        
        # Configure column weights
        main_frame.columnconfigure(1, weight=1)
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self._close_window)
        
        logger.info("Settings window opened")
    
    def _add_key(self) -> None:
        """Add a new API key."""
        dialog = tk.Toplevel(self.window)
        dialog.title("Add API Key")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Enter your Gemini API key:").pack(pady=10)
        
        key_entry = ttk.Entry(dialog, show="•", width=50)
        key_entry.pack(pady=5)
        key_entry.focus()
        
        def save_key():
            api_key = key_entry.get().strip()
            if not api_key:
                messagebox.showwarning("Empty Key", "Please enter an API key.")
                return
            
            # Check for duplicates
            if api_key in self.config.get_all_api_keys():
                messagebox.showinfo("Duplicate", "This API key already exists.")
                dialog.destroy()
                return
            
            # Add to listbox
            masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else api_key
            self.keys_listbox.insert(tk.END, masked_key)
            
            # Store the full key temporarily (will be saved when settings are saved)
            if not hasattr(self, 'temp_keys'):
                self.temp_keys = list(self.config.get_all_api_keys())
            self.temp_keys.append(api_key)
            
            messagebox.showinfo("Success", "API key added! Don't forget to click 'Save' to apply changes.")
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=save_key).pack(pady=10)
        
        # Bind Enter key
        key_entry.bind('<Return>', lambda e: save_key())
    
    def _remove_key(self) -> None:
        """Remove selected API key."""
        selection = self.keys_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an API key to remove.")
            return
        
        index = selection[0]
        
        if messagebox.askyesno("Confirm", "Remove this API key?"):
            self.keys_listbox.delete(index)
            
            # Remove from temp storage
            if not hasattr(self, 'temp_keys'):
                self.temp_keys = list(self.config.get_all_api_keys())
            if index < len(self.temp_keys):
                self.temp_keys.pop(index)
    
    def _record_hotkey(self) -> None:
        """Record hotkey from keyboard input."""
        messagebox.showinfo(
            "Record Hotkey",
            "Hotkey recording is a future feature.\n\n"
            "For now, please type the hotkey manually.\n"
            "Format: ctrl+shift+alt+a"
        )
    
    def _test_api(self) -> None:
        """Test selected API key connection."""
        selection = self.keys_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an API key to test.")
            return
        
        index = selection[0]
        
        # Get the actual key
        if hasattr(self, 'temp_keys'):
            keys = self.temp_keys
        else:
            keys = self.config.get_all_api_keys()
        
        if index >= len(keys):
            messagebox.showerror("Error", "Invalid key selection.")
            return
        
        api_key = keys[index]
        
        try:
            from google import genai
            
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents="Hello"
            )
            messagebox.showinfo("Success", f"API key #{index + 1} works correctly!")
        except Exception as e:
            messagebox.showerror("Error", f"API test failed:\n{str(e)[:100]}")
    
    def _test_capture(self) -> None:
        """Test screenshot capture."""
        if self.on_test_capture:
            self.on_test_capture()
            messagebox.showinfo("Test Capture", "Screenshot captured!\nCheck the logs directory.")
    
    def _save_settings(self) -> None:
        """Save settings to configuration."""
        try:
            # Save API keys
            if hasattr(self, 'temp_keys'):
                # Clear old keys and add new ones
                old_keys = self.config.get_all_api_keys()
                self.config.set('gemini.api_keys', self.temp_keys)
            
            # Update other configuration
            self.config.set('hotkey', self.hotkey_var.get().strip())
            self.config.set('gemini.system_prompt', self.prompt_text.get('1.0', tk.END).strip())
            self.config.set('gemini.auto_rotate_on_quota_error', self.auto_rotate_var.get())
            self.config.set('auto_paste.enabled', self.auto_paste_var.get())
            self.config.set('auto_paste.restore_clipboard', self.restore_clipboard_var.get())
            self.config.set('auto_paste.delay_ms', self.delay_var.get())
            self.config.set('startup.launch_on_boot', self.startup_var.get())
            
            logger.info("Settings saved")
            
            # Call callback
            if self.on_save:
                self.on_save()
            
            messagebox.showinfo("Success", "Settings saved successfully!\n\nPlease restart the application for changes to take effect.")
            self._close_window()
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings:\n{str(e)}")
    
    def _close_window(self) -> None:
        """Close settings window."""
        if self.window:
            self.window.destroy()
            self.window = None
            logger.info("Settings window closed")
    
    def run(self) -> None:
        """Run the settings window (blocking)."""
        if self.window:
            self.window.mainloop()
