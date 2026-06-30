import { useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../navigation/types';
import { supabase } from '../lib/supabase';
import { extractFacts } from '../lib/extract';

type Props = NativeStackScreenProps<RootStackParamList, 'LogInteraction'>;

export default function LogInteractionScreen({ route, navigation }: Props) {
  const { personId } = route.params;
  const [body, setBody] = useState('');
  const [saving, setSaving] = useState(false);

  // The capture -> structure -> store loop, in its thinnest form:
  // 1) take a free-text sentence
  // 2) if a Gemini key is set, ask the model to pull out facts (else use raw text)
  // 3) write the interaction, plus any extracted attributes
  async function save() {
    const text = body.trim();
    if (!text) return;
    setSaving(true);

    const extracted = await extractFacts(text); // null when no API key — that's fine

    const { error } = await supabase.from('interactions').insert({
      person_id: personId,
      channel: extracted?.channel ?? null,
      summary: extracted?.summary ?? text,
    });

    if (!error && extracted?.attributes?.length) {
      await supabase.from('attributes').insert(
        extracted.attributes.map((a) => ({
          person_id: personId,
          key: a.key,
          value: a.value,
        }))
      );
    }

    setSaving(false);
    if (error) Alert.alert('Save error', error.message);
    else navigation.goBack();
  }

  return (
    <View style={styles.container}>
      <Text style={styles.label}>
        Describe what happened in a sentence or two. If you set a Gemini key,
        the app pulls out the facts automatically.
      </Text>
      <TextInput
        style={styles.input}
        placeholder="e.g. Coffee with her — she started a pottery class and is stressed about her thesis defense in March."
        multiline
        value={body}
        onChangeText={setBody}
        autoFocus
      />
      <Pressable style={styles.btn} onPress={save} disabled={saving}>
        {saving ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>Save</Text>}
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, gap: 12 },
  label: { fontSize: 14, color: '#555' },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    minHeight: 120,
    textAlignVertical: 'top',
  },
  btn: { backgroundColor: '#2b2b2b', borderRadius: 8, padding: 14, alignItems: 'center' },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '500' },
});
