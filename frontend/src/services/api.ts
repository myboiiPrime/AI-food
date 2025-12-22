import axios from 'axios';
import { Platform } from 'react-native';

// In Expo Go on Android, localhost is 10.0.2.2. On iOS it is localhost.
// However, when running on a physical device, you need the actual local IP.
// The user specified http://<YOUR_LOCAL_IP>:5000.
// We'll use an environment variable or a default placeholder.

const BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.1.XX:5000'; // Placeholder

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface DetectResponse {
  success: boolean;
  ingredients: string[];
}

export interface AnalyzeRequest {
  ingredients: string[];
  user_profile: {
    health_constraints: {
      condition: string;
    };
  };
}

export const detectIngredients = async (base64Image: string): Promise<string[]> => {
  try {
    const response = await api.post<DetectResponse>('/api/detect', { image: base64Image });
    if (response.data.success) {
      return response.data.ingredients;
    }
    return [];
  } catch (error) {
    console.error('API Error: detect', error);
    throw error;
  }
};

export const analyzeRecipes = async (data: AnalyzeRequest) => {
  try {
    const response = await api.post('/api/analyze', data);
    return response.data;
  } catch (error) {
    console.error('API Error: analyze', error);
    throw error;
  }
};

export const getNutrition = async (ingredients: string[]) => {
  try {
    const response = await api.post('/api/nutrition', { ingredients });
    return response.data;
  } catch (error) {
    console.error('API Error: nutrition', error);
    throw error;
  }
};

export default api;
