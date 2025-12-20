"""
Smart Filter Logic - Health Constraint Translation Layer

This module contains all health-related decision logic.
Per project rules: ALL decision-making logic resides in the backend, 
never in the React Native app.
"""


def build_recipe_filters(user_profile: dict) -> dict:
    """
    Translates user health conditions into Spoonacular API filter parameters.
    
    Args:
        user_profile: Dictionary containing user profile with health constraints.
            Expected structure:
            {
                "health_constraints": {
                    "condition": "diabetes" | "hypertension" | "muscle_build" | ...
                }
            }
    
    Returns:
        Dictionary of filter parameters for the Spoonacular API.
        
    Example:
        >>> build_recipe_filters({"health_constraints": {"condition": "diabetes"}})
        {'maxSugar': 5, 'minFiber': 5}
    """
    filters = {}
    
    health_constraints = user_profile.get('health_constraints', {})
    condition = health_constraints.get('condition')
    
    # Health condition to API filter mapping
    # These values are based on general dietary guidelines
    CONDITION_MAPPING = {
        # Diabetes: Low sugar, high fiber helps regulate blood sugar
        'diabetes': {
            'maxSugar': 5,      # grams per serving
            'minFiber': 5,      # grams per serving
            'maxCarbs': 45,     # grams per serving
        },
        # Hypertension: Low sodium for blood pressure control
        'hypertension': {
            'maxSodium': 400,   # mg per serving
            'maxSaturatedFat': 5,  # grams per serving
        },
        # Muscle building: High protein for muscle synthesis
        'muscle_build': {
            'minProtein': 30,   # grams per serving
            'minCalories': 300, # calories per serving
        },
        # Heart health: Low cholesterol and saturated fat
        'heart_disease': {
            'maxCholesterol': 50,   # mg per serving
            'maxSaturatedFat': 3,   # grams per serving
            'maxSodium': 400,       # mg per serving
        },
        # Weight loss: Calorie controlled, high protein, high fiber
        'weight_loss': {
            'maxCalories': 400,     # calories per serving
            'minProtein': 20,       # grams per serving
            'minFiber': 5,          # grams per serving
        },
        # Kidney health: Low protein, low sodium, low potassium
        'kidney_disease': {
            'maxProtein': 15,       # grams per serving
            'maxSodium': 300,       # mg per serving
        },
    }
    
    if condition in CONDITION_MAPPING:
        filters.update(CONDITION_MAPPING[condition])
    
    # Handle dietary restrictions (allergies, preferences)
    intolerances = health_constraints.get('intolerances', [])
    if intolerances:
        # Spoonacular accepts comma-separated intolerances
        filters['intolerances'] = ','.join(intolerances)
    
    # Handle diet type (vegetarian, vegan, etc.)
    diet = health_constraints.get('diet')
    if diet:
        filters['diet'] = diet
    
    return filters


def validate_recipe_for_user(recipe: dict, user_profile: dict) -> dict:
    """
    Post-filter validation: checks if a recipe meets user's health constraints.
    Returns analysis with warnings if any nutrients exceed limits.
    
    Args:
        recipe: Recipe data from Spoonacular
        user_profile: User profile with health constraints
        
    Returns:
        Dictionary with validation result and any warnings
    """
    warnings = []
    filters = build_recipe_filters(user_profile)
    
    nutrition = recipe.get('nutrition', {})
    nutrients = {n['name'].lower(): n['amount'] for n in nutrition.get('nutrients', [])}
    
    # Check each filter against actual recipe nutrition
    filter_nutrient_mapping = {
        'maxSugar': ('sugar', 'high'),
        'minFiber': ('fiber', 'low'),
        'maxCarbs': ('carbohydrates', 'high'),
        'maxSodium': ('sodium', 'high'),
        'maxSaturatedFat': ('saturated fat', 'high'),
        'minProtein': ('protein', 'low'),
        'maxCholesterol': ('cholesterol', 'high'),
        'maxCalories': ('calories', 'high'),
        'minCalories': ('calories', 'low'),
    }
    
    for filter_key, (nutrient_name, direction) in filter_nutrient_mapping.items():
        if filter_key in filters:
            limit = filters[filter_key]
            actual = nutrients.get(nutrient_name, 0)
            
            if direction == 'high' and actual > limit:
                warnings.append(f"{nutrient_name.title()}: {actual}g exceeds limit of {limit}g")
            elif direction == 'low' and actual < limit:
                warnings.append(f"{nutrient_name.title()}: {actual}g below minimum of {limit}g")
    
    return {
        'valid': len(warnings) == 0,
        'warnings': warnings
    }
