-- Honda Freed Superchatbot Database Schema
-- Run this in Supabase SQL Editor

-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- SERVICE MANUALS TABLE (Vector Search)
-- ============================================
DROP TABLE IF EXISTS freed_service_manuals CASCADE;
CREATE TABLE freed_service_manuals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section TEXT NOT NULL,
    subsection TEXT,
    content TEXT NOT NULL,
    tags TEXT[],
    embedding vector(384),  -- all-MiniLM-L6-v2 dimension
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON freed_service_manuals USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================
-- COMMON ISSUES TABLE (Vector Search)
-- ============================================
DROP TABLE IF EXISTS freed_common_issues CASCADE;
CREATE TABLE freed_common_issues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symptom TEXT NOT NULL,
    symptom_detail TEXT,
    probable_cause TEXT[],
    diagnostic_steps TEXT[],
    part_codes TEXT[],
    cost_estimate_idr JSONB,
    urgency TEXT DEFAULT 'medium',  -- low, medium, high, critical
    embedding vector(384),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON freed_common_issues USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================
-- MODIFICATION CATALOG TABLE
-- ============================================
DROP TABLE IF EXISTS modification_catalog CASCADE;
CREATE TABLE modification_catalog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    part_name TEXT NOT NULL,
    brand TEXT NOT NULL,
    category TEXT NOT NULL,  -- engine, suspension, brakes, exterior, interior, audio
    subcategory TEXT,
    description TEXT,
    performance_gain JSONB,  -- {"hp": "+5-8", "torque": "+10 Nm", "weight": "-2kg"}
    price_range_idr JSONB NOT NULL,  -- {"min": 1500000, "max": 2500000}
    installation_time_hours NUMERIC,
    min_stage INTEGER DEFAULT 1,  -- minimum stage this part is recommended for
    legal_status TEXT DEFAULT 'Street Legal',  -- Street Legal, Track Only, Gray Area
    compatibility TEXT[],  -- ["GB3", "GB4", "L15A"]
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON modification_catalog (category);
CREATE INDEX ON modification_catalog (min_stage);

-- ============================================
-- STAGE PRESETS TABLE
-- ============================================
DROP TABLE IF EXISTS stage_presets CASCADE;
CREATE TABLE stage_presets (
    stage INTEGER PRIMARY KEY,
    stage_name TEXT NOT NULL,
    description TEXT,
    target_hp_range JSONB,  -- {"min": 130, "max": 140}
    estimated_hp_total INTEGER,
    estimated_cost_idr JSONB NOT NULL,
    required_supporting_mods TEXT[],
    warnings TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- WORKSHOPS TABLE
-- ============================================
DROP TABLE IF EXISTS workshops CASCADE;
CREATE TABLE workshops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    specialization TEXT[],  -- ["Honda", "CVT", "Tuning", "General"]
    rating NUMERIC,
    price_tier TEXT,  -- budget, mid, premium
    google_maps_url TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON workshops (city);

-- ============================================
-- VECTOR SEARCH FUNCTIONS
-- ============================================

-- Function to search service manuals by semantic similarity
CREATE OR REPLACE FUNCTION match_service_manuals(
    query_embedding vector(384),
    match_threshold float DEFAULT 0.5,
    match_count int DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    section TEXT,
    subsection TEXT,
    content TEXT,
    tags TEXT[],
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        fsm.id,
        fsm.section,
        fsm.subsection,
        fsm.content,
        fsm.tags,
        1 - (fsm.embedding <=> query_embedding) AS similarity
    FROM freed_service_manuals fsm
    WHERE 1 - (fsm.embedding <=> query_embedding) > match_threshold
    ORDER BY fsm.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Function to search common issues by semantic similarity
CREATE OR REPLACE FUNCTION match_common_issues(
    query_embedding vector(384),
    match_threshold float DEFAULT 0.5,
    match_count int DEFAULT 3
)
RETURNS TABLE (
    id UUID,
    symptom TEXT,
    symptom_detail TEXT,
    probable_cause TEXT[],
    diagnostic_steps TEXT[],
    part_codes TEXT[],
    cost_estimate_idr JSONB,
    urgency TEXT,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        fci.id,
        fci.symptom,
        fci.symptom_detail,
        fci.probable_cause,
        fci.diagnostic_steps,
        fci.part_codes,
        fci.cost_estimate_idr,
        fci.urgency,
        1 - (fci.embedding <=> query_embedding) AS similarity
    FROM freed_common_issues fci
    WHERE 1 - (fci.embedding <=> query_embedding) > match_threshold
    ORDER BY fci.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ============================================
-- INITIAL STAGE PRESETS DATA
-- ============================================
INSERT INTO stage_presets (stage, stage_name, description, target_hp_range, estimated_hp_total, estimated_cost_idr, required_supporting_mods, warnings) VALUES
(1, 'Street Sleeper', 'Basic bolt-on modifications for daily driving with improved performance',
   '{"min": 130, "max": 140}', 135, '{"min": 8000000, "max": 15000000}',
   ARRAY['Stock CVT can handle this power level'],
   ARRAY['Void factory warranty on modified parts']),
(2, 'Weekend Warrior', 'Intermediate modifications for spirited driving and occasional track days',
   '{"min": 150, "max": 165}', 155, '{"min": 25000000, "max": 45000000}',
   ARRAY['CVT cooler recommended', 'Brake upgrade required', 'Suspension upgrade recommended'],
   ARRAY['CVT at limit - consider cooler', 'Void factory warranty']),
(3, 'Track Monster', 'Full build for maximum performance, primarily track use',
   '{"min": 175, "max": 200}', 180, '{"min": 60000000, "max": 120000000}',
   ARRAY['Built CVT or manual swap required', 'Forged internals required', 'Full brake system upgrade', 'Roll cage recommended'],
   ARRAY['Not street legal in some configurations', 'Requires professional tuning', 'Full warranty void'])
ON CONFLICT (stage) DO UPDATE SET
    stage_name = EXCLUDED.stage_name,
    description = EXCLUDED.description,
    target_hp_range = EXCLUDED.target_hp_range,
    estimated_hp_total = EXCLUDED.estimated_hp_total,
    estimated_cost_idr = EXCLUDED.estimated_cost_idr,
    required_supporting_mods = EXCLUDED.required_supporting_mods,
    warnings = EXCLUDED.warnings;
