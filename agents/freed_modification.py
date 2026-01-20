#!/usr/bin/env python3
"""
Honda Freed Modification Agent - LangGraph Implementation
Handles modification planning for Honda Freed GB3/GB4 (2008-2016)
"""
import os
from typing import TypedDict, List, Optional
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)


class ModificationState(TypedDict):
    """State for modification workflow"""
    user_id: str
    message: str
    requested_stage: Optional[int]
    budget: Optional[int]
    focus_area: str  # engine, suspension, exterior, interior, audio
    available_parts: List[dict]
    stage_preset: Optional[dict]
    modification_plan: str
    total_cost: dict
    response: str


MODIFICATION_SYSTEM_PROMPT = """Kamu adalah tuner specialist Honda Freed dengan pengalaman membangun 100+ Freed modifikasi.

HONDA FREED L15A ENGINE SPECS (Stock):
- Power: 117 HP @ 6,600 RPM
- Torque: 146 Nm @ 4,800 RPM
- Compression: 10.4:1
- Redline: 6,800 RPM
- CVT gear ratio: 2.631-0.408

STAGE MODIFICATION GUIDE:

🟢 STAGE 1 - Street Sleeper (Target: 130-140 HP)
Budget: Rp 8-15 juta
- Cold Air Intake (K&N/Simota): +5-8 HP
- Performance air filter: +3-5 HP
- Exhaust header 4-2-1: +5-8 HP
- Free flow muffler: +3-5 HP
- ECU tune (Hondata/KTuner): +10-15 HP
- NGK Iridium spark plugs: improved combustion

🟡 STAGE 2 - Weekend Warrior (Target: 150-165 HP)
Budget: Rp 25-45 juta
- Include semua Stage 1 +
- Throttle body upgrade (60mm): +5-8 HP
- Fuel injector upgrade (440cc): supports higher HP
- Camshaft upgrade (mild): +10-15 HP
- Lightweight pulley set: +3-5 HP
- Sport clutch kit (for manual): better power transfer
- CVT cooler (for CVT): reliability
- Coilover suspension (Tein/BC): handling
- Upgraded brakes (Brembo): safety

🔴 STAGE 3 - Track Monster (Target: 175-200 HP)
Budget: Rp 60-120 juta
- Include semua Stage 2 +
- Supercharger kit (Sprintex/Kraftwerks): +40-60 HP
- Forged internals: durability
- Built CVT/transmission: handle power
- Full roll cage: safety
- Carbon fiber parts: weight reduction
- Full aero kit: downforce

IMPORTANT NOTES:
- CVT dapat handle max ~160 HP tanpa rebuild
- Di atas 160 HP perlu CVT cooler + rebuilt CVT
- Manual transmission lebih kuat untuk high HP builds
- Selalu balance power dengan handling dan brakes

Selalu berikan rekomendasi dalam Bahasa Indonesia dengan format yang jelas."""


def parse_request(state: ModificationState) -> ModificationState:
    """Parse modification request from user message"""
    message = state["message"].lower()

    # Detect stage request
    if "stage 1" in message or "stage1" in message:
        state["requested_stage"] = 1
    elif "stage 2" in message or "stage2" in message:
        state["requested_stage"] = 2
    elif "stage 3" in message or "stage3" in message:
        state["requested_stage"] = 3

    # Detect focus area
    focus_keywords = {
        "engine": ["mesin", "engine", "power", "hp", "turbo", "supercharger", "intake", "exhaust"],
        "suspension": ["kaki", "suspension", "coilover", "per", "shockbreaker", "handling"],
        "exterior": ["body", "bodykit", "aero", "spoiler", "widebody", "exterior"],
        "interior": ["interior", "jok", "seat", "dashboard", "racing seat"],
        "audio": ["audio", "speaker", "subwoofer", "amplifier", "head unit"],
        "brakes": ["rem", "brake", "brembo", "caliper", "rotor"],
    }

    state["focus_area"] = "engine"  # default
    for area, keywords in focus_keywords.items():
        if any(kw in message for kw in keywords):
            state["focus_area"] = area
            break

    # Detect budget
    import re
    budget_match = re.search(r'(\d+)\s*(jt|juta|jt|million)', message)
    if budget_match:
        state["budget"] = int(budget_match.group(1)) * 1_000_000

    return state


