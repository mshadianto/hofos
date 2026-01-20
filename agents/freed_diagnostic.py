#!/usr/bin/env python3
"""
Honda Freed Diagnostic Agent - LangGraph Implementation
Handles diagnostic reasoning for Honda Freed GB3/GB4 (2008-2016)
"""
import os
from typing import TypedDict, Annotated, List, Optional
from operator import add
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from sentence_transformers import SentenceTransformer

load_dotenv()

# Initialize models
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

embedder = SentenceTransformer('all-MiniLM-L6-v2')


class DiagnosticState(TypedDict):
    """State for diagnostic workflow"""
    user_id: str
    message: str
    symptoms: List[str]
    vehicle_info: dict
    retrieved_docs: List[dict]
    common_issues: List[dict]
    diagnosis: str
    recommendations: List[str]
    cost_estimate: dict
    response: str


FREED_SYSTEM_PROMPT = """Kamu adalah mekanik ahli Honda Freed GB3/GB4 (2008-2016) dengan pengalaman 15+ tahun.

SPESIFIKASI HONDA FREED:
- Mesin: L15A i-VTEC 1.5L (117 HP @ 6,600 RPM, 146 Nm @ 4,800 RPM)
- Transmisi: CVT / 5-speed Manual
- Kapasitas oli: 3.5L (dengan filter)
- Oli recommended: 0W-20 atau 5W-30
- Interval servis: 10,000 km atau 6 bulan
- Timing chain (bukan belt) - tidak perlu ganti berkala

COMMON ISSUES HONDA FREED:
1. CVT judder/getar saat akselerasi - ganti CVT fluid, cek torque converter
2. AC tidak dingin - cek freon, kompresor, kondensor
3. Idle kasar - bersihkan throttle body, cek IACV
4. Bunyi gluduk depan - cek ball joint, tie rod end, stabilizer link
5. Rem bunyi - cek pad thickness, rotor condition
6. Check engine light - scan OBD2 untuk error code

PANDUAN DIAGNOSA:
1. Tanyakan detail gejala (kapan, seberapa sering, kondisi apa)
2. Hubungkan dengan common issues yang relevan
3. Berikan diagnosa dengan confidence level
4. Rekomendasikan part yang perlu diganti dengan estimasi harga
5. Sarankan bengkel jika diperlukan

Selalu jawab dalam Bahasa Indonesia dengan format yang jelas."""


def extract_symptoms(state: DiagnosticState) -> DiagnosticState:
    """Extract symptoms from user message"""
    message = state["message"].lower()

    symptom_keywords = {
        "getar": ["cvt judder", "mounting rusak", "balance shaft"],
        "bunyi": ["ball joint", "tie rod", "bearing", "brake pad"],
        "bocor": ["seal oli", "radiator", "water pump"],
        "panas": ["thermostat", "radiator", "water pump", "kipas"],
        "boros": ["filter udara kotor", "busi aus", "injector kotor"],
        "susah_start": ["aki lemah", "starter", "fuel pump"],
        "ac": ["freon habis", "kompresor", "kondensor", "evaporator"],
        "rem": ["brake pad", "rotor", "master cylinder", "brake fluid"],
        "oli": ["seal bocor", "gasket", "piston ring"],
        "cvt": ["cvt fluid", "torque converter", "solenoid"],
        "lampu": ["bohlam", "relay", "fuse", "alternator"],
        "stir": ["power steering", "rack end", "tie rod"],
    }

    detected_symptoms = []
    for keyword, related in symptom_keywords.items():
        if keyword in message:
            detected_symptoms.extend(related)

    if not detected_symptoms:
        detected_symptoms = ["general_checkup"]

    state["symptoms"] = list(set(detected_symptoms))
    return state


def retrieve_service_docs(state: DiagnosticState) -> DiagnosticState:
    """Retrieve relevant service manual sections via vector search"""
    from database.supabase_client import supabase

    query_embedding = embedder.encode(state["message"]).tolist()

    try:
        # Vector similarity search on service manuals
        result = supabase.rpc(
            'match_service_manuals',
            {
                'query_embedding': query_embedding,
                'match_threshold': 0.5,
                'match_count': 5
            }
        ).execute()

        state["retrieved_docs"] = result.data if result.data else []
    except Exception as e:
        print(f"Vector search error: {e}")
        state["retrieved_docs"] = []

    return state


