import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function CrashDetailScreen({ route, navigation }) {
  const { crash } = route.params;

  return (
    <LinearGradient
      colors={['#121212', '#1E1E1E', '#292929']} // Gradient effect
      style={styles.container}
    >
      <Text style={styles.title}>Crash Details</Text>

      <View style={styles.detailBox}>
        <Text style={styles.info}>🕒 Time: {crash.timestamp}</Text>
        <Text style={styles.info}>⚠️ Details: {crash.details}</Text>
      </View>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Back to Crash Logs</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 20,
    textAlign: 'center',
  },
  detailBox: {
    backgroundColor: '#1E1E1E',
    padding: 20,
    borderRadius: 12,
    shadowColor: '#00bfff',
    shadowOpacity: 0.4,
    shadowRadius: 8,
  },
  info: {
    fontSize: 16,
    color: '#fff',
    marginBottom: 10,
  },
  button: {
    marginTop: 20,
    backgroundColor: '#00bfff',
    paddingVertical: 12,
    borderRadius: 30,
    alignItems: 'center',
    shadowColor: '#00bfff',
    shadowOpacity: 0.5,
    shadowRadius: 10,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
  },
});
