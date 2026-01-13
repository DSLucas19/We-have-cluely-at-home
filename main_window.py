"""Main application window for AI Assistant."""
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
from typing import Callable, Optional
from datetime import datetime
from logger import logger

class ModernTheme:
    """Colors and styles for modern dark theme."""
    BG = "#1e1e1e"
    FG = "#ffffff"
    ACCENT = "#007acc"
    ACCENT_HOVER = "#0098ff"
    SECONDARY = "#252526"
    BORDER = "#3e3e42"
    SUCCESS = "#4ec9b0"
    ERROR = "#f44747"
    WARNING = "#cca700"
    
    FONT_MAIN = ("Segoe UI", 10)
    FONT_HEADER = ("Segoe UI", 12, "bold")
    FONT_MONO = ("Consolas", 10)

class MainWindow:
    """Main GUI window for the AI Assistant."""
    
    def __init__(
        self,
        app_name: str,
        version: str,
        on_toggle: Callable[[bool], None],
        on_capture: Callable[[], None],
        on_settings: Callable[[], None],
        on_exit: Callable[[], None],
        initial_enabled: bool = True
    ):
        """Initialize main window."""
        self.app_name = app_name
        self.version = version
        self.on_toggle = on_toggle
        self.on_capture = on_capture
        self.on_settings = on_settings
        self.on_exit = on_exit
        
        self.window: Optional[tk.Tk] = None
        self.is_enabled = initial_enabled
        self.log_queue = queue.Queue()
        
        # State for dragging window
        self._drag_data = {"x": 0, "y": 0}
        
    def create_window(self) -> None:
        """Create and configure the main window."""
        self.window = tk.Tk()
        self.window.title(self.app_name)
        self.window.geometry("400x600")
        self.window.configure(bg=ModernTheme.BG)
        # self.window.overrideredirect(True)  # Frameless window - maybe too aggressive for now, standard frame is safer
        
        # Configure Styles
        self._configure_styles()
        
        # Create UI Layout
        self._create_header()
        self._create_status_area()
        self._create_log_area()
        self._create_controls()
        self._create_footer()
        
        # Handle close
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
        
        # Start log poller
        self._poll_logs()
        
    def _configure_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # General Frame
        style.configure('TFrame', background=ModernTheme.BG)
        style.configure('Card.TFrame', background=ModernTheme.SECONDARY, relief='flat')
        
        # Buttons
        style.configure(
            'Accent.TButton',
            background=ModernTheme.ACCENT,
            foreground='white',
            borderwidth=0,
            font=ModernTheme.FONT_MAIN,
            padding=10
        )
        style.map(
            'Accent.TButton',
            background=[('active', ModernTheme.ACCENT_HOVER)],
            relief=[('pressed', 'flat')]
        )
        
        style.configure(
            'Secondary.TButton',
            background=ModernTheme.SECONDARY,
            foreground='white',
            borderwidth=1,
            bordercolor=ModernTheme.BORDER,
            font=ModernTheme.FONT_MAIN,
            padding=8
        )
        style.map(
            'Secondary.TButton',
            background=[('active', ModernTheme.BORDER)]
        )
        
        # Labels
        style.configure(
            'TLabel',
            background=ModernTheme.BG,
            foreground=ModernTheme.FG,
            font=ModernTheme.FONT_MAIN
        )
        style.configure(
            'Header.TLabel',
            font=ModernTheme.FONT_HEADER
        )
        
    def _create_header(self):
        """Create header section."""
        header_frame = ttk.Frame(self.window)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Title
        title = ttk.Label(
            header_frame,
            text=self.app_name,
            style='Header.TLabel',
            font=("Segoe UI", 16, "bold")
        )
        title.pack(side=tk.LEFT)
        
        # Version badge
        version = ttk.Label(
            header_frame,
            text=f"v{self.version}",
            foreground="gray",
            font=("Segoe UI", 8)
        )
        version.pack(side=tk.LEFT, padx=10, pady=(4, 0))
        
    def _create_status_area(self):
        """Create status indicator."""
        status_frame = ttk.Frame(self.window, style='Card.TFrame', padding=15)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = ttk.Label(
            status_frame,
            text="● Active",
            background=ModernTheme.SECONDARY,
            foreground=ModernTheme.SUCCESS,
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.hotkey_label = ttk.Label(
            status_frame,
            text="Waiting for input...",
            background=ModernTheme.SECONDARY,
            foreground="gray"
        )
        self.hotkey_label.pack(side=tk.RIGHT)
        
    def _create_log_area(self):
        """Create scrollable log area."""
        log_frame = ttk.Frame(self.window)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(log_frame, text="Activity Log", foreground="gray").pack(anchor=tk.W, pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            bg=ModernTheme.SECONDARY,
            fg=ModernTheme.FG,
            font=ModernTheme.FONT_MONO,
            relief='flat',
            padx=10,
            pady=10,
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state='disabled')
        
        # Tag configs for colors
        self.log_text.tag_config('INFO', foreground=ModernTheme.FG)
        self.log_text.tag_config('ERROR', foreground=ModernTheme.ERROR)
        self.log_text.tag_config('WARNING', foreground=ModernTheme.WARNING)
        self.log_text.tag_config('SUCCESS', foreground=ModernTheme.SUCCESS)
        
    def _create_controls(self):
        """Create control buttons."""
        control_frame = ttk.Frame(self.window)
        control_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Top row: Capture
        capture_btn = ttk.Button(
            control_frame,
            text="⚡ Capture Now",
            style='Accent.TButton',
            command=self.on_capture
        )
        capture_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Bottom row: Settings | Enable/Toggle
        row_frame = ttk.Frame(control_frame)
        row_frame.pack(fill=tk.X)
        
        self.enable_btn = ttk.Button(
            row_frame,
            text="Disable",
            style='Secondary.TButton',
            command=self._toggle_enabled
        )
        self.enable_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        settings_btn = ttk.Button(
            row_frame,
            text="Settings",
            style='Secondary.TButton',
            command=self.on_settings
        )
        settings_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
    def _create_footer(self):
        """Create footer."""
        footer_frame = ttk.Frame(self.window)
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Quit button
        quit_btn = ttk.Label(
            footer_frame,
            text="Quit Application",
            foreground="gray",
            cursor="hand2"
        )
        quit_btn.pack(side=tk.RIGHT)
        quit_btn.bind("<Button-1>", lambda e: self.on_exit())
        
    def _toggle_enabled(self):
        """Toggle enabled state."""
        self.is_enabled = not self.is_enabled
        self.on_toggle(self.is_enabled)
        
        if self.is_enabled:
            self.enable_btn.configure(text="Disable")
            self.status_label.configure(text="● Active", foreground=ModernTheme.SUCCESS)
        else:
            self.enable_btn.configure(text="Enable")
            self.status_label.configure(text="○ Paused", foreground="gray")
            
    def update_hotkey(self, hotkey: str):
        """Update hotkey display."""
        if self.window:
            self.hotkey_label.configure(text=f"Hotkey: {hotkey}")
            
    def log(self, message: str, level: str = "INFO"):
        """Add message to log queue."""
        self.log_queue.put((datetime.now().strftime("%H:%M:%S"), level, message))
        
    def _poll_logs(self):
        """Poll for new log messages."""
        if not self.window:
            return
            
        try:
            while True:
                timestamp, level, msg = self.log_queue.get_nowait()
                if self.window:
                    self.log_text.configure(state='normal')
                    self.log_text.insert(tk.END, f"[{timestamp}] ", 'INFO')
                    self.log_text.insert(tk.END, f"{msg}\n", level)
                    self.log_text.see(tk.END)
                    self.log_text.configure(state='disabled')
        except queue.Empty:
            pass
            
        self.window.after(100, self._poll_logs)

    def show(self):
        """Show the window."""
        if not self.window:
            self.create_window()
        else:
            self.window.deiconify()
            self.window.lift()
            
    def hide(self):
        """Hide the window (minimize to tray)."""
        if self.window:
            self.window.withdraw()
            
    def update_status(self, text: str):
        """Update status label text temporarily."""
        if self.window and hasattr(self, 'status_label'):
             # You might want to flash or just change it
             # For now, just logging it
             pass

    def close(self):
        """Destroy window."""
        if self.window:
            self.window.destroy()
            self.window = None
