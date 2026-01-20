#!/usr/bin/env python3
"""
Honda Freed Superchatbot - Database Seeding Script
Seeds service manuals, common issues, and modification catalog
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
from database.supabase_client import supabase

# Initialize embedding model
print("Loading embedding model...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')


# ============================================
# HONDA FREED SERVICE MANUAL DATA
# ============================================
SERVICE_MANUALS = [
    # ENGINE - L15A i-VTEC
    {
        "section": "Engine - L15A i-VTEC Specifications",
        "subsection": "General Specifications",
        "content": """Honda Freed menggunakan mesin L15A i-VTEC 1.5L SOHC 16 valve. Spesifikasi: Displacement 1497cc, Bore x Stroke 73.0 x 89.4mm, Compression Ratio 10.4:1, Max Power 117 HP @ 6600 RPM, Max Torque 146 Nm @ 4800 RPM. Sistem i-VTEC mengaktifkan di 2500-3000 RPM untuk efisiensi bahan bakar optimal. Mesin menggunakan timing chain (bukan belt) sehingga tidak memerlukan penggantian berkala.""",
        "tags": ["engine", "L15A", "i-VTEC", "specifications", "power", "torque"]
    },
    {
        "section": "Engine - Oil System",
        "subsection": "Oil Change Procedure",
        "content": """Kapasitas oli mesin Honda Freed: 3.5L dengan filter, 3.2L tanpa filter. Spesifikasi oli yang direkomendasikan: 0W-20 (utama) atau 5W-30 (alternatif untuk cuaca panas). Interval penggantian: setiap 10,000 km atau 6 bulan, mana yang lebih dulu. Prosedur: 1) Hangatkan mesin 2-3 menit, 2) Matikan mesin, buka drain plug (17mm), 3) Ganti oil filter, 4) Pasang drain plug dengan torque 29 Nm, 5) Isi oli baru, 6) Cek level dengan dipstick.""",
        "tags": ["engine", "oil", "maintenance", "change", "filter", "drain"]
    },
    {
        "section": "Engine - Cooling System",
        "subsection": "Coolant Specifications",
        "content": """Sistem pendingin Honda Freed memiliki kapasitas total 5.4L. Gunakan Honda All Season Antifreeze/Coolant Type 2 (biru) atau setara dengan spesifikasi JIS K 2234. Campuran 50:50 dengan air suling. Interval penggantian: setiap 200,000 km atau 10 tahun (initial), kemudian setiap 100,000 km atau 5 tahun. Thermostat membuka pada suhu 76-80°C. Tekanan tutup radiator: 108 kPa.""",
        "tags": ["engine", "cooling", "coolant", "radiator", "thermostat", "overheating"]
    },
    {
        "section": "Engine - Spark Plugs",
        "subsection": "Spark Plug Replacement",
        "content": """Honda Freed L15A menggunakan spark plug NGK IZFR6K-11 (Iridium) atau DENSO SK20R11. Gap: 1.0-1.1mm. Torque pemasangan: 18 Nm. Interval penggantian: Iridium 160,000 km, Standard 40,000 km. Gejala spark plug aus: idle kasar, akselerasi lemah, fuel economy menurun, susah start saat dingin. Selalu ganti 4 busi sekaligus untuk performa optimal.""",
        "tags": ["engine", "spark plug", "ignition", "NGK", "DENSO", "maintenance"]
    },
    {
        "section": "Engine - Throttle Body",
        "subsection": "Throttle Body Cleaning",
        "content": """Throttle body Honda Freed drive-by-wire (DBW) dengan diameter 48mm. Pembersihan direkomendasikan setiap 40,000 km atau jika idle kasar. Prosedur: 1) Disconnect battery 10 menit, 2) Remove air intake hose, 3) Spray throttle cleaner pada butterfly valve, 4) Bersihkan dengan kain microfiber, 5) Reconnect battery, 6) Idle relearn: nyalakan mesin, biarkan idle 10 menit tanpa menyentuh pedal gas.""",
        "tags": ["engine", "throttle body", "cleaning", "idle", "DBW", "maintenance"]
    },
    # CVT TRANSMISSION
    {
        "section": "Transmission - CVT Overview",
        "subsection": "CVT Specifications",
        "content": """Honda Freed menggunakan CVT (Continuously Variable Transmission) dengan torque converter. Gear ratio: 2.631-0.408 (forward), 1.845 (reverse). Kapasitas CVT fluid: 3.1L (drain and refill), 6.2L (total capacity). CVT fluid type: Honda HCF-2 atau setara. Interval penggantian: setiap 40,000 km untuk kondisi normal, 20,000 km untuk kondisi berat (macet, panas ekstrem).""",
        "tags": ["transmission", "CVT", "fluid", "specifications", "gear ratio"]
    },
    {
        "section": "Transmission - CVT Maintenance",
        "subsection": "CVT Fluid Change",
        "content": """Prosedur ganti CVT fluid Honda Freed: 1) Hangatkan transmisi dengan berkendara 10-15 menit, 2) Angkat kendaraan, buka drain plug (3/8 square), 3) Keluarkan fluid lama (sekitar 3.1L), 4) Pasang drain plug dengan washer baru, torque 49 Nm, 5) Isi fluid baru melalui dipstick tube, 6) Cek level saat mesin menyala pada N position, suhu 35-45°C. PENTING: Hanya gunakan Honda HCF-2, fluid lain dapat merusak CVT.""",
        "tags": ["transmission", "CVT", "fluid", "maintenance", "drain", "fill"]
    },
    {
        "section": "Transmission - CVT Problems",
        "subsection": "CVT Judder Diagnosis",
        "content": """CVT judder/getar adalah masalah umum Honda Freed. Gejala: getar/vibration saat akselerasi dari diam, terutama pada 15-30 km/h. Penyebab: 1) CVT fluid degradasi - ganti fluid, 2) Torque converter clutch slip - flush system, 3) Start clutch wear - perlu rebuild. Solusi bertahap: a) Ganti CVT fluid dengan HCF-2 original, b) Jika masih getar setelah 500km, lakukan CVT flush 2x drain-fill, c) Jika tetap ada, perlu inspeksi torque converter.""",
        "tags": ["transmission", "CVT", "judder", "vibration", "problem", "diagnosis"]
    },
    # SUSPENSION
    {
        "section": "Suspension - Front",
        "subsection": "Front Suspension Overview",
        "content": """Honda Freed menggunakan MacPherson strut di depan dengan lower arm dan stabilizer bar. Komponen yang perlu diperhatikan: 1) Ball joint - cek setiap 40,000 km, ganti jika ada play, 2) Tie rod end - cek boot dan play, 3) Stabilizer link - sering aus, bunyi kletek saat jalan tidak rata, 4) Strut mount/bearing - bunyi saat belok, 5) Shock absorber - cek bocor dan bounce test.""",
        "tags": ["suspension", "front", "MacPherson", "ball joint", "tie rod", "stabilizer"]
    },
    {
        "section": "Suspension - Rear",
        "subsection": "Rear Suspension Overview",
        "content": """Suspensi belakang Honda Freed menggunakan torsion beam dengan coil spring dan shock absorber terpisah. Komponen: 1) Shock absorber - cek kebocoran oli, 2) Coil spring - cek patah/turun, 3) Trailing arm bushing - aus menyebabkan handling tidak stabil, 4) Wheel bearing - bunyi dengung saat kecepatan tinggi. Alignment belakang: Toe -0.08° sampai +0.08°, Camber fixed.""",
        "tags": ["suspension", "rear", "torsion beam", "shock", "spring", "bearing"]
    },
    # BRAKES
    {
        "section": "Brakes - Overview",
        "subsection": "Brake System Specifications",
        "content": """Sistem rem Honda Freed: Disc brake ventilated di depan (262mm), drum brake di belakang (180mm). Dilengkapi ABS dan EBD. Ketebalan pad depan minimum: 1.6mm (service limit), baru 10.0mm. Ketebalan disc minimum: 24.0mm (service limit), baru 26.0mm. Interval penggantian pad: 30,000-50,000 km tergantung gaya berkendara. Brake fluid: DOT 3 atau DOT 4, ganti setiap 3 tahun.""",
        "tags": ["brakes", "disc", "drum", "ABS", "pad", "rotor", "fluid"]
    },
    {
        "section": "Brakes - Pad Replacement",
        "subsection": "Front Brake Pad Procedure",
        "content": """Prosedur ganti brake pad depan Honda Freed: 1) Kendorkan baut roda, jack up dan pasang stand, 2) Lepas roda, 3) Lepas 2 baut caliper slide pin (14mm), 4) Angkat caliper, gantung dengan kawat (jangan biarkan menggantung di hose), 5) Keluarkan pad lama, 6) Tekan piston dengan C-clamp (buka tutup reservoir), 7) Pasang pad baru dengan anti-squeal shim, 8) Pasang caliper, torque slide pin 37 Nm, 9) Pompa pedal rem sebelum jalan.""",
        "tags": ["brakes", "pad", "replacement", "caliper", "procedure", "front"]
    },
    # AC SYSTEM
    {
        "section": "AC System - Overview",
        "subsection": "AC Specifications",
        "content": """Sistem AC Honda Freed menggunakan refrigerant R-134a dengan kapasitas 400-450g. Komponen utama: Kompresor (electric clutch type), Kondensor (di depan radiator), Evaporator (di dashboard), Expansion valve. Tekanan normal: Low side 1.5-2.5 kg/cm², High side 14-16 kg/cm² pada idle dengan AC max. Interval servis: Cek refrigerant level setiap tahun, ganti cabin filter setiap 15,000 km.""",
        "tags": ["AC", "air conditioning", "refrigerant", "R-134a", "compressor", "cooling"]
    },
    {
        "section": "AC System - Troubleshooting",
        "subsection": "AC Not Cold Diagnosis",
        "content": """Diagnosa AC tidak dingin Honda Freed: 1) Cek tekanan refrigerant - low pressure = bocor/kurang freon, 2) Cek kompresor clutch engage - tidak engage = cek relay/fuse/clutch coil, 3) Cek kondensor - kotor = bersihkan dengan air, 4) Cek cabin filter - tersumbat = ganti, 5) Cek blower - lemah = cek resistor/motor, 6) Cek expansion valve - stuck = AC kadang dingin kadang tidak. Lokasi kebocoran umum: O-ring fitting, condenser, evaporator.""",
        "tags": ["AC", "troubleshooting", "diagnosis", "not cold", "compressor", "refrigerant"]
    },
    # ELECTRICAL
    {
        "section": "Electrical - Battery",
        "subsection": "Battery Specifications",
        "content": """Honda Freed menggunakan battery 12V 45Ah (46B24L atau setara). Lokasi: di engine bay sebelah kiri. Alternator output: 13.5-14.5V saat mesin jalan. Arus charging normal: 30-80A tergantung beban. Gejala battery lemah: starter lambat, lampu redup saat start, check battery warning. Umur battery normal: 2-4 tahun. Tips: jaga terminal bersih dari korosi, cek elektrolit jika battery konvensional.""",
        "tags": ["electrical", "battery", "alternator", "charging", "voltage", "starter"]
    },
    {
        "section": "Electrical - Common Problems",
        "subsection": "Electrical Troubleshooting",
        "content": """Masalah kelistrikan umum Honda Freed: 1) Lampu dashboard mati - cek fuse di fuse box (bawah dashboard kiri), 2) Power window lemah - cek motor/regulator, 3) Central lock tidak fungsi - cek actuator dan main relay, 4) Audio mati - cek fuse ACC 7.5A, 5) Klakson tidak bunyi - cek relay dan horn pad. Fuse box utama ada 2 lokasi: di bawah dashboard (interior) dan di engine bay (dekat battery).""",
        "tags": ["electrical", "fuse", "troubleshooting", "power window", "central lock", "audio"]
    },
    # STEERING
    {
        "section": "Steering - EPS System",
        "subsection": "Electric Power Steering",
        "content": """Honda Freed menggunakan Electric Power Steering (EPS) tanpa hydraulic fluid. Keuntungan: lebih efisien, tidak ada kebocoran oli power steering. Komponen: EPS motor (di steering column), EPS ECU, torque sensor. Masalah umum: 1) Stir berat - cek EPS fuse, EPS warning light, 2) Stir tidak center - perlu alignment, 3) Bunyi saat belok - cek steering column bearing. Warning light EPS menyala = scan dengan HDS.""",
        "tags": ["steering", "EPS", "electric", "power steering", "alignment"]
    },
]


# ============================================
# COMMON ISSUES DATA
# ============================================
COMMON_ISSUES = [
    {
        "symptom": "CVT getar/judder saat akselerasi",
        "symptom_detail": "Mobil bergetar saat akselerasi dari diam, terutama di kecepatan 15-30 km/h. Getar terasa di seluruh bodi.",
        "probable_cause": ["CVT fluid degradasi", "Torque converter clutch slip", "Start clutch wear"],
        "diagnostic_steps": [
            "Cek kondisi dan warna CVT fluid",
            "Test drive untuk konfirmasi gejala",
            "Scan ECU untuk error code",
            "Cek riwayat penggantian CVT fluid"
        ],
        "part_codes": ["08200-HCF2", "CVT Fluid HCF-2"],
        "cost_estimate_idr": {"min": 500000, "max": 3000000},
        "urgency": "medium"
    },
    {
        "symptom": "AC tidak dingin",
        "symptom_detail": "AC hidup tapi hembusan tidak dingin atau kurang dingin. Kompresor mungkin tidak engage.",
        "probable_cause": ["Refrigerant habis/bocor", "Kompresor rusak", "Kondensor kotor", "Expansion valve stuck"],
        "diagnostic_steps": [
            "Cek tekanan refrigerant dengan manifold gauge",
            "Cek apakah kompresor clutch engage",
            "Periksa kondensor dari kotoran",
            "Cek cabin filter"
        ],
        "part_codes": ["R-134a Refrigerant", "38800-RB0-003 Compressor"],
        "cost_estimate_idr": {"min": 200000, "max": 5000000},
        "urgency": "low"
    },
    {
        "symptom": "Bunyi gluduk/kletek dari depan",
        "symptom_detail": "Bunyi gluduk atau kletek saat melewati jalan tidak rata, polisi tidur, atau saat belok.",
        "probable_cause": ["Stabilizer link aus", "Ball joint aus", "Tie rod end aus", "Strut mount rusak"],
        "diagnostic_steps": [
            "Angkat mobil dan cek play di stabilizer link",
            "Cek play ball joint dengan mencungkil",
            "Cek tie rod end dengan menggoyang roda",
            "Cek kondisi strut mount"
        ],
        "part_codes": ["51320-SNA-A02 Ball Joint", "51321-SNA-A01 Stabilizer Link", "53540-SNA-A01 Tie Rod End"],
        "cost_estimate_idr": {"min": 300000, "max": 2000000},
        "urgency": "medium"
    },
    {
        "symptom": "Idle kasar/tidak stabil",
        "symptom_detail": "Putaran mesin tidak stabil saat idle, kadang hampir mati. RPM naik turun.",
        "probable_cause": ["Throttle body kotor", "IACV bermasalah", "Spark plug aus", "Air filter kotor"],
        "diagnostic_steps": [
            "Scan ECU untuk error code",
            "Bersihkan throttle body",
            "Cek kondisi spark plug",
            "Ganti air filter jika kotor"
        ],
        "part_codes": ["16400-RB0-003 Throttle Body", "IZFR6K-11 Spark Plug", "17220-RB0-000 Air Filter"],
        "cost_estimate_idr": {"min": 150000, "max": 1500000},
        "urgency": "low"
    },
    {
        "symptom": "Rem bunyi/berdecit",
        "symptom_detail": "Bunyi decit atau grinding saat mengerem. Mungkin disertai getaran di pedal rem.",
        "probable_cause": ["Brake pad habis", "Disc rotor aus/warped", "Caliper macet", "Brake pad glazing"],
        "diagnostic_steps": [
            "Cek ketebalan brake pad",
            "Cek kondisi disc rotor (ketebalan dan kerataan)",
            "Periksa caliper slide pin",
            "Cek brake fluid level"
        ],
        "part_codes": ["45022-TF0-J51 Front Pad Set", "45251-TF0-J50 Front Disc Rotor"],
        "cost_estimate_idr": {"min": 400000, "max": 2500000},
        "urgency": "high"
    },
    {
        "symptom": "Mesin panas/overheat",
        "symptom_detail": "Temperatur mesin naik ke zona merah, warning light menyala, mungkin ada uap dari kap mesin.",
        "probable_cause": ["Coolant habis/bocor", "Thermostat stuck closed", "Kipas radiator mati", "Water pump rusak"],
        "diagnostic_steps": [
            "Cek level coolant di reservoir",
            "Periksa kebocoran di hose dan radiator",
            "Cek operasi kipas radiator",
            "Test thermostat"
        ],
        "part_codes": ["19301-RNA-315 Thermostat", "19030-RB0-004 Fan Motor", "19200-RB0-003 Water Pump"],
        "cost_estimate_idr": {"min": 200000, "max": 3500000},
        "urgency": "critical"
    },
    {
        "symptom": "Susah start/starter lemah",
        "symptom_detail": "Mesin lambat atau sulit distart. Bunyi starter lemah atau hanya bunyi klik.",
        "probable_cause": ["Battery lemah", "Starter motor aus", "Kabel battery longgar/korosi", "Alternator rusak"],
        "diagnostic_steps": [
            "Test tegangan battery (harus >12.4V)",
            "Cek kabel battery dari korosi",
            "Test arus cranking battery",
            "Test output alternator saat mesin jalan"
        ],
        "part_codes": ["31200-RB0-004 Starter Motor", "46B24L Battery", "31100-RB0-004 Alternator"],
        "cost_estimate_idr": {"min": 200000, "max": 4000000},
        "urgency": "high"
    },
    {
        "symptom": "Konsumsi BBM boros",
        "symptom_detail": "Fuel economy menurun signifikan dari normal (di bawah 10 km/L dalam kota).",
        "probable_cause": ["Air filter kotor", "Spark plug aus", "Injector kotor", "O2 sensor error", "Ban tekanan kurang"],
        "diagnostic_steps": [
            "Cek dan ganti air filter",
            "Cek kondisi spark plug",
            "Scan ECU untuk error code (terutama O2 sensor)",
            "Cek tekanan ban"
        ],
        "part_codes": ["17220-RB0-000 Air Filter", "IZFR6K-11 Spark Plug", "36531-RB0-003 O2 Sensor"],
        "cost_estimate_idr": {"min": 100000, "max": 2000000},
        "urgency": "low"
    },
    {
        "symptom": "Stir berat",
        "symptom_detail": "Steering terasa berat, terutama saat parkir atau kecepatan rendah.",
        "probable_cause": ["EPS motor rusak", "EPS fuse putus", "Torque sensor error", "Ban tekanan kurang"],
        "diagnostic_steps": [
            "Cek EPS warning light di dashboard",
            "Cek fuse EPS di fuse box",
            "Scan ECU untuk EPS error code",
            "Cek tekanan ban"
        ],
        "part_codes": ["53600-TF0-003 EPS Motor Assembly"],
        "cost_estimate_idr": {"min": 100000, "max": 8000000},
        "urgency": "medium"
    },
    {
        "symptom": "Check engine light menyala",
        "symptom_detail": "Lampu MIL (Malfunction Indicator Lamp) menyala di dashboard. Mesin mungkin masih jalan normal.",
        "probable_cause": ["O2 sensor fault", "Catalytic converter issue", "EVAP system leak", "Misfire detected"],
        "diagnostic_steps": [
            "Scan OBD2 untuk membaca DTC (Diagnostic Trouble Code)",
            "Catat kode error yang muncul",
            "Diagnosa berdasarkan kode spesifik",
            "Clear code dan test drive untuk konfirmasi"
        ],
        "part_codes": ["Varies based on DTC"],
        "cost_estimate_idr": {"min": 50000, "max": 5000000},
        "urgency": "medium"
    },
]


# ============================================
# MODIFICATION PARTS CATALOG (50+ items)
# ============================================
MODIFICATION_PARTS = [
    # === ENGINE - AIR INTAKE ===
    {
        "part_name": "Cold Air Intake Kit",
        "brand": "K&N",
        "category": "engine",
        "subcategory": "air intake",
        "description": "High-flow cold air intake system dengan heat shield untuk mesin L15A",
        "performance_gain": {"hp": "+5-8", "torque": "+8-10 Nm"},
        "price_range_idr": {"min": 3500000, "max": 5000000},
        "installation_time_hours": 1.5,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Perlu tune ulang untuk hasil optimal"
    },
    {
        "part_name": "Replacement Air Filter",
        "brand": "K&N",
        "category": "engine",
        "subcategory": "air intake",
        "description": "Drop-in replacement filter high-flow washable",
        "performance_gain": {"hp": "+3-5"},
        "price_range_idr": {"min": 800000, "max": 1200000},
        "installation_time_hours": 0.25,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Bisa dicuci dan dipakai ulang"
    },
    {
        "part_name": "Open Pod Air Filter Kit",
        "brand": "Simota",
        "category": "engine",
        "subcategory": "air intake",
        "description": "Open pod filter dengan velocity stack",
        "performance_gain": {"hp": "+5-8"},
        "price_range_idr": {"min": 1500000, "max": 2500000},
        "installation_time_hours": 1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Suara intake lebih kencang"
    },
    # === ENGINE - EXHAUST ===
    {
        "part_name": "Header 4-2-1",
        "brand": "ORD",
        "category": "engine",
        "subcategory": "exhaust",
        "description": "Stainless steel 4-2-1 header untuk L15A",
        "performance_gain": {"hp": "+5-8", "torque": "+8-12 Nm"},
        "price_range_idr": {"min": 2500000, "max": 4000000},
        "installation_time_hours": 3,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Check engine light mungkin menyala jika tanpa tune"
    },
    {
        "part_name": "Downpipe High Flow",
        "brand": "Tanabe",
        "category": "engine",
        "subcategory": "exhaust",
        "description": "60mm stainless steel downpipe",
        "performance_gain": {"hp": "+3-5"},
        "price_range_idr": {"min": 2000000, "max": 3500000},
        "installation_time_hours": 2,
        "min_stage": 1,
        "legal_status": "Gray Area",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Cek regulasi emisi lokal"
    },
    {
        "part_name": "Muffler Bolt-On",
        "brand": "HKS",
        "category": "engine",
        "subcategory": "exhaust",
        "description": "Hi-Power muffler universal bolt-on",
        "performance_gain": {"hp": "+3-5"},
        "price_range_idr": {"min": 3000000, "max": 5500000},
        "installation_time_hours": 1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Suara lebih sporty"
    },
    {
        "part_name": "Full Exhaust System",
        "brand": "Fujitsubo",
        "category": "engine",
        "subcategory": "exhaust",
        "description": "Header-back full exhaust system stainless",
        "performance_gain": {"hp": "+10-15", "torque": "+12-18 Nm"},
        "price_range_idr": {"min": 8000000, "max": 15000000},
        "installation_time_hours": 4,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Best value untuk performance exhaust"
    },
    # === ENGINE - ECU/TUNING ===
    {
        "part_name": "ECU Tune",
        "brand": "Hondata",
        "category": "engine",
        "subcategory": "tuning",
        "description": "FlashPro ECU tuning untuk L15A dengan base map",
        "performance_gain": {"hp": "+10-15", "torque": "+15-20 Nm"},
        "price_range_idr": {"min": 8000000, "max": 12000000},
        "installation_time_hours": 2,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Wajib untuk full Stage 1. Custom tune available"
    },
    {
        "part_name": "ECU Tune Kit",
        "brand": "KTuner",
        "category": "engine",
        "subcategory": "tuning",
        "description": "KTuner V2 untuk Honda dengan cable dan software",
        "performance_gain": {"hp": "+10-15", "torque": "+15-20 Nm"},
        "price_range_idr": {"min": 6500000, "max": 9000000},
        "installation_time_hours": 2,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Alternatif Hondata yang lebih affordable"
    },
    {
        "part_name": "Piggyback ECU",
        "brand": "Dastek Unichip",
        "category": "engine",
        "subcategory": "tuning",
        "description": "Piggyback ECU untuk fuel dan ignition tuning",
        "performance_gain": {"hp": "+8-12"},
        "price_range_idr": {"min": 5000000, "max": 7500000},
        "installation_time_hours": 3,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Tidak void ECU warranty"
    },
    # === ENGINE - IGNITION ===
    {
        "part_name": "Iridium Spark Plugs (set of 4)",
        "brand": "NGK",
        "category": "engine",
        "subcategory": "ignition",
        "description": "NGK Iridium IX spark plugs untuk L15A",
        "performance_gain": {"hp": "+1-2"},
        "price_range_idr": {"min": 400000, "max": 600000},
        "installation_time_hours": 0.5,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Part number: IZFR6K-11. Recommended untuk semua build"
    },
    {
        "part_name": "Performance Ignition Coils (set of 4)",
        "brand": "MSD",
        "category": "engine",
        "subcategory": "ignition",
        "description": "High-output ignition coils",
        "performance_gain": {"hp": "+2-3"},
        "price_range_idr": {"min": 2500000, "max": 4000000},
        "installation_time_hours": 1,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Untuk build dengan higher compression"
    },
    # === ENGINE - FUEL ===
    {
        "part_name": "Fuel Injectors 440cc (set of 4)",
        "brand": "Bosch",
        "category": "engine",
        "subcategory": "fuel",
        "description": "High-flow fuel injectors untuk forced induction",
        "performance_gain": {"hp": "Supports +50 HP builds"},
        "price_range_idr": {"min": 3500000, "max": 5500000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Wajib untuk forced induction. Perlu tune"
    },
    {
        "part_name": "Fuel Pump High Flow",
        "brand": "Walbro",
        "category": "engine",
        "subcategory": "fuel",
        "description": "255 LPH in-tank fuel pump",
        "performance_gain": {"hp": "Supports +80 HP builds"},
        "price_range_idr": {"min": 2000000, "max": 3000000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Untuk build dengan high power demand"
    },
    {
        "part_name": "Fuel Pressure Regulator Adjustable",
        "brand": "Aeromotive",
        "category": "engine",
        "subcategory": "fuel",
        "description": "Adjustable FPR dengan gauge",
        "performance_gain": {"hp": "Tuning support"},
        "price_range_idr": {"min": 1500000, "max": 2500000},
        "installation_time_hours": 1.5,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Untuk fine-tuning air-fuel ratio"
    },
    # === ENGINE - INTERNALS ===
    {
        "part_name": "Throttle Body 60mm",
        "brand": "Skunk2",
        "category": "engine",
        "subcategory": "throttle",
        "description": "60mm throttle body upgrade dari stock 48mm",
        "performance_gain": {"hp": "+5-8"},
        "price_range_idr": {"min": 4000000, "max": 6000000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Perlu intake manifold adapter"
    },
    {
        "part_name": "Camshaft Stage 2",
        "brand": "Toda Racing",
        "category": "engine",
        "subcategory": "camshaft",
        "description": "Performance camshaft dengan lift dan duration lebih tinggi",
        "performance_gain": {"hp": "+15-20"},
        "price_range_idr": {"min": 8000000, "max": 15000000},
        "installation_time_hours": 8,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Mempengaruhi idle. Perlu tune. Best dengan header dan intake"
    },
    {
        "part_name": "Valve Spring Kit",
        "brand": "Supertech",
        "category": "engine",
        "subcategory": "valvetrain",
        "description": "Dual valve spring kit untuk high RPM",
        "performance_gain": {"hp": "Enables +1000 RPM redline"},
        "price_range_idr": {"min": 4000000, "max": 6000000},
        "installation_time_hours": 6,
        "min_stage": 3,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Untuk aggressive cam builds"
    },
    {
        "part_name": "Lightweight Pulley Set",
        "brand": "Unorthodox Racing",
        "category": "engine",
        "subcategory": "pulleys",
        "description": "Underdrive pulley set (crank, alternator, AC)",
        "performance_gain": {"hp": "+3-5"},
        "price_range_idr": {"min": 2500000, "max": 4000000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Mengurangi parasitic loss"
    },
    # === ENGINE - FORCED INDUCTION ===
    {
        "part_name": "Supercharger Kit",
        "brand": "Kraftwerks",
        "category": "engine",
        "subcategory": "forced induction",
        "description": "Centrifugal supercharger kit lengkap dengan intercooler",
        "performance_gain": {"hp": "+60-80"},
        "price_range_idr": {"min": 45000000, "max": 65000000},
        "installation_time_hours": 16,
        "min_stage": 3,
        "legal_status": "Gray Area",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Perlu forged internals untuk boost tinggi. Perlu professional tune"
    },
    {
        "part_name": "Turbo Kit",
        "brand": "Full-Race",
        "category": "engine",
        "subcategory": "forced induction",
        "description": "Complete turbo kit dengan manifold, turbo, intercooler, piping",
        "performance_gain": {"hp": "+80-120"},
        "price_range_idr": {"min": 55000000, "max": 85000000},
        "installation_time_hours": 24,
        "min_stage": 3,
        "legal_status": "Track Only",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Full engine build required. CVT tidak recommended"
    },
    {
        "part_name": "Intercooler Kit",
        "brand": "Mishimoto",
        "category": "engine",
        "subcategory": "forced induction",
        "description": "Front-mount intercooler untuk forced induction builds",
        "performance_gain": {"hp": "Reduces intake temps 20-30°C"},
        "price_range_idr": {"min": 5000000, "max": 8000000},
        "installation_time_hours": 4,
        "min_stage": 3,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Ukuran disesuaikan dengan boost level"
    },
    # === ENGINE - COOLING ===
    {
        "part_name": "Radiator Aluminum",
        "brand": "Koyo",
        "category": "engine",
        "subcategory": "cooling",
        "description": "Full aluminum racing radiator dual-pass",
        "performance_gain": {"hp": "Better heat management"},
        "price_range_idr": {"min": 4000000, "max": 7000000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "30% lebih efisien dari stock"
    },
    {
        "part_name": "Oil Cooler Kit",
        "brand": "Mishimoto",
        "category": "engine",
        "subcategory": "cooling",
        "description": "Thermostatic oil cooler kit dengan lines dan fittings",
        "performance_gain": {"hp": "Maintains oil temp <110°C"},
        "price_range_idr": {"min": 3500000, "max": 5500000},
        "installation_time_hours": 3,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4", "L15A"],
        "notes": "Recommended untuk track use atau daerah panas"
    },
    {
        "part_name": "CVT Cooler Kit",
        "brand": "Custom",
        "category": "engine",
        "subcategory": "cooling",
        "description": "External CVT fluid cooler dengan thermostat",
        "performance_gain": {"hp": "Extends CVT life"},
        "price_range_idr": {"min": 2500000, "max": 4500000},
        "installation_time_hours": 3,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "WAJIB untuk build di atas 150 HP dengan CVT"
    },
    # === SUSPENSION ===
    {
        "part_name": "Coilover Kit",
        "brand": "Tein",
        "category": "suspension",
        "subcategory": "coilover",
        "description": "Tein Street Basis Z full adjustable height",
        "performance_gain": {"handling": "Improved cornering"},
        "price_range_idr": {"min": 8000000, "max": 12000000},
        "installation_time_hours": 4,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Drop 25-50mm dari stock"
    },
    {
        "part_name": "Coilover Kit Racing",
        "brand": "BC Racing",
        "category": "suspension",
        "subcategory": "coilover",
        "description": "BC Racing BR Series 32-way damping adjustable",
        "performance_gain": {"handling": "Track-ready"},
        "price_range_idr": {"min": 12000000, "max": 18000000},
        "installation_time_hours": 4,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Pillow ball top mount included"
    },
    {
        "part_name": "Lowering Springs",
        "brand": "Eibach",
        "category": "suspension",
        "subcategory": "springs",
        "description": "Eibach Pro-Kit lowering springs",
        "performance_gain": {"handling": "Lower COG"},
        "price_range_idr": {"min": 3500000, "max": 5000000},
        "installation_time_hours": 3,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Drop 25-30mm dengan stock damper"
    },
    {
        "part_name": "Front Strut Bar",
        "brand": "Ultra Racing",
        "category": "suspension",
        "subcategory": "chassis",
        "description": "Front strut tower bar aluminum",
        "performance_gain": {"handling": "Reduced flex"},
        "price_range_idr": {"min": 800000, "max": 1500000},
        "installation_time_hours": 0.5,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Easy bolt-on upgrade"
    },
    {
        "part_name": "Rear Strut Bar",
        "brand": "Ultra Racing",
        "category": "suspension",
        "subcategory": "chassis",
        "description": "Rear strut tower bar aluminum",
        "performance_gain": {"handling": "Reduced flex"},
        "price_range_idr": {"min": 800000, "max": 1500000},
        "installation_time_hours": 0.5,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Pair dengan front bar untuk best result"
    },
    {
        "part_name": "Front Sway Bar",
        "brand": "Whiteline",
        "category": "suspension",
        "subcategory": "sway bar",
        "description": "Adjustable front sway bar 22mm",
        "performance_gain": {"handling": "Reduced body roll"},
        "price_range_idr": {"min": 2500000, "max": 4000000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "3-way adjustable stiffness"
    },
    {
        "part_name": "Rear Sway Bar",
        "brand": "Whiteline",
        "category": "suspension",
        "subcategory": "sway bar",
        "description": "Adjustable rear sway bar 18mm",
        "performance_gain": {"handling": "Better balance"},
        "price_range_idr": {"min": 2500000, "max": 4000000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Tune oversteer/understeer"
    },
    {
        "part_name": "Camber Kit Front",
        "brand": "SPC",
        "category": "suspension",
        "subcategory": "alignment",
        "description": "Adjustable front camber bolts",
        "performance_gain": {"handling": "Proper alignment"},
        "price_range_idr": {"min": 500000, "max": 900000},
        "installation_time_hours": 1,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Wajib setelah lowering"
    },
    # === BRAKES ===
    {
        "part_name": "Brake Pad Performance",
        "brand": "Project Mu",
        "category": "brakes",
        "subcategory": "pads",
        "description": "High-friction street/track brake pads",
        "performance_gain": {"braking": "30% better stopping"},
        "price_range_idr": {"min": 1200000, "max": 2000000},
        "installation_time_hours": 1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "NS400 compound untuk daily + occasional track"
    },
    {
        "part_name": "Brake Pad Racing",
        "brand": "Endless",
        "category": "brakes",
        "subcategory": "pads",
        "description": "Racing compound brake pads",
        "performance_gain": {"braking": "Track performance"},
        "price_range_idr": {"min": 2500000, "max": 4500000},
        "installation_time_hours": 1,
        "min_stage": 3,
        "legal_status": "Track Only",
        "compatibility": ["GB3", "GB4"],
        "notes": "MX72 compound. Butuh warm-up"
    },
    {
        "part_name": "Brake Rotor Slotted",
        "brand": "DBA",
        "category": "brakes",
        "subcategory": "rotors",
        "description": "Slotted brake rotors untuk heat dissipation",
        "performance_gain": {"braking": "Better cooling"},
        "price_range_idr": {"min": 2000000, "max": 3500000},
        "installation_time_hours": 1.5,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "T3 4000 series. Front set"
    },
    {
        "part_name": "Brake Rotor 2-Piece",
        "brand": "AP Racing",
        "category": "brakes",
        "subcategory": "rotors",
        "description": "2-piece floating rotor dengan aluminum hat",
        "performance_gain": {"braking": "Pro-level braking"},
        "price_range_idr": {"min": 8000000, "max": 15000000},
        "installation_time_hours": 2,
        "min_stage": 3,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Reduced unsprung weight"
    },
    {
        "part_name": "Big Brake Kit Front",
        "brand": "Wilwood",
        "category": "brakes",
        "subcategory": "big brake",
        "description": "4-piston caliper dengan 280mm rotor",
        "performance_gain": {"braking": "Massive upgrade"},
        "price_range_idr": {"min": 15000000, "max": 25000000},
        "installation_time_hours": 4,
        "min_stage": 3,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Requires 16\" minimum wheels"
    },
    {
        "part_name": "Brake Lines Stainless",
        "brand": "Goodridge",
        "category": "brakes",
        "subcategory": "lines",
        "description": "Stainless steel braided brake lines",
        "performance_gain": {"braking": "Better pedal feel"},
        "price_range_idr": {"min": 1200000, "max": 2000000},
        "installation_time_hours": 1.5,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Full set 4 lines"
    },
    {
        "part_name": "Brake Fluid Racing",
        "brand": "Motul",
        "category": "brakes",
        "subcategory": "fluid",
        "description": "Motul RBF 600 high temp brake fluid",
        "performance_gain": {"braking": "No fade under heat"},
        "price_range_idr": {"min": 350000, "max": 500000},
        "installation_time_hours": 0.5,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Boiling point 312°C. Ganti setiap tahun"
    },
    # === WHEELS & TIRES ===
    {
        "part_name": "Wheels 16x7 ET42",
        "brand": "Rays Volk Racing",
        "category": "wheels",
        "subcategory": "wheels",
        "description": "TE37 forged wheels lightweight",
        "performance_gain": {"weight": "-3kg per wheel"},
        "price_range_idr": {"min": 20000000, "max": 32000000},
        "installation_time_hours": 1,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "5x114.3. Set of 4"
    },
    {
        "part_name": "Wheels 16x7 ET42 Budget",
        "brand": "Enkei",
        "category": "wheels",
        "subcategory": "wheels",
        "description": "RPF1 lightweight wheels",
        "performance_gain": {"weight": "-2kg per wheel"},
        "price_range_idr": {"min": 8000000, "max": 12000000},
        "installation_time_hours": 1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "5x114.3. Set of 4. Great value"
    },
    {
        "part_name": "Tires Performance",
        "brand": "Michelin",
        "category": "wheels",
        "subcategory": "tires",
        "description": "Pilot Sport 4 195/55R16",
        "performance_gain": {"handling": "Superior grip"},
        "price_range_idr": {"min": 4000000, "max": 6000000},
        "installation_time_hours": 1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Set of 4. Best street tire"
    },
    {
        "part_name": "Tires Semi-Slick",
        "brand": "Toyo",
        "category": "wheels",
        "subcategory": "tires",
        "description": "Proxes R888R 195/55R16",
        "performance_gain": {"handling": "Track grip"},
        "price_range_idr": {"min": 5000000, "max": 8000000},
        "installation_time_hours": 1,
        "min_stage": 3,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Set of 4. 200 treadwear. Loud on street"
    },
    # === INTERIOR ===
    {
        "part_name": "Racing Seat",
        "brand": "Bride",
        "category": "interior",
        "subcategory": "seats",
        "description": "Bride Zeta III fixed bucket seat",
        "performance_gain": {"weight": "-5kg vs stock"},
        "price_range_idr": {"min": 8000000, "max": 15000000},
        "installation_time_hours": 2,
        "min_stage": 3,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Perlu seat rail adapter"
    },
    {
        "part_name": "Quick Release Hub",
        "brand": "NRG",
        "category": "interior",
        "subcategory": "steering",
        "description": "Quick release steering wheel hub",
        "performance_gain": {"convenience": "Theft deterrent"},
        "price_range_idr": {"min": 1000000, "max": 1800000},
        "installation_time_hours": 1,
        "min_stage": 2,
        "legal_status": "Gray Area",
        "compatibility": ["GB3", "GB4"],
        "notes": "Airbag akan nonaktif"
    },
    {
        "part_name": "Steering Wheel Racing",
        "brand": "Sparco",
        "category": "interior",
        "subcategory": "steering",
        "description": "350mm suede deep dish steering wheel",
        "performance_gain": {"handling": "Better grip"},
        "price_range_idr": {"min": 2500000, "max": 4500000},
        "installation_time_hours": 0.5,
        "min_stage": 2,
        "legal_status": "Gray Area",
        "compatibility": ["GB3", "GB4"],
        "notes": "Perlu boss kit dan quick release"
    },
    {
        "part_name": "Shift Knob",
        "brand": "Mugen",
        "category": "interior",
        "subcategory": "shift",
        "description": "Aluminum shift knob untuk manual",
        "performance_gain": {"feel": "Better shift feel"},
        "price_range_idr": {"min": 800000, "max": 1500000},
        "installation_time_hours": 0.1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3 MT", "GB4 MT"],
        "notes": "Hanya untuk transmisi manual"
    },
    {
        "part_name": "Roll Cage 4-Point",
        "brand": "Cusco",
        "category": "interior",
        "subcategory": "safety",
        "description": "4-point bolt-in roll cage steel",
        "performance_gain": {"safety": "Rollover protection"},
        "price_range_idr": {"min": 8000000, "max": 15000000},
        "installation_time_hours": 6,
        "min_stage": 3,
        "legal_status": "Track Only",
        "compatibility": ["GB3", "GB4"],
        "notes": "Wajib untuk track day"
    },
    # === EXTERIOR ===
    {
        "part_name": "Front Lip",
        "brand": "Mugen",
        "category": "exterior",
        "subcategory": "aero",
        "description": "Mugen style front lip spoiler",
        "performance_gain": {"aero": "Slight downforce"},
        "price_range_idr": {"min": 1500000, "max": 3000000},
        "installation_time_hours": 1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "FRP material. Perlu cat"
    },
    {
        "part_name": "Side Skirts",
        "brand": "Custom",
        "category": "exterior",
        "subcategory": "aero",
        "description": "Side skirt extensions",
        "performance_gain": {"aero": "Improved airflow"},
        "price_range_idr": {"min": 1500000, "max": 2500000},
        "installation_time_hours": 1,
        "min_stage": 1,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "FRP material. Perlu cat"
    },
    {
        "part_name": "Rear Diffuser",
        "brand": "Custom",
        "category": "exterior",
        "subcategory": "aero",
        "description": "Rear diffuser dengan fins",
        "performance_gain": {"aero": "Rear downforce"},
        "price_range_idr": {"min": 2000000, "max": 4000000},
        "installation_time_hours": 2,
        "min_stage": 2,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Works best with lowered ride height"
    },
    {
        "part_name": "GT Wing",
        "brand": "Voltex",
        "category": "exterior",
        "subcategory": "aero",
        "description": "1500mm GT wing carbon fiber",
        "performance_gain": {"aero": "High downforce"},
        "price_range_idr": {"min": 12000000, "max": 25000000},
        "installation_time_hours": 4,
        "min_stage": 3,
        "legal_status": "Track Only",
        "compatibility": ["GB3", "GB4"],
        "notes": "Perlu trunk reinforcement"
    },
    {
        "part_name": "Carbon Hood",
        "brand": "Seibon",
        "category": "exterior",
        "subcategory": "body",
        "description": "Carbon fiber hood dengan vents",
        "performance_gain": {"weight": "-10kg"},
        "price_range_idr": {"min": 8000000, "max": 15000000},
        "installation_time_hours": 2,
        "min_stage": 3,
        "legal_status": "Street Legal",
        "compatibility": ["GB3", "GB4"],
        "notes": "Vent membantu heat extraction"
    },
]


def seed_service_manuals():
    """Seed service manual data with embeddings"""
    print("\n[SERVICE MANUALS] Seeding service manuals...")

    for manual in SERVICE_MANUALS:
        # Generate embedding for the content
        text_for_embedding = f"{manual['section']} {manual['subsection']} {manual['content']}"
        embedding = embedder.encode(text_for_embedding).tolist()

        data = {
            "section": manual["section"],
            "subsection": manual["subsection"],
            "content": manual["content"],
            "tags": manual["tags"],
            "embedding": embedding
        }

        try:
            supabase.table("freed_service_manuals").insert(data).execute()
            print(f"  ✓ {manual['section'][:50]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"  Total: {len(SERVICE_MANUALS)} service manual entries")


def seed_common_issues():
    """Seed common issues data with embeddings"""
    print("\n[COMMON ISSUES] Seeding common issues...")

    for issue in COMMON_ISSUES:
        # Generate embedding for symptom + detail
        text_for_embedding = f"{issue['symptom']} {issue['symptom_detail']}"
        embedding = embedder.encode(text_for_embedding).tolist()

        data = {
            "symptom": issue["symptom"],
            "symptom_detail": issue["symptom_detail"],
            "probable_cause": issue["probable_cause"],
            "diagnostic_steps": issue["diagnostic_steps"],
            "part_codes": issue["part_codes"],
            "cost_estimate_idr": issue["cost_estimate_idr"],
            "urgency": issue["urgency"],
            "embedding": embedding
        }

        try:
            supabase.table("freed_common_issues").insert(data).execute()
            print(f"  ✓ {issue['symptom'][:50]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"  Total: {len(COMMON_ISSUES)} common issues")


def seed_modification_catalog():
    """Seed modification parts catalog"""
    print("\n[MODIFICATION CATALOG] Seeding modification catalog...")

    for part in MODIFICATION_PARTS:
        try:
            supabase.table("modification_catalog").insert(part).execute()
            print(f"  ✓ {part['part_name']} ({part['brand']})")
        except Exception as e:
            print(f"  ✗ Error {part['part_name']}: {e}")

    print(f"  Total: {len(MODIFICATION_PARTS)} parts")


def clear_tables():
    """Clear all data tables before seeding"""
    print("[CLEAR] Clearing existing data...")

    tables = [
        "freed_service_manuals",
        "freed_common_issues",
        "modification_catalog"
    ]

    for table in tables:
        try:
            supabase.table(table).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"  ✓ Cleared {table}")
        except Exception as e:
            print(f"  ✗ Error clearing {table}: {e}")


def main():
    import sys
    import io
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 50)
    print("HONDA FREED SUPERCHATBOT - DATABASE SEEDING")
    print("=" * 50)

    # Auto-seed without prompt for automation
    import os
    if os.environ.get('AUTO_SEED') == '1':
        clear_tables()
    else:
        # Ask user if they want to clear existing data
        try:
            clear = input("\nClear existing data first? (y/n): ").lower().strip()
            if clear == 'y':
                clear_tables()
        except EOFError:
            print("\nNo input provided, skipping clear...")

    # Seed all data
    seed_service_manuals()
    seed_common_issues()
    seed_modification_catalog()

    print("\n" + "=" * 50)
    print("SEEDING COMPLETE!")
    print("=" * 50)
    print(f"""
Summary:
- Service Manuals: {len(SERVICE_MANUALS)} entries
- Common Issues: {len(COMMON_ISSUES)} entries
- Modification Parts: {len(MODIFICATION_PARTS)} parts

Next steps:
1. Run the schema.sql in Supabase SQL Editor (if not done)
2. Start the server: uvicorn main:app --reload
3. Test with: curl http://localhost:8000/health
""")


if __name__ == "__main__":
    main()
