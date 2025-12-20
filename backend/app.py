"""
Smart Ingredient Chef - Flask Backend
Main application entry point with API endpoints.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import tempfile
import os

from config import Config
from logic import build_recipe_filters
from services.vision_service import RoboflowVisionService
from services.recipe_service import SpoonacularRecipeService
from services.nutrition_service import USDANutritionService


app = Flask(__name__)
CORS(app)

# Initialize services
vision_service = None
recipe_service = None
nutrition_service = None


def init_services():
    """Initialize API services. Called on first request."""
    global vision_service, recipe_service, nutrition_service
    
    missing = Config.validate()
    if missing:
        app.logger.warning(f"Missing API keys: {missing}. Some features may not work.")
    
    if Config.ROBOFLOW_API_KEY:
        vision_service = RoboflowVisionService(
            api_key=Config.ROBOFLOW_API_KEY,
            model_id=Config.ROBOFLOW_MODEL_ID
        )
    
    if Config.SPOONACULAR_API_KEY:
        recipe_service = SpoonacularRecipeService(
            api_key=Config.SPOONACULAR_API_KEY
        )
    
    if Config.USDA_API_KEY:
        nutrition_service = USDANutritionService(
            api_key=Config.USDA_API_KEY
        )


@app.before_request
def ensure_services():
    """Lazy initialization of services on first request."""
    if vision_service is None and recipe_service is None:
        init_services()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    services_status = {
        'vision': vision_service is not None,
        'recipe': recipe_service is not None,
        'nutrition': nutrition_service is not None
    }
    return jsonify({
        'status': 'healthy',
        'services': services_status
    })


@app.route('/api/detect', methods=['POST'])
def detect_ingredients():
    """
    Detect ingredients from an image.
    
    Expects JSON body:
    {
        "image": "base64_encoded_image_string"
    }
    
    Returns:
    {
        "success": true,
        "ingredients": ["tomato", "onion", "garlic"]
    }
    """
    if not vision_service:
        return jsonify({
            'success': False,
            'error': 'Vision service unavailable. Please check ROBOFLOW_API_KEY.'
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "image" field in request body.'
            }), 400
        
        # Decode base64 image and save to temp file
        image_data = base64.b64decode(data['image'])
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_data)
            tmp_path = tmp_file.name
        
        try:
            ingredients = vision_service.detect_ingredients(tmp_path)
            return jsonify({
                'success': True,
                'ingredients': ingredients
            })
        finally:
            # Clean up temp file
            os.unlink(tmp_path)
            
    except Exception as e:
        app.logger.error(f"Detection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Service unavailable. Please try again later.'
        }), 503


@app.route('/api/detect-url', methods=['POST'])
def detect_ingredients_from_url():
    """
    Detect ingredients from an image URL.
    
    Expects JSON body:
    {
        "image_url": "https://example.com/image.jpg"
    }
    
    Returns:
    {
        "success": true,
        "ingredients": ["tomato", "onion", "garlic"]
    }
    """
    if not vision_service:
        return jsonify({
            'success': False,
            'error': 'Vision service unavailable. Please check ROBOFLOW_API_KEY.'
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'image_url' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "image_url" field in request body.'
            }), 400
        
        ingredients = vision_service.detect_ingredients_from_url(data['image_url'])
        return jsonify({
            'success': True,
            'ingredients': ingredients
        })
            
    except Exception as e:
        app.logger.error(f"Detection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Service unavailable. Please try again later.'
        }), 503


@app.route('/api/analyze', methods=['POST'])
def analyze_cart():
    """
    Analyze cart ingredients and return health-filtered recipes.
    
    Expects JSON body:
    {
        "ingredients": ["tomato", "egg", "onion"],
        "user_profile": {
            "health_constraints": {
                "condition": "diabetes"  // or "hypertension", "muscle_build"
            }
        }
    }
    
    Returns:
    {
        "success": true,
        "recipes": [...],
        "applied_filters": {"maxSugar": 5, "minFiber": 5}
    }
    """
    if not recipe_service:
        return jsonify({
            'success': False,
            'error': 'Recipe service unavailable. Please check SPOONACULAR_API_KEY.'
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'ingredients' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "ingredients" field in request body.'
            }), 400
        
        ingredients = data['ingredients']
        user_profile = data.get('user_profile', {})
        
        # Build health-based filters using logic.py
        filters = build_recipe_filters(user_profile)
        
        # Search for recipes
        recipes = recipe_service.search_recipes(
            ingredients=ingredients,
            filters=filters
        )
        
        return jsonify({
            'success': True,
            'recipes': recipes,
            'applied_filters': filters
        })
        
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Service unavailable. Please try again later.'
        }), 503


@app.route('/api/nutrition', methods=['POST'])
def get_nutrition():
    """
    Get nutrition information for ingredients.
    
    Expects JSON body:
    {
        "ingredients": ["tomato", "egg"]
    }
    
    Returns:
    {
        "success": true,
        "nutrition": {...}
    }
    """
    if not nutrition_service:
        return jsonify({
            'success': False,
            'error': 'Nutrition service unavailable. Please check USDA_API_KEY.'
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'ingredients' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "ingredients" field in request body.'
            }), 400
        
        ingredients = data['ingredients']
        nutrition_data = nutrition_service.get_nutrition_info(ingredients)
        
        return jsonify({
            'success': True,
            'nutrition': nutrition_data
        })
        
    except Exception as e:
        app.logger.error(f"Nutrition error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Service unavailable. Please try again later.'
        }), 503


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.FLASK_DEBUG
    )
