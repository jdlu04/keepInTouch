# Frontend — Expo (React Native)

The Keep in Touch mobile app, built with Expo (SDK 57) and TypeScript.

> This is currently a **blank starter** — the frontend team builds the screens
> from here. It's just `App.tsx` (a placeholder screen) and the Expo config.

```
frontend/
├── App.tsx           Root component (placeholder)
├── index.ts          Expo entry point
├── app.json          Expo config
├── assets/           Icons and splash
├── .env.example      Template for the env vars (copy to .env)
├── tsconfig.json
└── src/              Team's app code lives here
    ├── components/   Reusable UI pieces (buttons, cards, …)
    ├── screens/      Full screens / pages
    ├── navigation/   React Navigation setup (stacks, tabs)
    ├── lib/          Supabase client + shared helpers
    ├── hooks/        Custom React hooks
    └── types/        Shared TypeScript types
```

The `src/` folders are empty scaffolding (each has a `.gitkeep`) — delete or
rename them however the team prefers. Import from them like
`import Foo from './src/components/Foo'`.

## Run it

```bash
npm install
npm run start      # Expo dev server — scan the QR code with Expo Go
```

Other commands: `npm run ios`, `npm run android`, `npm run web`.

Full setup (including connecting to Supabase when you're ready) is in
[../docs/setup.md](../docs/setup.md).

## Notes

- Type-check locally with `npx tsc --noEmit` (this is what CI runs).
- Secrets go in `frontend/.env` (gitignored) — never commit it.
