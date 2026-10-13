"""Automated Test Suite for Mine Inundation Intelligence System.
Tests text extraction, metadata, classification, deduplication, schema validation,
dashboard calculations, RAG retrieval relevance, and citation grounding.
"""
import os
import sys
import json
import sqlite3
import pytest
import pymupdf
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.extraction.schema import InundationIncident
from src.extraction.data_quality import run_data_quality_audit
from src.rag.rag_engine import MineInundationRAG
from src.analytics.prevention_engine import PreventionEngine

# Paths
COAL_PDF = "data/raw/sanket_coal_2016_2022.pdf"
NON_COAL_PDF = "data/raw/sanket_non_coal_2016_2022.pdf"
DATA_JSON = "data/extracted/inundation_incidents.json"
DATA_DB = "data/extracted/mine_inundation.db"

# 1. PDF Text Extraction & Page Count Tests
def test_pdf_text_extraction():
    assert os.path.exists(COAL_PDF), "Coal PDF missing"
    assert os.path.exists(NON_COAL_PDF), "Non-Coal PDF missing"
    
    doc_c = pymupdf.open(COAL_PDF)
    doc_nc = pymupdf.open(NON_COAL_PDF)
    
    assert len(doc_c) == 316, f"Expected 316 pages in Coal PDF, got {len(doc_c)}"
    assert len(doc_nc) == 355, f"Expected 355 pages in Non-Coal PDF, got {len(doc_nc)}"
    
    # Check that text is selectable and not blank images
    text_c = doc_c[18].get_text().strip()
    assert len(text_c) > 100, "Coal PDF page 19 should have selectable text"
    assert "DECADAL ANALYSIS" in text_c
    
    text_nc = doc_nc[18].get_text().strip()
    assert len(text_nc) > 100, "Non-Coal PDF page 19 should have selectable text"
    assert "DECADAL ANALYSIS" in text_nc

# 2. Page Level Metadata & Offset
def test_page_level_metadata():
    doc_c = pymupdf.open(COAL_PDF)
    # Printed page 1 is PDF page 15 (index 14)
    p1_text = doc_c[14].get_text()
    assert "1.   INTRODUCTION" in p1_text or "INTRODUCTION" in p1_text
    
    doc_nc = pymupdf.open(NON_COAL_PDF)
    p1_nc_text = doc_nc[14].get_text()
    assert "1.   INTRODUCTION" in p1_nc_text or "INTRODUCTION" in p1_nc_text

# 3. Structured Extraction & Schema Validation
def test_structured_extraction_and_schema():
    assert os.path.exists(DATA_JSON), "Extracted JSON missing"
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    assert len(records) > 0, "No records found in extracted JSON"
    
    # Validate each record against Pydantic schema
    for r in records:
        validated = InundationIncident(**r)
        assert validated.incident_id, "Incident ID must not be empty"
        assert validated.pdf_page > 0, "PDF page must be positive"
        assert 0.0 <= validated.confidence_score <= 1.0, "Confidence score must be between 0 and 1"

# 4. Inundation Classification
def test_inundation_classification():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Sayal D must be verified inundation
    assert any("sayal" in r["mine_name"].lower() and r["is_verified_inundation"] for r in records), "Sayal D must be verified inundation"
    # Khoodia must be verified inundation
    assert any("khoodia" in r["mine_name"].lower() and r["is_verified_inundation"] for r in records), "Khoodia must be verified inundation"
    # Turamdih Uranium must be verified inundation
    assert any("turamdih" in r["mine_name"].lower() and r["is_verified_inundation"] for r in records), "Turamdih must be verified inundation"
    # Purnadih Nawada must be verified inundation
    assert any("purnadih" in r["mine_name"].lower() and r["is_verified_inundation"] for r in records), "Purnadih Nawada must be verified inundation"

# 5. Duplicate Detection & Linking
def test_duplicate_detection():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    duplicates = [r for r in records if r.get("duplicate_of") is not None]
    assert len(duplicates) >= 10, f"Expected at least 10 linked duplicate Court of Inquiry records, found {len(duplicates)}"
    
    # Check that Chasnalla Court of Inquiry is linked
    chasnalla_dups = [r for r in duplicates if "chasnalla" in r.get("duplicate_of", "").lower()]
    assert len(chasnalla_dups) >= 1, "Chasnalla Court of Inquiry should be linked to primary historical disaster"

# 6. Data Aggregation & Dashboard Calculations
def test_dashboard_calculations():
    engine = PreventionEngine(DATA_JSON)
    stats = engine.get_summary_statistics()
    
    assert stats["total_verified_incidents"] == 45, f"Expected 45 verified inundations, got {stats['total_verified_incidents']}"
    assert stats["total_verified_fatalities"] == 933, f"Expected 933 verified fatalities, got {stats['total_verified_fatalities']}"
    assert "Coal" in stats["by_mineral"]
    assert stats["by_mineral"]["Coal"] >= 30

# 7. SQLite Database Integrity
def test_sqlite_database():
    assert os.path.exists(DATA_DB), "SQLite DB missing"
    conn = sqlite3.connect(DATA_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE is_verified_inundation = 1;")
    verified_in_db = cursor.fetchone()[0]
    assert verified_in_db == 45, f"Expected 45 verified in DB, got {verified_in_db}"
    conn.close()

# 8. RAG Retrieval Relevance & Accuracy
def test_rag_retrieval_relevance():
    rag = MineInundationRAG(json_path=DATA_JSON)
    
    # Test 1: Query for Chasnalla
    res1 = rag.answer_query("Tell me about the Chasnalla inundation disaster")
    assert any("chasnalla" in c["mine_name"].lower() for c in res1["citations"]), "Citations should include Chasnalla"
    
    # Test 2: Query for Khoodia
    res2 = rag.answer_query("What happened at Khoodia colliery regarding parting failure?")
    assert any("khoodia" in c["mine_name"].lower() for c in res2["citations"]), "Citations should include Khoodia"
    
    # Test 3: Query for Turamdih
    res3 = rag.answer_query("Explain the sludge inrush accident at Turamdih uranium mine")
    assert any("turamdih" in c["mine_name"].lower() for c in res3["citations"]), "Citations should include Turamdih"

# 9. Citations & Page Grounding
def test_citations_grounding():
    rag = MineInundationRAG(json_path=DATA_JSON)
    res = rag.answer_query("What are the most frequently reported causes of mine inundation?")
    assert len(res["citations"]) > 0, "Must return citations"
    for c in res["citations"]:
        assert c["pdf_page"] > 0, "PDF page must be valid"
        assert c["pdf"].endswith(".pdf"), "PDF name must end with .pdf"

# 10. Empty & Edge Case Queries
def test_empty_or_edge_case_queries():
    rag = MineInundationRAG(json_path=DATA_JSON)
    res = rag.answer_query("    ")
    assert "Please ask a specific question" in res["answer"]
    assert len(res["citations"]) == 0

# 11. Data Quality Audit Execution
def test_data_quality_report():
    report = run_data_quality_audit(DATA_JSON)
    assert report["total_records_extracted"] == 81
    assert report["validation_checks"]["invalid_page_references"] == 0
    assert report["validation_checks"]["negative_casualty_values"] == 0
    assert report["validation_checks"]["invalid_date_formats"] == 0
    assert report["validation_checks"]["invalid_confidence_scores"] == 0
    assert report["validation_checks"]["ai_findings_separation_clean"] is True
