# EAG Security Dashboard

Phase 20 frontend for Extension AI Guard.

## Stack

- React 19
- TypeScript 6
- Vite 8
- Tailwind CSS 4.3.3
- Oxlint

## Development

Create `.env.local` when the backend is not running at the default address:

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Then:

```
npm install
npm run dev
```

Production verification:

```
npm run lint
npm run build
```

The frontend does not implement security-detection rules. The FastAPI backend remains authoritative.
