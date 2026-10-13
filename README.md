# Mine Inundation Intelligence System ⛏️🌊
### RAG Chatbot + Forensic Analytics Dashboard for Historical Mine Inundations

A production-grade AI-powered safety intelligence system built on historical mine accident enquiry reports published by the **Directorate General of Mines Safety (DGMS)**, Ministry of Labour & Employment, Government of India:
1. `sanket_coal_2016_2022.pdf` (316 pages)
2. `sanket_non_coal_2016_2022.pdf` (355 pages)

---

## 🎯 Key Capabilities

1. **Precision Inundation Extraction**:
   - Automated extraction pipeline screening 671 total PDF pages (622 detailed fatal accident reports and historical registers).
   - Distinguishes **actual mine inundations / inrushes** from general drowning, vehicle rollback, or dewatering accidents.
   - Extracts 25+ structured fields per incident according to statutory schemas (Pydantic validated).

2. **Grounded RAG Chatbot with Document Citations**:
   - Persistent vector index using **ChromaDB** and all-MiniLM-L6-v2 embeddings via ONNX Runtime.
   - Hybrid retrieval combining dense vector similarity with lexical keyword boost.
   - Verifiable page-level citations (`[sanket_coal_2016_2022.pdf, PDF p. 119 / Printed p. 105]`).
   - Clear architectural separation between **Factual Findings**, **Statutory Regulations**, and **AI-Generated Preventive Suggestions**.

3. **Interactive Analytics Dashboard**:
   - Visualizations built in Streamlit and Plotly Dark theme.
   - Chronological disaster trendlines, mineral sector distribution, ingress mechanism taxonomy, and mine workings breakdown.
   - Numerical metrics calculated strictly from the verified SQLite database (`data/extracted/mine_inundation.db`).

4. **Forensic Cause & Contributing-Factor Analysis**:
   - Deep-dive into physical mechanisms (barrier piercing, parting shear failure, river breach, stowing puncture, displacement waves).
   - Direct cause vs. established root cause analysis.
   - Detailed review of geological and hydrological conditions (hydrostatic head, silty shale, monsoon floods).

5. **Preventive Controls & Hazard-to-Control Matrix**:
   - Maps 7 major historical inundation failure modes to statutory DGMS controls and AI engineering recommendations.
   - Early warning and monitoring technology guidelines (IoT hydrostatic telemetry, borehole radar, LiDAR).

6. **Data Quality & Incident Review Audit**:
   - Automated validation of page references, dates, and non-negative casualty counts.
   - Cross-linking and deduplication between Chapter 10 (Major Accidents) and Chapter 11 (Courts of Inquiry).
   - Interactive review panel for reviewing unverified or ambiguous water-related incidents.

---

## 🚀 Quickstart & Setup

### Prerequisites
- Python 3.10+ (tested and verified on Python 3.14 on Windows)
- Git (optional)

### 1. Installation
Clone or navigate to the repository directory:
```bash
cd c:\Users\saipr\Desktop\mine_induntation
pip install -r requirements.txt
```

### 2. Verify Extracted Database & Vector Index
The repository includes pre-built extracted datasets and vector indices. To regenerate them from scratch:
```bash
# 1. Run the extraction and database pipeline
python src/extraction/build_database.py

# 2. Run the data quality audit
python src/extraction/data_quality.py

# 3. Populate or refresh the ChromaDB vector index
python src/rag/rag_engine.py
```

### 3. Launch the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Automated Testing
Execute the complete test suite using `pytest`:
```bash
pytest tests/test_system.py -v
```
All 11 unit and integration tests verify:
- PDF text extractability and page counts (316 and 355)
- Metadata extraction and page offset accuracy
- Pydantic schema validation
- Inundation classification rules
- Deduplication and Court of Inquiry linking
- Database calculations and aggregations
- ChromaDB vector retrieval relevance
- Citation grounding
- Edge-case and empty query handling
- Data quality validation checks

---

## 📊 Summary of Extracted Data

| Category | Extracted Count | Fatalities |
| :--- | :---: | :---: |
| **Verified Primary Inundations** | **45** | **933** |
| *— Historical Major Accidents (1901–2015)* | 36 | 923 |
| *— Detailed Modern Investigations (2016–2022)* | 8 | 10 |
| *— Standalone Court of Inquiry Cases* | 1 | 0 |
| **Duplicate References (Court of Inquiry Linked)** | 15 | *(603 deduplicated)* |
| **Related Water / Sump Drowning Incidents** | 21 | 24 |
| **Total Screened Records** | **81** | **957** |

---

## 🤖 Sample Evaluation Queries for RAG Chatbot

Test the chatbot with these representative domain questions:
1. *What are the most frequently reported causes of mine inundation?*
2. *Which incidents involved water entering from old workings?*
3. *What geological or hydrological conditions contributed to these accidents?*
4. *What warning signs were identified in the reports?*
5. *Which preventive recommendations recur across incidents?*
6. *Compare the causes and consequences of incidents in the two PDFs.*
7. *What happened at Khoodia colliery regarding parting failure?*
8. *Explain the sludge inrush accident at Turamdih uranium mine.*
9. *What safety lessons can be learned from the Chasnalla disaster?*

---

## ⚖️ Legal & Engineering Disclaimer
This intelligence system is based on historical accident reports published by the Directorate General of Mines Safety (DGMS). It is designed for forensic research, training, and risk visualization, and is not a substitute for site-specific engineering assessments, statutory permissions, or qualified mine safety personnel.
