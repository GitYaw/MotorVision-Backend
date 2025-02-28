import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { Ionicons } from "@expo/vector-icons";

// Import Screens
import HomeScreen from "./screens/HomeScreen";
import CrashLogsScreen from "./screens/CrashLogsScreen";
import CrashDetailScreen from "./screens/CrashDetailScreen";
import StatsScreen from "./screens/StatsScreen";
import CrashRecordingScreen from "./screens/CrashRecordingScreen";

// Create Stack Navigator for Crash Data (Crash Logs + Crash Recording)
const CrashStack = createStackNavigator();
function CrashStackNavigator() {
  return (
    <CrashStack.Navigator screenOptions={{ headerShown: false }}>
      <CrashStack.Screen name="CrashRecording" component={CrashRecordingScreen} />
      <CrashStack.Screen name="CrashLogs" component={CrashLogsScreen} />
      <CrashStack.Screen name="CrashDetail" component={CrashDetailScreen} />
    </CrashStack.Navigator>
  );
}

// Create Bottom Tab Navigator
const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        initialRouteName="Home"
        screenOptions={({ route }) => ({
          tabBarIcon: ({ color, size }) => {
            let iconName;

            if (route.name === "Home") {
              iconName = "home-outline";
            } else if (route.name === "Stats") {
              iconName = "bar-chart-outline";
            } else if (route.name === "Crash Data") {
              iconName = "alert-circle-outline";
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarStyle: { backgroundColor: "#1E1E1E", borderTopColor: "transparent" },
          tabBarActiveTintColor: "#00bfff",
          tabBarInactiveTintColor: "#bbb",
          headerShown: false,
        })}
      >
        <Tab.Screen name="Stats" component={StatsScreen} />
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Crash Data" component={CrashStackNavigator} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
