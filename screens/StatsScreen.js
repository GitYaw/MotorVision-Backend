import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ActivityIndicator } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { collection, getDocs } from "firebase/firestore";
import { database } from "../config/firebase";

export default function StatsScreen() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const querySnapshot = await getDocs(collection(database, "stats"));
        if (!querySnapshot.empty) {
          setStats(querySnapshot.docs[0].data()); // Just get the first document
        }
      } catch (error) {
        console.error("Firestore Error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#00bfff" />
      </View>
    );
  }

  return (
    <LinearGradient colors={["#121212", "#1E1E1E", "#292929"]} style={styles.container}>
      <Text style={styles.title}>📊 Stats</Text>
      {stats ? (
        <Text style={styles.text}>Distance: {stats.distance} miles</Text>
      ) : (
        <Text style={styles.text}>No data found</Text>
      )}
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
    fontSize: 24,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 10,
  },
  text: {
    fontSize: 18,
    color: "#bbb",
  },
});