import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, FlatList } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

// this page is good

// this is the instructions
const data = [
  {id: '1', name: "1. Turn on your mobile phone's bluetooth feature."},
  {id: '2', name: "2. Navigate to your mobile phone's bluetooth device settings."},
  {id: '3', name: "3. Identify a bluetooth device titled HC-05."},
  {id: '4', name: "4. Connect to the bluetooth device, and enter the password for the device if prompted."},
  {id: '5', name: "5. Go back to the Change Device screen to see if the device showed up."},
]

export default function InstructionsPairNewDevice({navigation }) {

  return (
    <LinearGradient
      colors={['#121212', '#1E1E1E', '#292929']} // Gradient effect
      style={styles.container}
    >
      <View style={styles.paddingTop}>
      <Text style={styles.title}> How to Pair a New Device to Phone</Text>
      <Text style={styles.title}> </Text>

      {/* <View style={styles.container}> */}
      <FlatList
        data={data}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text style={styles.instructionsText}>{item.name}</Text>
          </View>
        )}
      />
    {/* </View> */}

    
      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Back to Change New Device</Text>
      </TouchableOpacity>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    paddingTop: 40,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
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
  },
  item: {
    backgroundColor: '#1e1e1e',
    borderRadius: 12,
    padding: 15,
    marginVertical: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
    borderWidth: 1,
    borderColor: '#00bfff', // Border color to make the box pop
  },
  instructionsText: {
    fontSize: 18,
    color: '#fff',
    fontWeight: 'bold',

  },
  paddingContainer: {
    flex: 1,
    paddingTop: 50,
    justifyContent: 'center',
  }
});
