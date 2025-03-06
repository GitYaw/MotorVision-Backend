import { 
  View, 
  Button, 
  Easing, 
  Text, 
  ScrollView, 
  Animated, 
  Image, 
  StyleSheet, 
  Platform, 
  PermissionsAndroid, 
  ActivityIndicator, 
  TouchableOpacity,
  StatusBar 
} from "react-native";

// AI Generation used to resolve syntax issues, and to develop template for script.
import React, { useEffect, useRef, useState } from "react";
// import Geolocation from "react-native-geolocation-service";

import axios from "axios";

import * as Location from "expo-location";

/* Smart Button -> connect this to a rest API (connect rest api)
const SmartHelmetButton = () => {
  const [buttonText, setButtonText] = useState('Connect to SmartHelmet?');

  return (
    // add a call to a rest API
    
    
    <TouchableOpacity
      style={styles.button}
      onPress={() => setButtonText('Connected to SmartHelmet!')}
    >
      <Text style={styles.buttonText}>{buttonText}</Text>
    </TouchableOpacity>
  );
}; */

const SmartHelmetButton = () => {
  const [buttonText, setButtonText] = useState('Connect to SmartHelmet?');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Function to handle the API call when the button is pressed
  const handleButtonPress = async () => {
    setLoading(true);  // Show loading state
    setError(null);     // Clear previous error state

    try {
      // Make the API call here (replace with your actual endpoint)
      const response = await axios.get('http://127.0.0.1:8000/connect/');
      
      // Assume the response has a boolean field `success`
      const isConnected = response.data.message;

      setButtonText(response.data.message)
    } catch (err) {
      setError('Error with API/Bluetooth Connection: ' + err);
      // setButtonText('Connected to SmartHelmet!'); // Optional: Update button to show error
    } finally {
      setLoading(false); // Hide loading state
    }
  };

  return (
    <TouchableOpacity
      style={styles.button}
      onPress={handleButtonPress} // Call the async function on press
    >
      {/* Show loading or error message if applicable */}
      <Text style={styles.buttonText}>
        {loading ? 'Connecting...' : error || buttonText}
      </Text>
    </TouchableOpacity>
  );
};



// Rotating image component
function RotatingImageComponent({ isRotating, stopRotation }) {
  const rotateValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    let animation;
    if (isRotating) {
      animation = Animated.loop(
        Animated.timing(rotateValue, {
          toValue: 1,
          duration: 40000,
          easing: Easing.linear,
          useNativeDriver: true,
        })
      ).start();
    } else {
      if (animation) {
        animation.stop();
      }
    }

    return () => {
      if (animation) {
        animation.stop();
      }
    };
  }, [isRotating]);

  const rotateInterpolation = rotateValue.interpolate({
    inputRange: [0, 0.25],
    outputRange: ["0deg", "360deg"],
  });

  return (
    <View style={{ alignItems: "center", gap: 10 }}>
      <Animated.Image
        source={require("../assets/Car.png")} // Changed from SVG to PNG (React Native doesn't support require() for SVGs)
        style={{ width: 100, height: 100, transform: [{ perspective: 800 }, { rotateY: rotateInterpolation }] }}
      />


    </View>
  );
}

function RotatingImage() {
  const [isRotating, setIsRotating] = useState(true);

  const stopRotation = () => setIsRotating(false);

  return <RotatingImageComponent isRotating={isRotating} stopRotation={stopRotation} />;
}

// Location Component
function LocationView() {
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const requestPermissionAndGetLocation = async () => {
      const hasPermission = await requestLocationPermission();
      if (!hasPermission) {
        setError("Location permission denied");
        setLoading(false);
        return;
      }

      try {
        const position = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.High,
        });

        setLocation({
          latitude: parseFloat(position.coords.latitude.toFixed(2)),
          longitude: parseFloat(position.coords.longitude.toFixed(2)),
          accuracy: position.coords.accuracy,
        });
      } catch (err) {
        setError(err.message);
      }

      setLoading(false);
    };

    requestPermissionAndGetLocation();
  }, []);

  const requestLocationPermission = async () => {
    const { status } = await Location.requestForegroundPermissionsAsync();
    return status === "granted";
  };

  if (loading) return <ActivityIndicator size="large" color="blue" />;
  if (error) return <Text>Error: {error}</Text>;

  return (
    <View style={styles.locationContainer}>
      {loading && <ActivityIndicator size="large" />}
      {error && <Text style={{ color: "red" }}>Error: {error}</Text>}
      {location ? (
        <View>
          <Text style={styles.bodyText}>🌍 {location.latitude}°, {location.longitude}°</Text>
        </View>
      ) : (
        !loading && <Text>No location data available.</Text>
      )}
    </View>
  );
}

export default function HomeScreen({navigation}) {
  return (
    <ScrollView style={styles.scrollView}>
      <View style={styles.titleContainer}>
        <Text style={styles.titleText}>MotorVision</Text>
      </View>
      <View style={styles.stepContainer}></View>
      <LocationView /> {/* Added Location Component */}
      <View style={styles.helmetContainer}>
        <Text style={styles.connectText}>Connect to a Paired Device</Text>
      </View>
      <View style={styles.helmetContainer}>
        <RotatingImage />
      </View>
      <SmartHelmetButton />
      <TouchableOpacity
          style={styles.button}
            onPress={() => navigation.navigate('ConnectDeviceScreen')}
          >
            <Text style={styles.buttonText}>Change Device</Text>
      </TouchableOpacity>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  locationContainer: {
    marginTop: 10,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "transparent",
  },
  bodyText: {
    fontSize: 20,
    fontWeight: "bold",
    textAlign: "center",
    color: "white",
  },
  application: {
    flex: 1,
    backgroundColor: "#F3F3F3",
  },
  titleContainer: {
    marginTop: 100,
    marginBottom: 0,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "transparent",
  },
  titleText: {
    fontSize: 60,
    fontWeight: "bold",
    textAlign: "center",
    color: "white",
  },
  stepContainer: {
    marginTop: 5,
    marginBottom: 5,
    flexDirection: "row",
    alignItems: "center",
    fontWeight: "bold",
    justifyContent: "center",
    backgroundColor: "transparent",
  },
  helmetContainer: {
    marginTop: 20,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "transparent",
  },
  buttonContainer: {
    marginTop: 20,
    marginLeft: 20,
    marginRight: 20,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "transparent",
  },
  connectText: {
    fontSize: 30,
    fontWeight: "bold",
    textAlign: "center",
    color: "white",
  },
  locationContainer: {
    marginTop: 20,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "transparent",
  },
  bodyText: {
    fontSize: 20,
    textAlign: "center",
    color: "white",
  },
  scrollView: {
    flex: 1,
    backgroundColor: "#121212",
    padding: 20,
  },
  button: {
    marginTop: 20,
    marginLeft: 10,
    marginRight: 10,
    backgroundColor: '#00bfff',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
    shadowColor: '#00bfff',
    shadowOpacity: 0.5,
    shadowRadius: 10,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: "center"
  },
});
