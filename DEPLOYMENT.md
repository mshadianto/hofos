# 🚀 Deployment Guide

## Railway (Recommended)
1. Push to GitHub
2. Connect Railway to repo
3. Set environment variables
4. Auto-deploy

## Manual VPS
```bash
git clone YOUR_REPO
cd honda-freed-superchatbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Cloudflare Worker
```bash
cd cloudflare-worker
wrangler login
wrangler secret put PYTHON_BACKEND_URL
wrangler deploy
```
