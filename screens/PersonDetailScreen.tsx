import { useCallback, useState } from 'react';
import { Alert, FlatList, Pressable, StyleSheet, Text, View } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../navigation/types';
import { supabase } from '../lib/supabase';

type Props = NativeStackScreenProps<RootStackParamList, 'PersonDetail'>;
type Attribute = { id: string; key: string; value: string | null };
type Interaction = { id: string; channel: string | null; summary: string | null; occurred_at: string };

export default function PersonDetailScreen({ route, navigation }: Props) {
  const { personId, name } = route.params;
  const [attributes, setAttributes] = useState<Attribute[]>([]);
  const [interactions, setInteractions] = useState<Interaction[]>([]);

  const load = useCallback(async () => {
    const [attrs, ints] = await Promise.all([
      supabase.from('attributes').select('id, key, value').eq('person_id', personId),
      supabase
        .from('interactions')
        .select('id, channel, summary, occurred_at')
        .eq('person_id', personId)
        .order('occurred_at', { ascending: false }),
    ]);
    if (attrs.error) Alert.alert('Load error', attrs.error.message);
    else setAttributes(attrs.data ?? []);
    if (ints.error) Alert.alert('Load error', ints.error.message);
    else setInteractions(ints.data ?? []);
  }, [personId]);

  useFocusEffect(useCallback(() => { load(); }, [load]));

  return (
    <View style={styles.container}>
      <Pressable
        style={styles.btn}
        onPress={() => navigation.navigate('LogInteraction', { personId, name })}
      >
        <Text style={styles.btnText}>Log an interaction</Text>
      </Pressable>

      <Text style={styles.section}>What you know</Text>
      {attributes.length === 0 ? (
        <Text style={styles.empty}>No facts yet.</Text>
      ) : (
        attributes.map((a) => (
          <Text key={a.id} style={styles.fact}>
            <Text style={styles.factKey}>{a.key}: </Text>
            {a.value}
          </Text>
        ))
      )}

      <Text style={styles.section}>History</Text>
      <FlatList
        data={interactions}
        keyExtractor={(i) => i.id}
        renderItem={({ item }) => (
          <View style={styles.row}>
            <Text style={styles.summary}>{item.summary ?? '(no summary)'}</Text>
            <Text style={styles.meta}>
              {item.channel ? item.channel + ' · ' : ''}
              {new Date(item.occurred_at).toLocaleDateString()}
            </Text>
          </View>
        )}
        ListEmptyComponent={<Text style={styles.empty}>No interactions logged yet.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  btn: { backgroundColor: '#2b2b2b', borderRadius: 8, padding: 14, alignItems: 'center' },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '500' },
  section: { fontSize: 13, fontWeight: '600', color: '#888', marginTop: 20, marginBottom: 6, textTransform: 'uppercase' },
  fact: { fontSize: 15, marginBottom: 4 },
  factKey: { fontWeight: '500' },
  row: { paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: '#eee' },
  summary: { fontSize: 15 },
  meta: { fontSize: 12, color: '#999', marginTop: 2 },
  empty: { color: '#999' },
});
