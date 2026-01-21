# Honda Freed Superchatbot - Web Frontend

Landing page dengan chat widget untuk Honda Freed Superchatbot.

## Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env dengan API URL dan secret
```

## Development

```bash
npm run dev
```

Buka http://localhost:3000

## Build

```bash
npm run build
```

Output di folder `dist/`

## Environment Variables

- `VITE_API_URL` - URL backend API (default: http://localhost:8000)
- `VITE_API_SECRET` - API secret untuk auth

## Deploy

Build output (`dist/`) bisa di-deploy ke:
- Vercel
- Netlify
- Cloudflare Pages
- Static hosting lainnya

Pastikan set environment variables di platform deploy.
