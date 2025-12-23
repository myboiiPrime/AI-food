import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView, TextInput } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';

export default function IngredientsScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [newItem, setNewItem] = useState('');

  useEffect(() => {
    if (params.detected) {
      try {
        const parsed = JSON.parse(params.detected as string);
        setIngredients(parsed);
      } catch (e) {
        console.error('Failed to parse ingredients', e);
      }
    } else {
      // Fallback/Mock data if came directly
      setIngredients(['Tomato', 'Egg', 'Onion']);
    }
  }, [params.detected]);

  const removeIngredient = (index: number) => {
    const newIngredients = [...ingredients];
    newIngredients.splice(index, 1);
    setIngredients(newIngredients);
  };

  const addIngredient = () => {
    if (newItem.trim().length > 0) {
      setIngredients([...ingredients, newItem.trim()]);
      setNewItem('');
    }
  };

  const findRecipes = () => {
    router.push({
      pathname: '/recipes',
      params: {
        ingredients: JSON.stringify(ingredients)
      }
    });
  };

  return (
    <View className="flex-1 bg-white">
      <ScrollView className="flex-1 p-6">
        <Text className="text-2xl font-bold text-gray-800 mb-2">Ingredients Found</Text>
        <Text className="text-gray-600 mb-6 text-lg">
          We found these items. Add or remove any to get the best recipes.
        </Text>

        <View className="flex-row flex-wrap gap-3 mb-8">
          {ingredients.map((item, index) => (
            <View key={index} className="bg-green-50 border border-green-200 rounded-full px-4 py-2 flex-row items-center">
              <Text className="text-green-800 text-lg mr-2 capitalize">{item}</Text>
              <TouchableOpacity onPress={() => removeIngredient(index)} hitSlop={10}>
                <Text className="text-green-600 font-bold text-lg">×</Text>
              </TouchableOpacity>
            </View>
          ))}
          {ingredients.length === 0 && (
            <Text className="text-gray-400 italic">No ingredients listed yet.</Text>
          )}
        </View>

        <View className="flex-row gap-3 items-center mb-8">
          <TextInput
            className="flex-1 border-2 border-gray-200 rounded-xl px-4 py-3 text-lg bg-gray-50"
            placeholder="Add another item..."
            value={newItem}
            onChangeText={setNewItem}
            onSubmitEditing={addIngredient}
          />
          <TouchableOpacity
            className="bg-gray-800 p-4 rounded-xl"
            onPress={addIngredient}
          >
            <Text className="text-white font-bold text-lg">+</Text>
          </TouchableOpacity>
        </View>

      </ScrollView>

      <View className="p-6 border-t border-gray-100 bg-white shadow-lg">
        <TouchableOpacity
          className="bg-green-600 p-5 rounded-2xl items-center shadow-md"
          onPress={findRecipes}
        >
          <Text className="text-white text-2xl font-bold">Find Recipes</Text>
          <Text className="text-green-100">Using {ingredients.length} ingredients</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
