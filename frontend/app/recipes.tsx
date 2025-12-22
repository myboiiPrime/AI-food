import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, Image, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Mock Data for Prototype
const MOCK_RECIPES = [
  {
    id: 1,
    title: 'Spinach & Egg Scramble',
    image: 'https://via.placeholder.com/150',
    tags: ['diabetes', 'muscle_build', 'keto'],
    time: '15 min',
    cals: '320 kcal',
    description: 'A quick and healthy breakfast option rich in protein and fiber.'
  },
  {
    id: 2,
    title: 'Tomato & Onion Omelet',
    image: 'https://via.placeholder.com/150',
    tags: ['vegetarian', 'gluten_free'],
    time: '10 min',
    cals: '250 kcal',
    description: 'Classic omelet with fresh garden vegetables.'
  },
  {
    id: 3,
    title: 'Bell Pepper Stuffed with Egg',
    image: 'https://via.placeholder.com/150',
    tags: ['low_carb', 'diabetes'],
    time: '25 min',
    cals: '180 kcal',
    description: 'Colorful and nutritious, perfect for a light lunch.'
  },
];

export default function RecipesScreen() {
  const { ingredients } = useLocalSearchParams();
  const [loading, setLoading] = useState(true);
  const [recipes, setRecipes] = useState<any[]>([]);
  const [userCondition, setUserCondition] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    // Simulate API delay
    try {
      const condition = await AsyncStorage.getItem('health_condition');
      setUserCondition(condition);

      setTimeout(() => {
        setRecipes(MOCK_RECIPES);
        setLoading(false);
      }, 1500);
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  };

  const isConditionSafe = (recipeTags: string[]) => {
    if (!userCondition || userCondition === 'none') return false;
    // Simple check: if the condition is in the tags, it's explicitly good.
    // In a real app, the backend logic would be more complex.
    // For this prototype, we check if the tag matches the condition.
    return recipeTags.includes(userCondition);
  };

  const getConditionLabel = () => {
    switch(userCondition) {
      case 'diabetes': return 'Diabetes Safe';
      case 'muscle_build': return 'High Protein';
      case 'heart_disease': return 'Heart Friendly';
      case 'weight_loss': return 'Low Calorie';
      default: return '';
    }
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-50">
        <ActivityIndicator size="large" color="#16a34a" />
        <Text className="mt-4 text-gray-600 font-medium">Analyzing your ingredients...</Text>
        <Text className="text-gray-400 text-sm mt-1">Checking against your health profile</Text>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-gray-50 p-4">
      <Text className="text-2xl font-bold text-gray-800 mb-6 px-2">Recommended for You</Text>

      <View className="gap-6 pb-8">
        {recipes.map((recipe) => (
          <View key={recipe.id} className="bg-white rounded-3xl shadow-sm overflow-hidden border border-gray-100">
            {/* Image Placeholder */}
            <View className="h-48 bg-gray-200 w-full relative">
               {/* Badge if safe */}
               {isConditionSafe(recipe.tags) && (
                 <View className="absolute top-4 left-4 bg-green-500 px-3 py-1 rounded-full shadow-md z-10">
                   <Text className="text-white font-bold text-xs uppercase tracking-wide">
                     ✓ {getConditionLabel()}
                   </Text>
                 </View>
               )}
               {/* Image would go here */}
               <View className="flex-1 items-center justify-center">
                 <Text className="text-gray-400">Recipe Image</Text>
               </View>
            </View>

            <View className="p-5">
              <View className="flex-row justify-between items-start mb-2">
                <Text className="text-xl font-bold text-gray-800 flex-1 mr-2">{recipe.title}</Text>
                <View className="bg-orange-100 px-2 py-1 rounded-lg">
                  <Text className="text-orange-700 text-xs font-bold">{recipe.time}</Text>
                </View>
              </View>

              <Text className="text-gray-600 mb-4 leading-relaxed">{recipe.description}</Text>

              <View className="flex-row items-center justify-between mt-2 pt-4 border-t border-gray-100">
                 <Text className="text-gray-500 font-medium">{recipe.cals}</Text>
                 <TouchableOpacity className="bg-gray-900 px-5 py-2 rounded-full">
                   <Text className="text-white font-bold">View Recipe</Text>
                 </TouchableOpacity>
              </View>
            </View>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}
