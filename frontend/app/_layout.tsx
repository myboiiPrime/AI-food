import '../global.css';
import { Stack } from 'expo-router';
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function Layout() {
  return (
    <SafeAreaProvider>
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: '#fff',
          },
          headerTintColor: '#000',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen name="index" options={{ title: 'Pantry Chef' }} />
        <Stack.Screen name="profile" options={{ title: 'My Health Profile' }} />
        <Stack.Screen name="snap" options={{ title: 'Snap & Cook' }} />
        <Stack.Screen name="ingredients" options={{ title: 'Review Ingredients' }} />
        <Stack.Screen name="recipes" options={{ title: 'Recipe Feed' }} />
      </Stack>
    </SafeAreaProvider>
  );
}
