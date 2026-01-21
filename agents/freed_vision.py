#!/usr/bin/env python3
"""
Honda Freed Vision Agent - Image-based Diagnostics
Uses Groq's vision model to analyze car images for diagnostics
"""
import os
import base64
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VISION_SYSTEM_PROMPT = """Kamu adalah mekanik ahli Honda Freed GB3/GB4 (2008-2016) dengan kemampuan visual diagnosis.

TUGAS: Analisa gambar yang dikirim user untuk mendiagnosa masalah mobil.

SPESIFIKASI HONDA FREED:
- Mesin: L15A i-VTEC 1.5L (117 HP)
- Transmisi: CVT / 5-speed Manual
- Tahun: 2008-2016

YANG BISA KAMU IDENTIFIKASI DARI GAMBAR:
1. Kondisi mesin (oli bocor, kabel rusak, komponen aus)
2. Dashboard warning lights dan error codes
3. Kondisi ban, velg, rem
4. Kerusakan body, cat, karat
5. Kondisi interior (jok, dashboard, panel)
6. Komponen undercarriage
7. Kondisi lampu, kaca, wiper
8. Kebocoran cairan (oli, coolant, brake fluid)

FORMAT JAWABAN:
1. Deskripsi apa yang terlihat di gambar
2. Identifikasi masalah/kondisi (jika ada)
3. Kemungkinan penyebab
4. Rekomendasi tindakan
5. Estimasi biaya perbaikan (dalam Rupiah)
6. Tingkat urgensi (segera/bisa ditunda/preventif)

Jika gambar tidak jelas atau bukan bagian mobil, minta user untuk mengirim ulang gambar yang lebih jelas.

Selalu jawab dalam Bahasa Indonesia dengan format yang jelas dan mudah dipahami."""


def process_image_diagnosis(user_id: str, message: str, image_base64: str) -> str:
    """
    Process image for car diagnostics using vision model

    Args:
        user_id: User identifier
        message: Optional text message/context from user
        image_base64: Base64 encoded image data

    Returns:
        Formatted diagnostic response
    """
    try:
        # Prepare the image for the API
        # Groq expects base64 image in data URL format
        image_url = f"data:image/jpeg;base64,{image_base64}"

        # Create the message with image
        messages = [
            {
                "role": "system",
                "content": VISION_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    },
                    {
                        "type": "text",
                        "text": f"Tolong analisa gambar ini. Konteks dari user: {message}"
                    }
                ]
            }
        ]

        # Call Groq vision model
        response = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",  # Groq's vision model
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )

        diagnosis = response.choices[0].message.content

        # Format the response
        formatted_response = f"""📷 *DIAGNOSA VISUAL HONDA FREED*

{diagnosis}

---
💡 _Diagnosa ini berdasarkan analisa gambar dengan AI._
_Untuk kepastian, kunjungi bengkel untuk pemeriksaan langsung._

Ketik keluhan tambahan atau kirim foto lain untuk analisa lebih lanjut!
"""
        return formatted_response

    except Exception as e:
        error_msg = str(e)
        print(f"[VISION] Error processing image: {error_msg}")

        # Check for specific error types
        if "rate_limit" in error_msg.lower():
            return """⚠️ *SISTEM SIBUK*

Maaf, terlalu banyak permintaan saat ini.
Silakan coba lagi dalam beberapa detik.

Atau ketik keluhan Anda secara teks untuk diagnosa alternatif."""

        if "invalid" in error_msg.lower() or "image" in error_msg.lower():
            return """⚠️ *GAMBAR TIDAK VALID*

Maaf, gambar tidak dapat diproses. Pastikan:
• Format: JPG, PNG, atau WEBP
• Ukuran: Maksimal 5MB
• Gambar jelas dan tidak blur

Silakan kirim ulang gambar yang lebih jelas."""

        return f"""⚠️ *TERJADI KESALAHAN*

Maaf, gagal memproses gambar.
Silakan coba lagi atau ketik keluhan Anda secara teks.

Ketik *HELP* untuk panduan penggunaan."""
