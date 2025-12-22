import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { Link, useRouter } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function Hub() {
  const router = useRouter();

  return (
    <View className="flex-1 bg-gray-50 p-6">
      <StatusBar style="auto" />
      <View className="mb-8 mt-4">
        <Text className="text-4xl font-bold text-gray-800">Hello,</Text>
        <Text className="text-2xl text-gray-600">What are we cooking today?</Text>
      </View>

      <View className="flex-1 gap-6">
        {/* Primary Action: Snap & Cook */}
        <TouchableOpacity
          className="bg-green-600 p-8 rounded-3xl shadow-lg flex items-center justify-center h-48"
          onPress={() => router.push('/snap')}
        >
          <View className="bg-white/20 p-4 rounded-full mb-2">
             <Text className="text-4xl">📸</Text>
          </View>
          <Text className="text-white text-3xl font-bold">Snap & Cook</Text>
          <Text className="text-green-100 text-lg text-center mt-2">Scan your ingredients</Text>
        </TouchableOpacity>

        {/* Secondary Action: My Health Profile */}
        <TouchableOpacity
          className="bg-blue-600 p-6 rounded-2xl shadow-md flex-row items-center justify-between"
          onPress={() => router.push('/profile')}
        >
          <View className="flex-row items-center gap-4">
            <Text className="text-3xl">❤️</Text>
            <View>
              <Text className="text-white text-xl font-bold">My Health Profile</Text>
              <Text className="text-blue-100">Manage dietary needs</Text>
            </View>
          </View>
          <Text className="text-white text-2xl">›</Text>
        </TouchableOpacity>

        {/* Info Card */}
        <View className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mt-auto">
          <Text className="text-gray-800 font-bold text-lg mb-2">Did you know?</Text>
          <Text className="text-gray-600">
            Scanning your pantry can help reduce food waste by up to 30%.
          </Text>
        </View>
      </View>
    </View>
  );
}
