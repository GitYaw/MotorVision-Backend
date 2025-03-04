import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";

export default function HomeScreen({ navigation }) {
  return (
    <LinearGradient
      colors={["#121212", "#1E1E1E", "#292929"]} // Gradient Background
      style={styles.container}
    >
      {/* Helmet Status */}
      <View style={styles.statusContainer}>
        <Text style={styles.statusText}>🔋 Helmet Battery: 85%</Text>
        <Text style={[styles.statusText, { color: "#00ff00" }]}>🟢 Connected</Text>
      </View>

      {/* Voice Control */}
      <View style={styles.voiceContainer}>
        <Text style={styles.label}>Tap to Speak</Text>
        <TouchableOpacity style={styles.voiceButton}>
          <Ionicons name="mic-outline" size={40} color="white" />
        </TouchableOpacity>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  statusContainer: {
    position: "absolute",
    top: 60,
    alignItems: "center",
  },
  statusText: {
    color: "#fff",
    fontSize: 18,
    marginVertical: 5,
  },
  voiceContainer: {
    alignItems: "center",
    marginBottom: 40,
  },
  label: {
    color: "#bbb",
    fontSize: 18,
    marginBottom: 10,
  },
  voiceButton: {
    backgroundColor: "#007bff",
    padding: 20,
    borderRadius: 50,
    shadowColor: "#007bff",
    shadowOpacity: 0.6,
    shadowRadius: 10,
    elevation: 5,
  },
  controls: {
    position: "absolute",
    bottom: 60,
    width: "100%",
    alignItems: "center",
  },
  button: {
    backgroundColor: "#4caf50",
    padding: 15,
    width: "80%",
    borderRadius: 12,
    alignItems: "center",
    marginVertical: 10,
    shadowColor: "#4caf50",
    shadowOpacity: 0.5,
    shadowRadius: 8,
    elevation: 5,
  },
  crashButton: {
    backgroundColor: "#d32f2f",
    shadowColor: "#d32f2f",
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
});

