// ============================================================================
// OPTIONAL — Day 4. Turn one sentence into structured facts using a FREE LLM.
//
// Get a free key at https://ai.google.dev (Google AI Studio) and put it in
// .env as EXPO_PUBLIC_GEMINI_API_KEY. If no key is set, extractFacts() returns
// null and the app simply stores the raw note text — nothing breaks.
//
// SECURITY NOTE: calling the model directly from the app exposes your API key
// in the client bundle. That is fine for a prototype running on your own
// device. Before you ship, move this call into a Supabase Edge Function so the
// key stays server-side. (White paper, Step 7.)
// ============================================================================

const GEMINI_KEY = process.env.EXPO_PUBLIC_GEMINI_API_KEY;

// Model names change — confirm the current free model at https://ai.google.dev
const MODEL = 'gemini-1.5-flash';

export type Extracted = {
  full_name?: string;
  channel?: string;
  summary?: string;
  attributes?: { key: string; value: string }[];
};

export async function extractFacts(sentence: string): Promise<Extracted | null> {
  if (!GEMINI_KEY) return null;

  const prompt =
    'Extract relationship facts from the note below. ' +
    'Return ONLY JSON matching this shape: ' +
    '{"full_name": string, "channel": string, "summary": string, ' +
    '"attributes": [{"key": string, "value": string}]}. ' +
    'Use "in-person", "call", "text", or "email" for channel when clear.\n' +
    'Note: """' + sentence + '"""';

  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${GEMINI_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { responseMimeType: 'application/json' },
        }),
      }
    );
    if (!res.ok) return null;
    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
    return text ? (JSON.parse(text) as Extracted) : null;
  } catch {
    return null; // never let the AI step block a save
  }
}
