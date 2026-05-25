# Deployment Guide: Vercel Frontend + Render Backend

## 1. Repository layout

This repository is a monorepo.

- `frontend/`: Next.js app for Vercel
- `backend/`: FastAPI app for Render

## 2. Deploy backend to Render

Create a Render Web Service from this GitHub repository.

Recommended settings:

- Runtime: Python 3
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

After deployment, check:

```text
https://YOUR-BACKEND.onrender.com/health
```

It should return:

```json
{ "status": "healthy" }
```

## 3. Deploy frontend to Vercel

Import the same GitHub repository into Vercel.

Recommended settings:

- Framework Preset: Next.js
- Root Directory: `frontend`
- Install Command: `npm ci`
- Build Command: `npm run build`
- Output Directory: leave default

Set this Vercel environment variable for Production and Preview:

```text
NEXT_PUBLIC_API_BASE_URL=https://YOUR-BACKEND.onrender.com
```

## 4. Allow Vercel domain in Render CORS

After Vercel deployment, copy the Vercel app URL and add this Render environment variable:

```text
FRONTEND_ORIGINS=https://YOUR-APP.vercel.app
```

For local development plus production, use comma separation:

```text
FRONTEND_ORIGINS=https://YOUR-APP.vercel.app,http://localhost:3000,http://127.0.0.1:3000
```

Redeploy the Render backend after changing this variable.

## 5. Local development

Backend:

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 9001 --reload
```

Frontend:

```bash
cd frontend
npm ci
cp .env.example .env.local
npm run dev
```

Open:

```text
http://127.0.0.1:3000
```
