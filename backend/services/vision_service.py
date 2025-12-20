"""
Vision Service - Roboflow Integration

Handles ingredient detection from images using Roboflow's inference SDK
with the serverless workflow API for comprehensive food detection.

Free Tier: 1,000 API calls/month
"""
from inference_sdk import InferenceHTTPClient
import os
from typing import Optional


class RoboflowVisionService:
    """
    Service for detecting food ingredients from images using Roboflow.
    
    Uses the inference SDK to communicate with Roboflow's workflow API.
    """
    
    # Workflow configuration
    WORKSPACE_NAME = "food-69lly"
    WORKFLOW_ID = (
        "find-tomatoes-zucchinis-onions-garlics-bananas-limes-spinaches-gingers-"
        "broccolis-cherries-radishes-nuts-chilis-seeds-quinces-berries-lemons-"
        "mushrooms-oils-pastas-salmon-fish-beefs-chickens-eggs-shrimp-porks-"
        "meats-and-basils"
    )
    
    def __init__(self, api_key: str, model_id: str = None):
        """
        Initialize the Roboflow vision service.
        
        Args:
            api_key: Roboflow API key
            model_id: Model identifier (optional, uses workflow by default)
        """
        self.client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=api_key
        )
        self.model_id = model_id
        self.confidence_threshold = 0.5  # Minimum confidence for predictions
    
    def _run_workflow(self, image_path_or_url: str, max_retries: int = 3) -> dict:
        """
        Run the Roboflow workflow on an image with retry logic for cold starts.
        
        Args:
            image_path_or_url: Local file path or URL of the image
            max_retries: Maximum number of retries for model initialization
            
        Returns:
            Workflow result dictionary
        """
        import time
        
        for attempt in range(max_retries):
            result = self.client.run_workflow(
                workspace_name=self.WORKSPACE_NAME,
                workflow_id=self.WORKFLOW_ID,
                images={
                    "image": image_path_or_url
                }
            )
            
            # Check if model is still initializing (cold start)
            if isinstance(result, list) and len(result) > 0:
                first_item = result[0]
                if isinstance(first_item, dict) and "message" in first_item:
                    message = first_item.get("message", "")
                    if "being initialized" in message.lower():
                        if attempt < max_retries - 1:
                            # Wait with exponential backoff
                            wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
                            time.sleep(wait_time)
                            continue
            
            return result
        
        return result
    
    def detect_ingredients(self, image_path: str) -> list[str]:
        """
        Detect ingredients from an image file.
        
        Args:
            image_path: Path to the image file (JPG, PNG, etc.)
            
        Returns:
            List of detected ingredient names (deduplicated)
            
        Raises:
            Exception: If the API call fails
        """
        result = self._run_workflow(image_path)
        
        # Extract class names from predictions, filtering by confidence
        ingredients = set()
        
        # Handle workflow response format (list of outputs)
        if isinstance(result, list):
            for output in result:
                predictions = output.get("predictions", {})
                if isinstance(predictions, dict):
                    predictions = predictions.get("predictions", [])
                
                for prediction in predictions:
                    confidence = prediction.get("confidence", 0)
                    if confidence >= self.confidence_threshold:
                        ingredient_name = prediction.get("class", "").lower().strip()
                        if ingredient_name:
                            ingredients.add(ingredient_name)
        
        return list(ingredients)
    
    def detect_ingredients_from_url(self, image_url: str) -> list[str]:
        """
        Detect ingredients from an image URL.
        
        Args:
            image_url: URL of the image
            
        Returns:
            List of detected ingredient names (deduplicated)
            
        Raises:
            Exception: If the API call fails
        """
        return self.detect_ingredients(image_url)
    
    def detect_ingredients_with_details(self, image_path: str) -> list[dict]:
        """
        Detect ingredients with full details including confidence and bounding boxes.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of dictionaries with ingredient details:
            [
                {
                    "name": "tomato",
                    "confidence": 0.95,
                    "bbox": {"x": 100, "y": 100, "width": 50, "height": 50}
                }
            ]
        """
        result = self._run_workflow(image_path)
        
        ingredients = []
        
        # Handle workflow response format (list of outputs)
        if isinstance(result, list):
            for output in result:
                predictions = output.get("predictions", {})
                if isinstance(predictions, dict):
                    predictions = predictions.get("predictions", [])
                
                for prediction in predictions:
                    confidence = prediction.get("confidence", 0)
                    if confidence >= self.confidence_threshold:
                        ingredients.append({
                            "name": prediction.get("class", "").lower().strip(),
                            "confidence": round(confidence, 3),
                            "bbox": {
                                "x": prediction.get("x", 0),
                                "y": prediction.get("y", 0),
                                "width": prediction.get("width", 0),
                                "height": prediction.get("height", 0)
                            }
                        })
        
        return ingredients
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """
        Set the minimum confidence threshold for predictions.
        
        Args:
            threshold: Float between 0.0 and 1.0
        """
        if 0.0 <= threshold <= 1.0:
            self.confidence_threshold = threshold
        else:
            raise ValueError("Threshold must be between 0.0 and 1.0")
