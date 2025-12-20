"""
Configuration management for Smart Ingredient Chef Backend.
Loads environment variables securely using python-dotenv.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""
    
    # Roboflow Vision AI
    ROBOFLOW_API_KEY = os.getenv('ROBOFLOW_API_KEY')
    ROBOFLOW_MODEL_ID = os.getenv('ROBOFLOW_MODEL_ID', 'food-ingredients-detection-bq4jf/1')
    
    # Spoonacular Recipe API
    SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
    SPOONACULAR_BASE_URL = 'https://api.spoonacular.com'
    
    # USDA FoodData Central API
    USDA_API_KEY = os.getenv('USDA_API_KEY')
    USDA_BASE_URL = 'https://api.nal.usda.gov/fdc/v1'
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate that required configuration is present. Returns list of missing keys."""
        missing = []
        if not cls.ROBOFLOW_API_KEY:
            missing.append('ROBOFLOW_API_KEY')
        if not cls.SPOONACULAR_API_KEY:
            missing.append('SPOONACULAR_API_KEY')
        if not cls.USDA_API_KEY:
            missing.append('USDA_API_KEY')
        return missing