def retrieve_stage_preset(state: ModificationState) -> ModificationState:
    """Retrieve stage preset from database"""
    from database.supabase_client import supabase

    if state["requested_stage"]:
        try:
            result = supabase.table("stage_presets").select("*").eq(
                "stage", state["requested_stage"]
            ).execute()

            if result.data:
                state["stage_preset"] = result.data[0]
        except Exception as e:
            print(f"Stage preset error: {e}")

    return state


def retrieve_parts(state: ModificationState) -> ModificationState:
    """Retrieve matching parts from catalog"""
    from database.supabase_client import supabase

    try:
        query = supabase.table("modification_catalog").select("*")

        # Filter by focus area category if available
        if state["focus_area"]:
            query = query.ilike("category", f"%{state['focus_area']}%")

        # Filter by stage if requested
        if state["requested_stage"]:
            query = query.lte("min_stage", state["requested_stage"])

        result = query.limit(20).execute()
        state["available_parts"] = result.data if result.data else []

    except Exception as e:
        print(f"Parts retrieval error: {e}")
        state["available_parts"] = []

    return state


def generate_modification_plan(state: ModificationState) -> ModificationState:
    """Generate modification plan using LLM"""

    parts_info = ""
    if state["available_parts"]:
        parts_info = "📦 PARTS TERSEDIA DI KATALOG:\n"
        for part in state["available_parts"][:15]:
            price = part.get('price_range_idr', {})
            gain = part.get('performance_gain', {})
            parts_info += (
                f"- {part.get('part_name', 'N/A')} ({part.get('brand', 'N/A')}): "
                f"Rp {price.get('min', 0):,} - Rp {price.get('max', 0):,}"
            )
            if gain:
                parts_info += f" | Gain: {gain}"
            parts_info += f" | Status: {part.get('legal_status', 'N/A')}\n"

    stage_info = ""
    if state["stage_preset"]:
        preset = state["stage_preset"]
        cost = preset.get('estimated_cost_idr', {})
        stage_info = f"""
🎯 STAGE {preset.get('stage')} - {preset.get('stage_name')}
Target HP: {preset.get('estimated_hp_total')} HP
Budget Range: Rp {cost.get('min', 0):,} - Rp {cost.get('max', 0):,}
"""

    budget_info = ""
    if state["budget"]:
        budget_info = f"\n💰 BUDGET USER: Rp {state['budget']:,}"

    messages = [
        SystemMessage(content=MODIFICATION_SYSTEM_PROMPT),
        HumanMessage(content=f"""
REQUEST USER:
{state["message"]}

{stage_info}
{budget_info}

FOKUS AREA: {state["focus_area"]}

{parts_info}

Buatkan modification plan yang detail dengan:
1. Part list lengkap dengan harga
2. Urutan pemasangan yang benar
3. Estimasi HP gain per part
4. Total biaya (parts + installation)
5. Workshop recommendation (general tips)
6. Peringatan penting (garansi void, legal status, dll)
""")
    ]

    response = llm.invoke(messages)
    state["modification_plan"] = response.content

    return state


def calculate_total_cost(state: ModificationState) -> ModificationState:
    """Calculate total modification cost"""

    total_min = 0
    total_max = 0

    for part in state["available_parts"]:
        price = part.get('price_range_idr', {})
        total_min += price.get('min', 0)
        total_max += price.get('max', 0)

    # Add installation estimate (20-30% of parts cost)
    install_min = int(total_min * 0.2)
    install_max = int(total_max * 0.3)

    state["total_cost"] = {
        "parts_min": total_min,
        "parts_max": total_max,
        "install_min": install_min,
        "install_max": install_max,
        "total_min": total_min + install_min,
        "total_max": total_max + install_max
    }

    return state


