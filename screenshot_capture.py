"""Screenshot capture functionality using mss library."""
import io
import mss
from PIL import Image
from pathlib import Path
from typing import Optional
from logger import logger


class ScreenshotCapture:
    """Handles screenshot capture without changing window focus."""
    
    def __init__(self, save_to_disk: bool = False, output_dir: str = "screenshots"):
        """Initialize screenshot capture.
        
        Args:
            save_to_disk: Whether to save screenshots to disk
            output_dir: Directory to save screenshots
        """
        self.save_to_disk = save_to_disk
        self.output_dir = Path(output_dir)
        
        if self.save_to_disk:
            self.output_dir.mkdir(exist_ok=True)
    
    def capture_full_screen(self, monitor: int = 1) -> Image.Image:
        """Capture full screen without changing focus.
        
        Args:
            monitor: Monitor number (1 for primary monitor)
            
        Returns:
            PIL Image object
        """
        try:
            with mss.mss() as sct:
                # Capture the specified monitor
                monitor_data = sct.monitors[monitor]
                screenshot = sct.grab(monitor_data)
                
                # Convert to PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                logger.info(f"Screenshot captured: {screenshot.size}")
                
                # Optionally save to disk
                if self.save_to_disk:
                    from datetime import datetime
                    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    filepath = self.output_dir / filename
                    img.save(filepath)
                    logger.info(f"Screenshot saved to {filepath}")
                
                return img
                
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            raise
    
    def capture_active_window(self) -> Optional[Image.Image]:
        """Capture only the active window.
        
        Note: This is a placeholder for future implementation.
        Currently falls back to full screen capture.
        
        Returns:
            PIL Image object or None
        """
        # TODO: Implement active window capture using win32gui
        logger.warning("Active window capture not implemented, using full screen")
        return self.capture_full_screen()
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> Image.Image:
        """Capture specific screen region.
        
        Args:
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Width of region
            height: Height of region
            
        Returns:
            PIL Image object
        """
        try:
            with mss.mss() as sct:
                region = {"top": y, "left": x, "width": width, "height": height}
                screenshot = sct.grab(region)
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                logger.info(f"Region captured: {width}x{height} at ({x}, {y})")
                return img
                
        except Exception as e:
            logger.error(f"Failed to capture region: {e}")
            raise
    
    def image_to_bytes(self, img: Image.Image, format: str = "PNG") -> bytes:
        """Convert PIL Image to bytes.
        
        Args:
            img: PIL Image object
            format: Image format (PNG, JPEG, etc.)
            
        Returns:
            Image bytes
        """
        byte_arr = io.BytesIO()
        img.save(byte_arr, format=format)
        return byte_arr.getvalue()
