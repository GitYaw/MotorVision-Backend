import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

// Initialize Firebase
const firebaseConfig = {
	apiKey: "AIzaSyAgkbN5aBR-xNswI2uo8WUNhs5E2dOykCI",
	authDomain: "motor-vision-backend.firebaseapp.com",
	projectId: "motor-vision-backend",
	storageBucket: "motor-vision-backend.firebasestorage.app",
	messagingSenderId: "1015734436024",
	appId: "1:1015734436024:web:88cdadc74f40ad91f7f44d",
	measurementId: "G-2EJHJC6QLF"
};

const app = initializeApp(firebaseConfig);
const database = getFirestore(app)

export { database }

// see the Firebase documentation: https://firebase.google.com/docs/web/setup#access-firebase