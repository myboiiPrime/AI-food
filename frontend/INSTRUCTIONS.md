# Pantry Chef - Run Instructions

## Prerequisites

1.  **Node.js**: Ensure you have Node.js installed.
2.  **Python**: Ensure you have Python installed for the backend.
3.  **Expo Go**: Install the "Expo Go" app on your Android or iOS device.

## 1. Start the Backend

Open a terminal and navigate to the `backend` folder:

```bash
cd backend
# Install dependencies (if you haven't already)
pip install -r requirements.txt
# Run the server
python app.py
```

The backend should be running at `http://localhost:5000` (or `http://127.0.0.1:5000`).

## 2. Configure Frontend API URL

Since you are running the app on a mobile device (Expo Go), `localhost` refers to the phone itself, not your computer. You must use your computer's **Local IP Address**.

1.  Find your local IP address:
    *   **Mac/Linux**: Run `ifconfig` (look for `en0` or `wlan0` -> `inet`).
    *   **Windows**: Run `ipconfig` (look for "IPv4 Address").
    *   Example: `192.168.1.5`

2.  Open `frontend/src/services/api.ts`.
3.  Update the `BASE_URL` (or set `EXPO_PUBLIC_API_URL`):

    ```typescript
    // Replace with YOUR IP address
    const BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.1.5:5000';
    ```

## 3. Run the Frontend

Open a new terminal and navigate to the `frontend` folder:

```bash
cd frontend
# Install dependencies
npm install

# Start the Expo development server
npx expo start
```

## 4. Connect with Mobile

1.  You will see a **QR Code** in the terminal.
2.  Open **Expo Go** on your phone.
3.  **Android**: Tap "Scan QR Code" and scan the terminal code.
4.  **iOS**: Open the Camera app, scan the code, and tap the notification to open in Expo Go.

## Troubleshooting

*   **"Java boolean" Error**: This usually means a native library version mismatch. If you see this, run `npx expo install --fix` in the `frontend` directory to align versions.
*   **Network Request Failed**:
    *   Ensure your phone and computer are on the **same Wi-Fi network**.
    *   Ensure your computer's firewall accepts connections on port 5000 and 8081.
*   **Styles not loading**: Ensure you have run `npm install` to set up NativeWind.