def retrieve_common_issues(state: DiagnosticState) -> DiagnosticState:
    """Retrieve matching common issues from database"""
    from database.supabase_client import supabase

    query_embedding = embedder.encode(state["message"]).tolist()

    try:
        result = supabase.rpc(
            'match_common_issues',
            {
                'query_embedding': query_embedding,
                'match_threshold': 0.5,
                'match_count': 3
            }
        ).execute()

        state["common_issues"] = result.data if result.data else []
    except Exception as e:
        print(f"Common issues search error: {e}")
        state["common_issues"] = []

    return state


def generate_diagnosis(state: DiagnosticState) -> DiagnosticState:
    """Generate diagnosis using LLM with retrieved context"""

    context_parts = []

    if state["retrieved_docs"]:
        context_parts.append("📚 DARI SERVICE MANUAL:")
        for doc in state["retrieved_docs"][:3]:
            context_parts.append(f"- {doc.get('section', 'N/A')}: {doc.get('content', '')[:500]}")

    if state["common_issues"]:
        context_parts.append("\n⚠️ COMMON ISSUES TERKAIT:")
        for issue in state["common_issues"]:
            causes = ", ".join(issue.get('probable_cause', []))
            cost = issue.get('cost_estimate_idr', {})
            context_parts.append(
                f"- Gejala: {issue.get('symptom', 'N/A')}\n"
                f"  Penyebab: {causes}\n"
                f"  Estimasi: Rp {cost.get('min', 0):,} - Rp {cost.get('max', 0):,}"
            )

    context = "\n".join(context_parts) if context_parts else "Tidak ada data spesifik ditemukan."

    messages = [
        SystemMessage(content=FREED_SYSTEM_PROMPT),
        HumanMessage(content=f"""
KONTEKS DATABASE:
{context}

KELUHAN USER:
{state["message"]}

GEJALA TERDETEKSI: {', '.join(state["symptoms"])}

Berikan diagnosa lengkap dengan:
1. Kemungkinan penyebab (dengan persentase keyakinan)
2. Part yang perlu dicek/diganti
3. Estimasi biaya dalam Rupiah
4. Urgensi (segera/bisa ditunda/preventif)
5. Tips perawatan terkait
""")
    ]

    response = llm.invoke(messages)
    state["diagnosis"] = response.content

    return state


def format_response(state: DiagnosticState) -> DiagnosticState:
    """Format final response for WhatsApp"""

    response = f"""🔧 *DIAGNOSA HONDA FREED*

{state["diagnosis"]}

---
💡 _Diagnosa ini berdasarkan database 500+ kasus Honda Freed._
_Untuk kepastian, kunjungi bengkel resmi atau spesialis Honda._

Ketik:
• *BENGKEL [kota]* - cari bengkel terdekat
• *MODIF* - lihat katalog modifikasi
• *STAGE [1/2/3]* - paket modifikasi lengkap
"""

    state["response"] = response
    return state


def build_diagnostic_graph() -> StateGraph:
    """Build the diagnostic workflow graph"""
    workflow = StateGraph(DiagnosticState)

    # Add nodes
    workflow.add_node("extract_symptoms", extract_symptoms)
    workflow.add_node("retrieve_docs", retrieve_service_docs)
    workflow.add_node("retrieve_issues", retrieve_common_issues)
    workflow.add_node("generate_diagnosis", generate_diagnosis)
    workflow.add_node("format_response", format_response)

    # Define edges
    workflow.set_entry_point("extract_symptoms")
    workflow.add_edge("extract_symptoms", "retrieve_docs")
    workflow.add_edge("retrieve_docs", "retrieve_issues")
    workflow.add_edge("retrieve_issues", "generate_diagnosis")
    workflow.add_edge("generate_diagnosis", "format_response")
    workflow.add_edge("format_response", END)

    return workflow.compile()


# Compiled graph instance
diagnostic_graph = build_diagnostic_graph()


def process_freed_message(user_id: str, message: str) -> str:
    """
    Main entry point for diagnostic processing

    Args:
        user_id: WhatsApp user ID
        message: User's message/complaint

    Returns:
        Formatted diagnostic response
    """
    initial_state: DiagnosticState = {
        "user_id": user_id,
        "message": message,
        "symptoms": [],
        "vehicle_info": {"model": "Honda Freed GB3/GB4", "year_range": "2008-2016"},
        "retrieved_docs": [],
        "common_issues": [],
        "diagnosis": "",
        "recommendations": [],
        "cost_estimate": {},
        "response": ""
    }

    try:
        result = diagnostic_graph.invoke(initial_state)
        return result["response"]
    except Exception as e:
        return f"""⚠️ *SYSTEM ERROR*

Maaf, terjadi kesalahan dalam memproses permintaan Anda.
Error: {str(e)}

Silakan coba lagi atau hubungi admin.
"""
