"""Gemini AI integration with automatic API key rotation."""
from google import genai
from PIL import Image
from typing import Optional
from logger import logger


class GeminiIntegration:
    """Handles communication with Gemini AI API using google-genai SDK with key rotation."""
    
    def __init__(self, config_manager, model_name: str = "gemini-3-flash-preview"):
        """Initialize Gemini integration.
        
        Args:
            config_manager: ConfigManager instance for key rotation
            model_name: Model to use (default: Gemini 3 Flash Preview)
        """
        self.config = config_manager
        self.model_name = model_name
        self.client = None
        self.current_api_key = None
        
        # Initialize with first available key
        api_key = self.config.get_api_key()
        if api_key:
            self._initialize_client(api_key)
    
    def _initialize_client(self, api_key: str) -> None:
        """Initialize Gemini client with API key.
        
        Args:
            api_key: API key to use
        """
        try:
            self.client = genai.Client(api_key=api_key)
            self.current_api_key = api_key
            logger.info(f"Gemini client initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def _is_quota_error(self, error: Exception) -> bool:
        """Check if error is a quota/rate limit error.
        
        Args:
            error: Exception to check
            
        Returns:
            True if quota error, False otherwise
        """
        error_str = str(error).lower()
        quota_indicators = [
            'quota',
            'rate limit',
            'resource exhausted',
            '429',
            'too many requests',
            'exceeded'
        ]
        return any(indicator in error_str for indicator in quota_indicators)
    
    def _try_rotate_key(self) -> bool:
        """Attempt to rotate to next API key.
        
        Returns:
            True if rotation successful, False if no more keys
        """
        if not self.config.is_auto_rotate_enabled():
            logger.info("Auto-rotation disabled, not rotating key")
            return False
        
        all_keys = self.config.get_all_api_keys()
        if len(all_keys) <= 1:
            logger.warning("No alternative API keys available for rotation")
            return False
        
        # Get next key
        next_key = self.config.rotate_to_next_key()
        
        if next_key == self.current_api_key:
            logger.warning("Rotated back to same key (only one key or full cycle)")
            return False
        
        # Try initializing with new key
        try:
            self._initialize_client(next_key)
            logger.info(f"Successfully rotated to next API key (index: {self.config.get('gemini.current_key_index')})")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize with rotated key: {e}")
            return False
    
    def set_api_key(self, api_key: str) -> None:
        """Update API key and reinitialize client.
        
        Args:
            api_key: New API key
        """
        self._initialize_client(api_key)
    
    async def analyze_screenshot(
        self,
        image: Image.Image,
        prompt: str = "Analyze this screenshot and provide a solution.",
        retry_count: int = 0
    ) -> str:
        """Send screenshot to Gemini for analysis (async) with auto-rotation.
        
        Args:
            image: PIL Image object
            prompt: Custom prompt for analysis
            retry_count: Internal retry counter
            
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
            # Check if it's a quota error and we haven't tried all keys yet
            if self._is_quota_error(e) and retry_count < len(self.config.get_all_api_keys()):
                logger.warning(f"Quota error detected: {str(e)[:100]}")
                
                if self._try_rotate_key():
                    logger.info("Retrying with rotated API key...")
                    return await self.analyze_screenshot(image, prompt, retry_count + 1)
            
            error_msg = f"Error analyzing screenshot: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def analyze_screenshot_sync(
        self,
        image: Image.Image,
        prompt: str = "Analyze this screenshot and provide a solution.",
        retry_count: int = 0
    ) -> str:
        """Synchronous version of analyze_screenshot with auto-rotation.
        
        Args:
            image: PIL Image object
            prompt: Custom prompt for analysis
            retry_count: Internal retry counter
            
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
            # Check if it's a quota error and we haven't tried all keys yet
            if self._is_quota_error(e) and retry_count < len(self.config.get_all_api_keys()):
                logger.warning(f"Quota error detected: {str(e)[:100]}")
                
                if self._try_rotate_key():
                    logger.info("Retrying with rotated API key...")
                    return self.analyze_screenshot_sync(image, prompt, retry_count + 1)
            
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
