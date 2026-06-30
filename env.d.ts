// Ambient types for Expo public env vars so `tsc --noEmit` (used by CI) passes
// even before `expo start` generates expo-env.d.ts. Merges harmlessly with it.
declare namespace NodeJS {
  interface ProcessEnv {
    [key: `EXPO_PUBLIC_${string}`]: string | undefined;
  }
}
