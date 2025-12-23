import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Alert, TextInput, ScrollView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';

const CONDITIONS = [
  { id: 'diabetes', label: 'Manage Diabetes', emoji: '🩸' },
  { id: 'muscle_build', label: 'Build Muscle', emoji: '💪' },
  { id: 'heart_disease', label: 'Heart Health', emoji: '❤️' },
  { id: 'weight_loss', label: 'Weight Loss', emoji: '⚖️' },
  { id: 'none', label: 'No Restrictions', emoji: '✅' },
];

export default function ProfileScreen() {
  const [selectedCondition, setSelectedCondition] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const condition = await AsyncStorage.getItem('health_condition');
      if (condition) setSelectedCondition(condition);
    } catch (e) {
      console.error('Failed to load profile', e);
    }
  };

  const saveProfile = async (conditionId: string) => {
    try {
      setSelectedCondition(conditionId);
      await AsyncStorage.setItem('health_condition', conditionId);
      Alert.alert('Profile Saved', `Your goal is set to: ${CONDITIONS.find(c => c.id === conditionId)?.label}`);
    } catch (e) {
      Alert.alert('Error', 'Failed to save profile');
    }
  };

  return (
    <ScrollView className="flex-1 bg-white p-6">
      <Text className="text-2xl font-bold text-gray-800 mb-2">Health Goals</Text>
      <Text className="text-gray-600 mb-8 text-lg">
        Select a health goal so we can tailor recipes for you.
      </Text>

      <View className="gap-4">
        {CONDITIONS.map((condition) => (
          <TouchableOpacity
            key={condition.id}
            className={`p-5 rounded-xl border-2 flex-row items-center gap-4 ${
              selectedCondition === condition.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 bg-white'
            }`}
            onPress={() => saveProfile(condition.id)}
          >
            <Text className="text-3xl">{condition.emoji}</Text>
            <View>
              <Text className={`text-xl font-semibold ${
                selectedCondition === condition.id ? 'text-blue-700' : 'text-gray-700'
              }`}>
                {condition.label}
              </Text>
            </View>
            {selectedCondition === condition.id && (
              <View className="ml-auto bg-blue-500 rounded-full w-6 h-6 items-center justify-center">
                <Text className="text-white font-bold">✓</Text>
              </View>
            )}
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity
        className="mt-8 bg-gray-100 p-4 rounded-xl items-center"
        onPress={() => router.back()}
      >
        <Text className="text-gray-700 font-bold text-lg">Done</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}
