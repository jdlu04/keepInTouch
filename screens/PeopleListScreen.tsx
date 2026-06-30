import { useCallback, useState } from 'react';
import {
  Alert,
  FlatList,
  Pressable,
  RefreshControl,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../navigation/types';
import { supabase } from '../lib/supabase';

type Props = NativeStackScreenProps<RootStackParamList, 'People'>;
type Person = { id: string; full_name: string; relationship: string | null };

export default function PeopleListScreen({ navigation }: Props) {
  const [people, setPeople] = useState<Person[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [newName, setNewName] = useState('');

  // RLS makes this return only the signed-in user's rows — no filtering needed.
  const load = useCallback(async () => {
    const { data, error } = await supabase
      .from('people')
      .select('id, full_name, relationship')
      .order('full_name');
    if (error) Alert.alert('Load error', error.message);
    else setPeople(data ?? []);
  }, []);

  // Reload whenever the screen regains focus (e.g. after adding a person).
  useFocusEffect(useCallback(() => { load(); }, [load]));

  async function addPerson() {
    const name = newName.trim();
    if (!name) return;
    // user_id is filled automatically by the column default (auth.uid()).
    const { error } = await supabase.from('people').insert({ full_name: name });
    if (error) Alert.alert('Add error', error.message);
    else {
      setNewName('');
      load();
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.addRow}>
        <TextInput
          style={styles.input}
          placeholder="Add a person…"
          value={newName}
          onChangeText={setNewName}
          onSubmitEditing={addPerson}
          returnKeyType="done"
        />
        <Pressable style={styles.btn} onPress={addPerson}>
          <Text style={styles.btnText}>Add</Text>
        </Pressable>
      </View>

      <FlatList
        data={people}
        keyExtractor={(p) => p.id}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={async () => {
              setRefreshing(true);
              await load();
              setRefreshing(false);
            }}
          />
        }
        renderItem={({ item }) => (
          <Pressable
            style={styles.row}
            onPress={() =>
              navigation.navigate('PersonDetail', { personId: item.id, name: item.full_name })
            }
          >
            <Text style={styles.name}>{item.full_name}</Text>
            {item.relationship ? <Text style={styles.sub}>{item.relationship}</Text> : null}
          </Pressable>
        )}
        ListEmptyComponent={<Text style={styles.empty}>No people yet. Add someone above.</Text>}
      />

      <Pressable style={styles.signout} onPress={() => supabase.auth.signOut()}>
        <Text style={styles.signoutText}>Sign out</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  addRow: { flexDirection: 'row', gap: 8, marginBottom: 12 },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  btn: { backgroundColor: '#2b2b2b', borderRadius: 8, paddingHorizontal: 18, justifyContent: 'center' },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '500' },
  row: { paddingVertical: 14, borderBottomWidth: 1, borderBottomColor: '#eee' },
  name: { fontSize: 17, fontWeight: '500' },
  sub: { fontSize: 13, color: '#777', marginTop: 2 },
  empty: { textAlign: 'center', color: '#999', marginTop: 40 },
  signout: { paddingVertical: 14, alignItems: 'center' },
  signoutText: { color: '#b00', fontSize: 15 },
});
