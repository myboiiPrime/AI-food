"""
Recipe Service - Spoonacular API Integration

Handles recipe search and recommendations based on ingredients
and health-based filters.

Free Tier: 3,000 requests/month (150 API points/day)
"""
import requests
from typing import Optional


class SpoonacularRecipeService:
    """
    Service for searching recipes using the Spoonacular API.
    
    Supports ingredient-based search with nutritional filtering
    for health-conscious recipe recommendations.
    """
    
    BASE_URL = "https://api.spoonacular.com"
    
    def __init__(self, api_key: str):
        """
        Initialize the Spoonacular recipe service.
        
        Args:
            api_key: Spoonacular API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.params = {"apiKey": api_key}
    
    def search_recipes(
        self,
        ingredients: list[str],
        filters: Optional[dict] = None,
        number: int = 10
    ) -> list[dict]:
        """
        Search for recipes by ingredients with optional nutritional filters.
        
        Args:
            ingredients: List of ingredient names
            filters: Dictionary of nutritional filters from logic.py
            number: Maximum number of recipes to return
            
        Returns:
            List of recipe dictionaries with title, image, and nutrition info
        """
        # First, find recipes by ingredients
        endpoint = f"{self.BASE_URL}/recipes/complexSearch"
        
        params = {
            "includeIngredients": ",".join(ingredients),
            "number": number,
            "addRecipeInformation": True,
            "addRecipeNutrition": True,
            "fillIngredients": True,
            "sort": "max-used-ingredients"
        }
        
        # Apply health filters from logic.py
        if filters:
            for key, value in filters.items():
                params[key] = value
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            recipes = []
            for result in data.get("results", []):
                recipes.append(self._format_recipe(result))
            
            return recipes
            
        except requests.RequestException as e:
            raise Exception(f"Spoonacular API error: {str(e)}")
    
    def get_recipe_details(self, recipe_id: int) -> dict:
        """
        Get detailed information about a specific recipe.
        
        Args:
            recipe_id: Spoonacular recipe ID
            
        Returns:
            Detailed recipe dictionary
        """
        endpoint = f"{self.BASE_URL}/recipes/{recipe_id}/information"
        
        params = {
            "includeNutrition": True
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return self._format_recipe(response.json())
            
        except requests.RequestException as e:
            raise Exception(f"Spoonacular API error: {str(e)}")
    
    def _format_recipe(self, raw_recipe: dict) -> dict:
        """
        Format raw Spoonacular response into a cleaner structure.
        
        Args:
            raw_recipe: Raw recipe data from API
            
        Returns:
            Formatted recipe dictionary
        """
        # Extract key nutrients
        nutrition = {}
        nutrients_list = raw_recipe.get("nutrition", {}).get("nutrients", [])
        key_nutrients = ["Calories", "Protein", "Carbohydrates", "Fat", "Fiber", "Sugar", "Sodium"]
        
        for nutrient in nutrients_list:
            if nutrient.get("name") in key_nutrients:
                nutrition[nutrient["name"].lower()] = {
                    "amount": nutrient["amount"],
                    "unit": nutrient["unit"]
                }
        
        # Extract used and missing ingredients
        used_ingredients = [
            ing.get("name", "")
            for ing in raw_recipe.get("usedIngredients", [])
        ]
        missed_ingredients = [
            ing.get("name", "")
            for ing in raw_recipe.get("missedIngredients", [])
        ]
        
        return {
            "id": raw_recipe.get("id"),
            "title": raw_recipe.get("title"),
            "image": raw_recipe.get("image"),
            "readyInMinutes": raw_recipe.get("readyInMinutes"),
            "servings": raw_recipe.get("servings"),
            "sourceUrl": raw_recipe.get("sourceUrl"),
            "summary": raw_recipe.get("summary", "")[:200] + "..." if raw_recipe.get("summary") else "",
            "nutrition": nutrition,
            "usedIngredients": used_ingredients,
            "missedIngredients": missed_ingredients,
            "diets": raw_recipe.get("diets", []),
            "healthScore": raw_recipe.get("healthScore", 0)
        }
    
    def get_recipe_instructions(self, recipe_id: int) -> list[dict]:
        """
        Get step-by-step cooking instructions for a recipe.
        
        Args:
            recipe_id: Spoonacular recipe ID
            
        Returns:
            List of instruction steps
        """
        endpoint = f"{self.BASE_URL}/recipes/{recipe_id}/analyzedInstructions"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            data = response.json()
            
            steps = []
            for instruction_set in data:
                for step in instruction_set.get("steps", []):
                    steps.append({
                        "number": step.get("number"),
                        "step": step.get("step"),
                        "ingredients": [ing.get("name") for ing in step.get("ingredients", [])],
                        "equipment": [eq.get("name") for eq in step.get("equipment", [])]
                    })
            
            return steps
            
        except requests.RequestException as e:
            raise Exception(f"Spoonacular API error: {str(e)}")
