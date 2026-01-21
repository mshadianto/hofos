# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Honda Freed Superchatbot - an agentic RAG system for the Honda Freed Indonesia community (GB3/GB4, 2008-2016). Provides diagnostic reasoning, modification planning, and cost estimation via WhatsApp.

## Tech Stack

- **Backend**: Python/FastAPI + LangGraph for agentic workflows
- **Database**: Supabase (PostgreSQL with pgvector, 384-dim embeddings)
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **WhatsApp**: WAHA (WhatsApp HTTP API)

## Commands

```bash
# Setup (Windows)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Run server
uvicorn main:app --reload --port 8000

# Tests
pytest
pytest tests/test_api.py::test_health -v

# Seed database
python scripts/seed_data.py

# Deploy Cloudflare Worker
cd cloudflare-worker && wrangler deploy
```

## Architecture

```
main.py                 → FastAPI app, intent detection, routing
agents/
  freed_diagnostic.py   → Diagnostic LangGraph workflow (entry: process_freed_message)
  freed_modification.py → Modification LangGraph workflow (entry: process_modification_request)
database/
  schema.sql            → Supabase schema + RPC functions for vector search
  supabase_client.py    → Supabase singleton
cloudflare-worker/      → Legacy webhook proxy (Cloudflare Worker)
```

## Intent Routing (main.py:46)

`detect_intent()` matches keywords to route messages:
- `greeting` → static welcome message
- `help` → static help text
- `bengkel` → workshop search (placeholder)
- `modification`/`stage` → freed_modification agent
- `diagnostic` (default) → freed_diagnostic agent

## Agent Workflows

**Diagnostic** (`agents/freed_diagnostic.py`):
```
extract_symptoms → retrieve_service_docs → retrieve_common_issues → generate_diagnosis → format_response
```
- Vector search via `match_service_manuals()` and `match_common_issues()` RPC functions
- Entry point: `process_freed_message(user_id, message)`

**Modification** (`agents/freed_modification.py`):
```
parse_request → retrieve_stage_preset → retrieve_parts → generate_modification_plan → calculate_total_cost → format_response
```
- Queries `stage_presets` and `modification_catalog` tables
- Entry point: `process_modification_request(user_id, message)`

## Vector Search RPC Functions (database/schema.sql)

```sql
match_service_manuals(query_embedding vector(384), match_threshold float, match_count int)
match_common_issues(query_embedding vector(384), match_threshold float, match_count int)
```
Both use cosine similarity with default threshold 0.5.

## Webhook Integration

**Direct webhook (preferred)**: POST `/webhook`
- Receives WAHA payload, extracts `chatId` from `payload._data.key.remoteJidAlt`
- Calls `process_message_sync()`, sends reply via `send_waha_message()`

**Via Cloudflare Worker (legacy)**: POST `/process`
- Requires `Authorization: Bearer {API_SECRET}` header
- Worker handles WAHA send

## Environment Variables

```
SUPABASE_URL, SUPABASE_KEY  # Database + vector search
GROQ_API_KEY                # LLM provider
WAHA_URL, WAHA_API_KEY      # WhatsApp API
API_SECRET                  # Bearer auth for /process
```
