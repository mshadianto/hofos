# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Honda Freed Superchatbot - an agentic RAG (Retrieval-Augmented Generation) system for the Honda Freed Indonesia community. Provides diagnostic reasoning, modification planning, workshop recommendations, and cost estimation via WhatsApp integration.

## Tech Stack

- **Backend**: Python/FastAPI with LangGraph + LangChain for agentic workflows
- **Database**: Supabase (PostgreSQL with pgvector)
- **LLM**: Groq API (llama-3.1-70b-versatile)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2, 384 dimensions)
- **WhatsApp Integration**: WAHA (WhatsApp HTTP API)
- **Webhook Proxy**: Cloudflare Worker (routes WhatsApp messages to Python backend)

## Common Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Run development server
uvicorn main:app --reload --port 8000

# Run tests
pytest

# Run single test
pytest tests/test_api.py::test_health -v

# Seed database (requires Supabase connection)
python scripts/seed_data.py

# Deploy Cloudflare Worker
cd cloudflare-worker
wrangler deploy
```

## Architecture

```
main.py                         FastAPI app with intent detection and routing
├── agents/
│   ├── freed_diagnostic.py     LangGraph workflow: symptom extraction → vector search → LLM diagnosis
│   └── freed_modification.py   LangGraph workflow: parse request → retrieve parts → generate plan
├── database/
│   ├── schema.sql              Supabase schema with pgvector, RPC functions
│   └── supabase_client.py      Supabase connection singleton
├── scripts/
│   └── seed_data.py            Seeds: 16 service manual entries, 10 common issues, 54 mod parts
├── cloudflare-worker/
│   └── src/index.js            Webhook: WAHA → Python backend → WAHA
└── tests/
    └── test_api.py             FastAPI TestClient tests
```

## Agent Workflows

### Diagnostic Agent (freed_diagnostic.py)
```
extract_symptoms → retrieve_service_docs → retrieve_common_issues → generate_diagnosis → format_response
```
- Uses vector similarity search on `freed_service_manuals` and `freed_common_issues` tables
- LLM generates diagnosis with confidence levels, part recommendations, cost estimates

### Modification Agent (freed_modification.py)
```
parse_request → retrieve_stage_preset → retrieve_parts → generate_modification_plan → calculate_total_cost → format_response
```
- Supports Stage 1/2/3 presets with predefined part lists
- Filters parts by category, stage, and budget
- Calculates total cost including installation estimates

## Database Schema (key tables)

- `freed_service_manuals`: Service manual content with embeddings (vector search)
- `freed_common_issues`: Common problems with symptoms, causes, costs (vector search)
- `modification_catalog`: 54 parts across engine, suspension, brakes, wheels, interior, exterior
- `stage_presets`: Stage 1/2/3 modification packages with target HP and budget ranges

## Request Flow

1. WhatsApp message → WAHA webhook → Cloudflare Worker
2. Worker calls `/process` endpoint with Bearer auth
3. `detect_intent()` routes to: greeting, help, bengkel, modification, or diagnostic
4. Agent executes LangGraph workflow with RAG retrieval
5. Response sent back through Worker → WAHA → WhatsApp

## Environment Variables

Required in `.env`:
- `SUPABASE_URL`, `SUPABASE_KEY` - Database + vector search
- `GROQ_API_KEY` - LLM provider
- `WAHA_URL`, `WAHA_API_KEY` - WhatsApp API
- `API_SECRET` - Bearer token for /process endpoint auth

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /process` - Main message processing (requires Bearer auth)
- `GET /stages` - Get modification stage presets
- `GET /parts?category=engine&stage=1` - Query parts catalog
