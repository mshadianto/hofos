#!/usr/bin/env python3
"""
Honda Freed Superchatbot - Main API Entry Point
FastAPI application with routing to diagnostic and modification agents
"""
import re
import httpx
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

WAHA_URL = os.getenv("WAHA_URL")
WAHA_API_KEY = os.getenv("WAHA_API_KEY")

app = FastAPI(
    title="Honda Freed Superchatbot API",
    version="1.0.0",
    description="Agentic RAG system untuk komunitas Honda Freed Indonesia"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_SECRET = os.getenv("API_SECRET")


class MessageRequest(BaseModel):
    user_id: str
    message: str


class ImageRequest(BaseModel):
    user_id: str
    message: str = ""
    image_base64: str


class MessageResponse(BaseModel):
    response: str
    intent: str


def detect_intent(message: str) -> str:
    """
    Detect user intent from message to route to appropriate agent

    Returns:
        'diagnostic' - for car problems/issues
        'modification' - for mod/tuning requests
        'stage' - for specific stage info
        'bengkel' - for workshop search
        'help' - for help/info requests
        'greeting' - for greetings
    """
    message_lower = message.lower()

    # Greeting patterns
    greeting_patterns = ["halo", "helo", "hai", "hi", "hello", "selamat", "pagi", "siang", "sore", "malam"]
    if any(g in message_lower for g in greeting_patterns) and len(message_lower) < 30:
        return "greeting"

    # Stage-specific requests
    if re.search(r'stage\s*[123]', message_lower):
        return "stage"

    # Modification keywords
    mod_keywords = [
        "modif", "modifikasi", "upgrade", "ganti", "pasang",
        "turbo", "supercharger", "exhaust", "intake", "header",
        "coilover", "velg", "rem", "brake", "suspension",
        "stage", "tune", "ecu", "hondata", "bodykit", "aero"
    ]
    if any(kw in message_lower for kw in mod_keywords):
        return "modification"

    # Workshop keywords
    bengkel_keywords = ["bengkel", "workshop", "servis", "service", "lokasi", "alamat", "rekomendasi bengkel"]
    if any(kw in message_lower for kw in bengkel_keywords):
        return "bengkel"

    # Diagnostic keywords (problems/issues)
    diagnostic_keywords = [
        "masalah", "rusak", "bunyi", "getar", "bocor", "panas",
        "overheat", "mati", "susah", "boros", "lemah", "error",
        "warning", "check engine", "ac", "dingin", "rem", "stir",
        "cvt", "transmisi", "kopling", "oli", "bensin", "solar",
        "aki", "starter", "alternator", "radiator", "knalpot",
        "kenapa", "mengapa", "apa penyebab", "diagnosa", "cek"
    ]
    if any(kw in message_lower for kw in diagnostic_keywords):
        return "diagnostic"

    # Help keywords
    help_keywords = ["help", "bantuan", "cara", "bagaimana", "info", "apa itu", "menu"]
    if any(kw in message_lower for kw in help_keywords):
        return "help"

    # Default to diagnostic for unknown queries about the car
    return "diagnostic"


def get_greeting_response() -> str:
    """Return welcome message"""
    return """🚗 *SELAMAT DATANG DI HONDA FREED SUPERCHATBOT!*
_Developed by MS Hadianto #1347_

Saya asisten AI khusus untuk Honda Freed GB3/GB4 (2008-2016).

*Yang bisa saya bantu:*
🔧 *DIAGNOSA* - Ketik keluhan mobil Anda
   _Contoh: "AC tidak dingin" atau "CVT getar"_

🏎️ *MODIFIKASI* - Ketik permintaan mod
   _Contoh: "Stage 1" atau "modif mesin budget 10jt"_

📍 *BENGKEL* - Ketik "bengkel [kota]"
   _Contoh: "bengkel jakarta"_

---
Silakan ketik keluhan atau pertanyaan Anda!
"""


def get_help_response() -> str:
    """Return help message"""
    return """📋 *PANDUAN HONDA FREED SUPERCHATBOT*

*FITUR UTAMA:*

🔧 *DIAGNOSA MASALAH*
Ceritakan keluhan mobil Anda, saya akan analisa penyebab dan solusinya.
_Contoh:_
• "Mobil getar saat akselerasi"
• "AC tidak dingin"
• "Check engine light menyala"
• "Rem bunyi decit"

🏎️ *MODIFIKASI*
Tanyakan tentang upgrade dan modifikasi.
_Contoh:_
• "Stage 1" - paket modifikasi dasar
• "Stage 2" - paket menengah
• "Stage 3" - paket full racing
• "Modif mesin budget 15 juta"
• "Rekomendasi coilover"

📍 *CARI BENGKEL*
Ketik "bengkel [nama kota]" untuk rekomendasi bengkel.

---
💡 *Tips:* Semakin detail keluhan Anda, semakin akurat diagnosa saya!
"""


def get_workshop_response(message: str) -> str:
    """Return workshop search response"""
    # Extract city from message
    city_match = re.search(r'bengkel\s+(\w+)', message.lower())
    city = city_match.group(1) if city_match else "indonesia"

    return f"""📍 *CARI BENGKEL DI {city.upper()}*

Maaf, fitur pencarian bengkel masih dalam pengembangan.

*Sementara, berikut tips mencari bengkel:*

1. 🔍 Cari "bengkel Honda {city}" di Google Maps
2. ⭐ Pilih yang rating di atas 4.0
3. 💬 Baca review dari customer lain
4. 📞 Hubungi dulu untuk konfirmasi

*Bengkel Resmi Honda:*
Kunjungi honda-indonesia.com/dealer-locator

---
Ketik keluhan mobil Anda untuk diagnosa!
"""


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Honda Freed Superchatbot",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "/health": "Health check",
            "/process": "Process message (POST)"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected", "agents": "ready"}


@app.post("/process", response_model=MessageResponse)
async def process_message(request: MessageRequest, authorization: str = Header(None)):
    """
    Process incoming message and route to appropriate agent

    Args:
        request: MessageRequest with user_id and message
        authorization: Bearer token for authentication

    Returns:
        MessageResponse with response text and detected intent
    """
    # Validate authorization (optional for web frontend)
    if API_SECRET and authorization and authorization != f"Bearer {API_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Validate input
    if not request.message or not request.message.strip():
        return MessageResponse(
            response="Silakan ketik pesan Anda.",
            intent="empty"
        )

    # Detect intent
    intent = detect_intent(request.message)

    # Route to appropriate handler
    try:
        if intent == "greeting":
            response = get_greeting_response()

        elif intent == "help":
            response = get_help_response()

        elif intent == "bengkel":
            response = get_workshop_response(request.message)

        elif intent == "modification" or intent == "stage":
            from agents.freed_modification import process_modification_request
            response = process_modification_request(request.user_id, request.message)

        else:  # diagnostic (default)
            from agents.freed_diagnostic import process_freed_message
            response = process_freed_message(request.user_id, request.message)

    except Exception as e:
        response = f"""⚠️ *TERJADI KESALAHAN*

Maaf, sistem sedang mengalami gangguan.
Error: {str(e)[:100]}

Silakan coba lagi dalam beberapa saat.

Atau ketik *HELP* untuk melihat panduan penggunaan.
"""
        intent = "error"

    return MessageResponse(response=response, intent=intent)


@app.post("/process-image", response_model=MessageResponse)
async def process_image(request: ImageRequest, authorization: str = Header(None)):
    """
    Process image with vision model for car diagnostics

    Args:
        request: ImageRequest with user_id, message, and image_base64
        authorization: Bearer token for authentication

    Returns:
        MessageResponse with diagnosis based on image
    """
    # Validate authorization (allow empty for web frontend)
    if API_SECRET and authorization and authorization != f"Bearer {API_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not request.image_base64:
        return MessageResponse(
            response="Silakan kirim gambar untuk diagnosa.",
            intent="empty"
        )

    try:
        from agents.freed_vision import process_image_diagnosis
        response = process_image_diagnosis(
            request.user_id,
            request.message or "Tolong diagnosa masalah dari gambar ini",
            request.image_base64
        )
        return MessageResponse(response=response, intent="vision_diagnostic")
    except Exception as e:
        print(f"[VISION] Error: {e}")
        import traceback
        traceback.print_exc()
        return MessageResponse(
            response=f"⚠️ *TERJADI KESALAHAN*\n\nMaaf, gagal memproses gambar.\nError: {str(e)[:100]}\n\nCoba kirim ulang atau ketik keluhan Anda.",
            intent="error"
        )


@app.get("/stages")
async def get_stages():
    """Get all modification stage presets"""
    try:
        from database.supabase_client import supabase
        result = supabase.table("stage_presets").select("*").order("stage").execute()
        return {"stages": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/parts")
async def get_parts(category: str = None, stage: int = None):
    """Get modification parts catalog"""
    try:
        from database.supabase_client import supabase
        query = supabase.table("modification_catalog").select("*")

        if category:
            query = query.eq("category", category)
        if stage:
            query = query.lte("min_stage", stage)

        result = query.order("category").execute()
        return {"parts": result.data, "count": len(result.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def send_waha_message(chat_id: str, text: str, session: str = "default"):
    """Send message back via WAHA API"""
    print(f"[WAHA] Sending message to {chat_id} via session {session}")
    print(f"[WAHA] WAHA_URL: {WAHA_URL}, API_KEY set: {bool(WAHA_API_KEY)}")

    async with httpx.AsyncClient() as client:
        # Try the newer WAHA API endpoint first
        send_url = f"{WAHA_URL}/api/sendText"
        headers = {"X-Api-Key": WAHA_API_KEY}
        payload = {
            "session": session,
            "chatId": chat_id,
            "text": text
        }

        print(f"[WAHA] POST {send_url}")
        print(f"[WAHA] Payload: {payload}")

        try:
            response = await client.post(
                send_url,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            print(f"[WAHA] Response status: {response.status_code}")
            print(f"[WAHA] Response body: {response.text}")
            return response.json()
        except Exception as e:
            print(f"[WAHA] Error: {e}")
            return {"error": str(e)}


def process_message_sync(user_id: str, message: str) -> str:
    """Process message and return response (sync version for webhook)"""
    if not message or not message.strip():
        return "Silakan ketik pesan Anda."

    intent = detect_intent(message)

    try:
        if intent == "greeting":
            return get_greeting_response()
        elif intent == "help":
            return get_help_response()
        elif intent == "bengkel":
            return get_workshop_response(message)
        elif intent == "modification" or intent == "stage":
            from agents.freed_modification import process_modification_request
            return process_modification_request(user_id, message)
        else:
            from agents.freed_diagnostic import process_freed_message
            return process_freed_message(user_id, message)
    except Exception as e:
        return f"⚠️ *TERJADI KESALAHAN*\n\nError: {str(e)[:100]}\n\nKetik *HELP* untuk panduan."


@app.post("/webhook")
async def waha_webhook(request: Request):
    """
    Webhook endpoint for WAHA WhatsApp messages
    Receives message, processes it, sends reply back via WAHA
    """
    try:
        payload = await request.json()
        print(f"[WEBHOOK] ====== NEW REQUEST ======")
        print(f"[WEBHOOK] Full payload: {payload}")

        # Check if it's a message event (support multiple formats)
        event = payload.get("event", "")
        print(f"[WEBHOOK] Event type: {event}")

        # Accept various message event types from WAHA
        valid_events = ["message", "message.any", "message.received"]
        if not any(event.startswith(e) for e in valid_events):
            print(f"[WEBHOOK] Ignoring event: {event}")
            return {"status": "ignored", "reason": f"event type: {event}"}

        # Extract message data - handle different WAHA payload structures
        message_data = payload.get("payload", {})

        # Try different field names for chat ID
        # Prefer remoteJidAlt (standard format) over @lid format
        _data = message_data.get("_data", {})
        key_data = _data.get("key", {})
        chat_id = key_data.get("remoteJidAlt") or key_data.get("remoteJid") or message_data.get("from") or message_data.get("chatId")

        # Try different field names for message body
        message_body = message_data.get("body") or message_data.get("text") or ""
        if not message_body and "message" in message_data:
            msg = message_data.get("message", {})
            message_body = msg.get("conversation") or msg.get("extendedTextMessage", {}).get("text", "")

        is_from_me = message_data.get("fromMe", False) or key_data.get("fromMe", False)
        session = payload.get("session", "default")

        print(f"[WEBHOOK] Extracted - chat_id: {chat_id}, body: {message_body}, fromMe: {is_from_me}, session: {session}")

        # Skip messages from self
        if is_from_me:
            print(f"[WEBHOOK] Skipping self message")
            return {"status": "ignored", "reason": "message from self"}

        # Skip empty messages
        if not message_body:
            print(f"[WEBHOOK] Skipping empty message")
            return {"status": "ignored", "reason": "empty message"}

        if not chat_id:
            print(f"[WEBHOOK] No chat_id found")
            return {"status": "error", "reason": "no chat_id"}

        # Process the message
        print(f"[WEBHOOK] Processing message...")
        response_text = process_message_sync(chat_id, message_body)
        print(f"[WEBHOOK] Response generated ({len(response_text)} chars): {response_text[:100]}...")

        # Send reply via WAHA
        print(f"[WEBHOOK] Sending reply to WAHA...")
        result = await send_waha_message(chat_id, response_text, session)
        print(f"[WEBHOOK] WAHA send result: {result}")
        print(f"[WEBHOOK] ====== REQUEST COMPLETE ======")

        return {"status": "ok", "chat_id": chat_id, "processed": True}

    except Exception as e:
        print(f"[WEBHOOK] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
