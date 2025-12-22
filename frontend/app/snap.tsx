import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, ActivityIndicator } from 'react-native';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useRouter } from 'expo-router';

export default function SnapScreen() {
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [isScanning, setIsScanning] = useState(false);
  const router = useRouter();
  const cameraRef = React.useRef<CameraView>(null);

  if (!permission) {
    // Camera permissions are still loading.
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View className="flex-1 justify-center items-center p-6 bg-white">
        <Text className="text-xl text-center mb-4 text-gray-800">We need your permission to show the camera</Text>
        <TouchableOpacity
          className="bg-blue-600 px-6 py-3 rounded-full"
          onPress={requestPermission}
        >
          <Text className="text-white font-bold text-lg">Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        setIsScanning(true);
        const photo = await cameraRef.current.takePictureAsync({
          base64: true,
          quality: 0.5,
        });

        // Mock API call delay
        setTimeout(() => {
          setIsScanning(false);
          // Navigate to ingredients page with mock data
          // In real app, we would pass the API response
          router.push({
            pathname: '/ingredients',
            params: {
              detected: JSON.stringify(['Tomato', 'Egg', 'Onion', 'Bell Pepper']),
              imageUri: photo?.uri
            }
          });
        }, 2000);

      } catch (error) {
        console.error(error);
        setIsScanning(false);
      }
    }
  };

  function toggleCameraFacing() {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  }

  return (
    <View className="flex-1 bg-black">
      {isScanning ? (
        <View className="flex-1 items-center justify-center bg-black/80">
          <ActivityIndicator size="large" color="#4ade80" />
          <Text className="text-white text-2xl font-bold mt-4">Scanning Ingredients...</Text>
          <Text className="text-gray-300 text-lg mt-2">Identifying food items</Text>
        </View>
      ) : (
        <CameraView style={{ flex: 1 }} facing={facing} ref={cameraRef}>
          <View className="flex-1 bg-transparent justify-end pb-12 px-6">
             <View className="flex-row justify-between items-center mb-8">
               <TouchableOpacity
                  className="bg-black/40 p-4 rounded-full"
                  onPress={toggleCameraFacing}
                >
                  <Text className="text-white text-lg">Flip</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  className="w-20 h-20 bg-white rounded-full border-4 border-gray-300 items-center justify-center"
                  onPress={takePicture}
                >
                  <View className="w-16 h-16 bg-white rounded-full border-2 border-black" />
                </TouchableOpacity>

                <TouchableOpacity
                  className="bg-black/40 p-4 rounded-full"
                  onPress={() => router.back()}
                >
                  <Text className="text-white text-lg">Cancel</Text>
                </TouchableOpacity>
             </View>
             <Text className="text-white text-center text-lg bg-black/50 py-2 rounded-lg">
               Center food items in the frame
             </Text>
          </View>
        </CameraView>
      )}
    </View>
  );
}
