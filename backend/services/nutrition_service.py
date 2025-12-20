"""
Nutrition Service - USDA FoodData Central API Integration

Provides detailed nutrition information for ingredients.
Public domain database with 300,000+ food items.

Free Tier: 1,000 requests/hour (no credit card required)
"""
import requests
from typing import Optional


class USDANutritionService:
    """
    Service for retrieving nutrition data from USDA FoodData Central.
    
    Uses the public FoodData Central API for comprehensive
    nutritional information on food ingredients.
    """
    
    BASE_URL = "https://api.nal.usda.gov/fdc/v1"
    
    def __init__(self, api_key: str):
        """
        Initialize the USDA nutrition service.
        
        Args:
            api_key: Data.gov API key for USDA FoodData Central
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.params = {"api_key": api_key}
    
    def search_food(self, query: str, page_size: int = 5) -> list[dict]:
        """
        Search for foods matching a query.
        
        Args:
            query: Food name to search
            page_size: Maximum results to return
            
        Returns:
            List of matching foods with basic info
        """
        endpoint = f"{self.BASE_URL}/foods/search"
        
        params = {
            "query": query,
            "pageSize": page_size,
            "dataType": ["Foundation", "SR Legacy"]  # Prioritize common foods
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            foods = []
            for food in data.get("foods", []):
                foods.append({
                    "fdcId": food.get("fdcId"),
                    "description": food.get("description"),
                    "dataType": food.get("dataType"),
                    "brandOwner": food.get("brandOwner")
                })
            
            return foods
            
        except requests.RequestException as e:
            raise Exception(f"USDA API error: {str(e)}")
    
    def get_food_nutrition(self, fdc_id: int) -> dict:
        """
        Get detailed nutrition information for a specific food.
        
        Args:
            fdc_id: USDA FoodData Central ID
            
        Returns:
            Dictionary with nutrition details
        """
        endpoint = f"{self.BASE_URL}/food/{fdc_id}"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            data = response.json()
            
            return self._format_nutrition(data)
            
        except requests.RequestException as e:
            raise Exception(f"USDA API error: {str(e)}")
    
    def get_nutrition_info(self, ingredients: list[str]) -> dict:
        """
        Get nutrition information for a list of ingredients.
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Dictionary mapping ingredient names to their nutrition data
        """
        result = {}
        
        for ingredient in ingredients:
            try:
                # Search for the ingredient
                foods = self.search_food(ingredient, page_size=1)
                
                if foods:
                    # Get nutrition for the top match
                    fdc_id = foods[0]["fdcId"]
                    nutrition = self.get_food_nutrition(fdc_id)
                    result[ingredient] = {
                        "found": True,
                        "matchedFood": foods[0]["description"],
                        "nutrition": nutrition
                    }
                else:
                    result[ingredient] = {
                        "found": False,
                        "matchedFood": None,
                        "nutrition": None
                    }
                    
            except Exception as e:
                result[ingredient] = {
                    "found": False,
                    "error": str(e)
                }
        
        return result
    
    def _format_nutrition(self, raw_data: dict) -> dict:
        """
        Format raw USDA response into a cleaner structure.
        
        Args:
            raw_data: Raw food data from API
            
        Returns:
            Formatted nutrition dictionary
        """
        nutrients = {}
        
        # Key nutrients to extract
        nutrient_mapping = {
            "Energy": "calories",
            "Protein": "protein",
            "Total lipid (fat)": "fat",
            "Carbohydrate, by difference": "carbohydrates",
            "Fiber, total dietary": "fiber",
            "Sugars, total including NLEA": "sugar",
            "Sodium, Na": "sodium",
            "Cholesterol": "cholesterol",
            "Fatty acids, total saturated": "saturatedFat"
        }
        
        for nutrient in raw_data.get("foodNutrients", []):
            nutrient_name = nutrient.get("nutrient", {}).get("name", "")
            
            if nutrient_name in nutrient_mapping:
                key = nutrient_mapping[nutrient_name]
                nutrients[key] = {
                    "amount": nutrient.get("amount", 0),
                    "unit": nutrient.get("nutrient", {}).get("unitName", "")
                }
        
        return {
            "description": raw_data.get("description", ""),
            "servingSize": raw_data.get("servingSize"),
            "servingSizeUnit": raw_data.get("servingSizeUnit", "g"),
            "nutrients": nutrients
        }
