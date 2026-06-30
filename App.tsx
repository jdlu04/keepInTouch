import 'react-native-url-polyfill/auto';
import { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Session } from '@supabase/supabase-js';

import { supabase } from './lib/supabase';
import type { RootStackParamList } from './navigation/types';
import SignInScreen from './screens/SignInScreen';
import PeopleListScreen from './screens/PeopleListScreen';
import PersonDetailScreen from './screens/PersonDetailScreen';
import LogInteractionScreen from './screens/LogInteractionScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      setLoading(false);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_event, s) => {
      setSession(s);
    });
    return () => sub.subscription.unsubscribe();
  }, []);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center' }}>
        <ActivityIndicator />
      </View>
    );
  }

  if (!session) {
    return <SignInScreen />;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="People"
          component={PeopleListScreen}
          options={{ title: 'Your people' }}
        />
        <Stack.Screen
          name="PersonDetail"
          component={PersonDetailScreen}
          options={({ route }) => ({ title: route.params.name })}
        />
        <Stack.Screen
          name="LogInteraction"
          component={LogInteractionScreen}
          options={{ title: 'Log interaction' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
