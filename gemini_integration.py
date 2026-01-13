"""Gemini AI integration with new google-genai SDK."""
from google import genai
from PIL import Image
from typing import Optional
from logger import logger


class GeminiIntegration:
    """Handles communication with Gemini AI API using new google-genai SDK."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-3-flash-preview"):
        """Initialize Gemini integration.
        
        Args:
            api_key: Google AI API key
            model_name: Model to use (default: Gemini 3 Flash Preview)
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        
        if api_key:
            self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Gemini client with API key."""
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Gemini client initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def set_api_key(self, api_key: str) -> None:
        """Update API key and reinitialize client.
        
        Args:
            api_key: New API key
        """
        self.api_key = api_key
        self._initialize_client()
    
    async def analyze_screenshot(
        self,
        image: Image.Image,
        prompt: str = "Analyze this screenshot and provide a solution."
    ) -> str:
        """Send screenshot to Gemini for analysis (async).
        
        Args:
            image: PIL Image object
            prompt: Custom prompt for analysis
            
        Returns:
            AI response text
        """
        if not self.client:
            error_msg = "Gemini client not initialized. Please set API key."
            logger.error(error_msg)
            return error_msg
        
        try:
            logger.info("Sending screenshot to Gemini (async)...")
            
            # Pass PIL Image directly - SDK handles conversion
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[prompt, image]
            )
            
            result_text = response.text
            
            logger.info(f"Received response from Gemini ({len(result_text)} chars)")
            return result_text
            
        except Exception as e:
            error_msg = f"Error analyzing screenshot: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def analyze_screenshot_sync(
        self,
        image: Image.Image,
        prompt: str = "Analyze this screenshot and provide a solution."
    ) -> str:
        """Synchronous version of analyze_screenshot.
        
        Args:
            image: PIL Image object
            prompt: Custom prompt for analysis
            
        Returns:
            AI response text
        """
        if not self.client:
            error_msg = "Gemini client not initialized. Please set API key."
            logger.error(error_msg)
            return error_msg
        
        try:
            logger.info("Sending screenshot to Gemini (sync)...")
            
            # Pass PIL Image directly - SDK handles conversion
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, image]
            )
            
            result_text = response.text
            
            logger.info(f"Received response from Gemini ({len(result_text)} chars)")
            return result_text
            
        except Exception as e:
            error_msg = f"Error analyzing screenshot: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def test_connection(self) -> bool:
        """Test connection to Gemini API.
        
        Returns:
            True if connection successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            # Try a simple text generation
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Hello"
            )
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