def format_response(state: ModificationState) -> ModificationState:
    """Format final response for WhatsApp"""

    stage_header = ""
    if state["requested_stage"]:
        stage_names = {1: "Street Sleeper", 2: "Weekend Warrior", 3: "Track Monster"}
        stage_header = f"*STAGE {state['requested_stage']} - {stage_names.get(state['requested_stage'], '')}*\n\n"

    cost = state.get("total_cost", {})
    cost_summary = ""
    if cost:
        cost_summary = f"""
---
💰 *ESTIMASI BIAYA*
Parts: Rp {cost.get('parts_min', 0):,} - Rp {cost.get('parts_max', 0):,}
Install: Rp {cost.get('install_min', 0):,} - Rp {cost.get('install_max', 0):,}
*TOTAL: Rp {cost.get('total_min', 0):,} - Rp {cost.get('total_max', 0):,}*
"""

    response = f"""🏎️ *MODIFICATION PLAN HONDA FREED*
{stage_header}
{state["modification_plan"]}
{cost_summary}
---
⚠️ _Modifikasi dapat membatalkan garansi pabrikan._
_Pastikan semua part legal untuk penggunaan jalan raya._

Ketik:
• *STAGE [1/2/3]* - lihat paket modifikasi lain
• *BENGKEL [kota]* - cari bengkel modifikasi
• *DIAGNOSA [keluhan]* - diagnosa masalah
"""

    state["response"] = response
    return state


def build_modification_graph() -> StateGraph:
    """Build the modification workflow graph"""
    workflow = StateGraph(ModificationState)

    # Add nodes
    workflow.add_node("parse_request", parse_request)
    workflow.add_node("retrieve_stage", retrieve_stage_preset)
    workflow.add_node("retrieve_parts", retrieve_parts)
    workflow.add_node("generate_plan", generate_modification_plan)
    workflow.add_node("calculate_cost", calculate_total_cost)
    workflow.add_node("format_response", format_response)

    # Define edges
    workflow.set_entry_point("parse_request")
    workflow.add_edge("parse_request", "retrieve_stage")
    workflow.add_edge("retrieve_stage", "retrieve_parts")
    workflow.add_edge("retrieve_parts", "generate_plan")
    workflow.add_edge("generate_plan", "calculate_cost")
    workflow.add_edge("calculate_cost", "format_response")
    workflow.add_edge("format_response", END)

    return workflow.compile()


# Compiled graph instance
modification_graph = build_modification_graph()


def process_modification_request(user_id: str, message: str, vehicle_context: dict = None) -> str:
    """
    Main entry point for modification planning

    Args:
        user_id: WhatsApp user ID
        message: User's modification request
        vehicle_context: Optional vehicle context dict

    Returns:
        Formatted modification plan response
    """
    initial_state: ModificationState = {
        "user_id": user_id,
        "message": message,
        "requested_stage": None,
        "budget": None,
        "focus_area": "engine",
        "available_parts": [],
        "stage_preset": None,
        "modification_plan": "",
        "total_cost": {},
        "response": ""
    }

    try:
        result = modification_graph.invoke(initial_state)
        return result["response"]
    except Exception as e:
        return f"""⚠️ *SYSTEM ERROR*

Maaf, terjadi kesalahan dalam memproses permintaan modifikasi.
Error: {str(e)}

Silakan coba lagi atau hubungi admin.
"""


def get_stage_summary(stage: int) -> str:
    """Get quick summary of a modification stage"""
    from database.supabase_client import supabase

    try:
        result = supabase.table("stage_presets").select("*").eq("stage", stage).execute()

        if result.data:
            preset = result.data[0]
            cost = preset.get('estimated_cost_idr', {})
            return f"""🎯 *STAGE {stage} - {preset.get('stage_name')}*

Target Power: {preset.get('estimated_hp_total')} HP
Budget: Rp {cost.get('min', 0):,} - Rp {cost.get('max', 0):,}

Ketik *STAGE {stage} detail* untuk info lengkap.
"""
    except Exception as e:
        print(f"Stage summary error: {e}")

    return f"Stage {stage} tidak ditemukan."
