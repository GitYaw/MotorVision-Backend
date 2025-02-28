import React, { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function CrashRecordingScreen({ navigation }) {
  const [isRecording, setIsRecording] = useState(false);
  const [startTime, setStartTime] = useState(null);

  const toggleRecording = async () => {
    if (isRecording) {
      // Stopping Recording
      const endTime = new Date();
      const duration = (endTime - startTime) / 1000; // Duration in seconds

      // Only store last 5 minutes (300 seconds) of recording
      const finalDuration = duration > 300 ? 300 : duration;

      // Create new log entry
      const newLog = {
        id: Date.now().toString(),
        timestamp: endTime.toLocaleString(),
        duration: finalDuration,
        details: `Crash data recorded for ${Math.round(finalDuration)} seconds`,
      };

      try {
        // Retrieve existing logs
        const existingLogs = await AsyncStorage.getItem("crashLogs");
        const logs = existingLogs ? JSON.parse(existingLogs) : [];

        // Save new log
        logs.unshift(newLog);
        await AsyncStorage.setItem("crashLogs", JSON.stringify(logs));
      } catch (error) {
        console.error("Error saving log:", error);
      }

      setIsRecording(false);
      setStartTime(null);

      // Navigate to crash logs after stopping
      navigation.navigate("CrashLogs");
    } else {
      // Starting Recording
      setStartTime(new Date());
      setIsRecording(true);
    }
  };

  return (
    <LinearGradient colors={["#121212", "#1E1E1E", "#292929"]} style={styles.container}>
      <Text style={styles.title}>MotorVision</Text>
      <Text style={styles.status}>
        {isRecording ? "Recording Crash Data..." : "Tap to Start Recording"}
      </Text>

      <TouchableOpacity
        style={[styles.button, isRecording ? styles.buttonActive : styles.buttonInactive]}
        onPress={toggleRecording}
      >
        <Text style={styles.buttonText}>{isRecording ? "Stop" : "Start"}</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.linkButton} onPress={() => navigation.navigate("CrashLogs")}>
        <Text style={styles.linkText}>View Crash Reports</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 10,
  },
  status: {
    fontSize: 16,
    color: "#bbb",
    marginBottom: 30,
  },
  button: {
    width: 180,
    height: 60,
    borderRadius: 30,
    justifyContent: "center",
    alignItems: "center",
    shadowOpacity: 0.6,
    shadowRadius: 10,
  },
  buttonActive: {
    backgroundColor: "red",
    shadowColor: "red",
  },
  buttonInactive: {
    backgroundColor: "#00bfff",
    shadowColor: "#00bfff",
  },
  buttonText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#fff",
  },
  linkButton: {
    marginTop: 20,
  },
  linkText: {
    fontSize: 16,
    color: "#00bfff",
    textDecorationLine: "underline",
  },
});
