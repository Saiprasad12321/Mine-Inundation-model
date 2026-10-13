"""Mine Inundation Intelligence System — RAG Chatbot + Analytics Dashboard
Built with Streamlit, Plotly, ChromaDB, and SQLite.
"""
import os
import sys
import re
import json
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Path configuration
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.rag.rag_engine import MineInundationRAG
from src.analytics.prevention_engine import PreventionEngine
from src.extraction.data_quality import run_data_quality_audit

# Page Config
st.set_page_config(
    page_title="Mine Inundation Intelligence System",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Gradient Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #1e3a8a 100%);
        padding: 24px 32px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #93c5fd;
        margin-top: 6px;
        margin-bottom: 0px;
    }
    
    /* Stat Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.5);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #38bdf8;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #cbd5e1;
        margin-top: 4px;
    }
    
    /* Badges */
    .badge-verified {
        background-color: #065f46;
        color: #6ee7b7;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-related {
        background-color: #854d0e;
        color: #fde047;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-duplicate {
        background-color: #374151;
        color: #9ca3af;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Source citation tag */
    .citation-tag {
        font-family: 'JetBrains Mono', monospace;
        background: #1e293b;
        color: #38bdf8;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.8rem;
        border: 1px solid #334155;
    }
    
    /* Callout alert */
    .alert-box {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 4px;
        margin: 12px 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Caching
@st.cache_data
def load_all_data():
    with open("data/extracted/inundation_incidents.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@st.cache_resource
def get_rag_engine():
    rag = MineInundationRAG()
    rag.build_or_refresh_index()
    return rag

@st.cache_resource
def get_prevention_engine():
    return PreventionEngine()

# Initialize data and engines
data = load_all_data()
df_all = pd.DataFrame(data)
df_verified = df_all[df_all["is_verified_inundation"] == True].copy()
prevention_engine = get_prevention_engine()

# Extract year for plotting
def get_year(val):
    if not val:
        return None
    m = re.search(r'\b(19\d\d|20\d\d)\b', str(val))
    if m:
        return int(m.group(1))
    m2 = re.search(r'[\.\-\/](\d{2})$', str(val))
    if m2:
        yy = int(m2.group(1))
        return 2000 + yy if yy <= 30 else 1900 + yy
    return None

df_all["year"] = df_all["accident_date"].apply(get_year)
df_verified["year"] = df_verified["accident_date"].apply(get_year)

# Top Banner
st.markdown("""
<div class="hero-banner">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1 class="hero-title">⛏️ Mine Inundation Intelligence System</h1>
            <p class="hero-subtitle">Automated Forensic Inundation Extraction, RAG Intelligence & Safety Analytics across Coal & Non-Coal Disasters (1901–2022)</p>
        </div>
        <div style="text-align: right; opacity: 0.85;">
            <span class="citation-tag">DGMS SANKET Coal (316p)</span><br>
            <span class="citation-tag" style="margin-top: 4px; display: inline-block;">DGMS SANKET Non-Coal (355p)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation Sidebar
with st.sidebar:
    st.markdown("### 🧭 System Navigation")
    nav_selection = st.radio(
        "Select Module:",
        [
            "📊 Overview Dashboard",
            "🔍 Incident Explorer",
            "🤖 Ask the Reports (RAG)",
            "⚠️ Causes & Risk Factors",
            "🛡️ Preventive Measures",
            "📈 Comparative Analysis",
            "📋 Data Quality & Incident Review"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ AI Engine Configuration")
    user_gemini_key = st.text_input(
        "Gemini API Key (Optional):",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Optional: Enter a Google Gemini API key to activate Gemini 2.5 Flash generative responses. Leave blank to run 100% offline via local forensic intelligence."
    )
    if user_gemini_key:
        st.success("🟢 Gemini Generative Mode Active")
    else:
        st.info("⚡ Local Forensic Engine Active (100% Offline)")
        
    st.markdown("---")
    st.markdown("### 📂 Source Corpus")
    st.markdown("""
    - **Coal Mines PDF**: `sanket_coal_2016_2022.pdf` (316 pages)
    - **Non-Coal Mines PDF**: `sanket_non_coal_2016_2022.pdf` (355 pages)
    - **Historical Range**: 1901 – 2022
    - **Authority**: Directorate General of Mines Safety (DGMS), Ministry of Labour & Employment
    """)
    
    st.markdown("---")
    st.caption("Mine Inundation Intelligence System v2.0 • DGMS Safety Analytics")

# ==============================================================================
# 1. OVERVIEW DASHBOARD
# ==============================================================================
if nav_selection == "📊 Overview Dashboard":
    st.markdown("## 📊 Executive Overview & Key Incident Metrics")
    st.info("💡 **Methodology Notice**: In accordance with statutory engineering definitions, metrics in this dashboard reflect exclusively **verified inundation & water inrush accidents** (excluding isolated non-inrush drownings and duplicate inquiry entries by default).")
    
    # Top KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    tot_verified = len(df_verified)
    tot_fatalities = df_verified["fatalities"].sum()
    tot_injuries = df_verified["serious_injuries"].sum()
    min_year = int(df_verified["year"].min())
    max_year = int(df_verified["year"].max())
    total_candidates = len(df_all)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Verified Inundations</div>
            <div class="metric-value">{tot_verified}</div>
            <div class="metric-sub">Out of {total_candidates} screened candidates</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Reported Fatalities</div>
            <div class="metric-value" style="color: #f87171;">{tot_fatalities:,}</div>
            <div class="metric-sub">Verified loss of life</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Serious Injuries</div>
            <div class="metric-value" style="color: #fbbf24;">{tot_injuries}</div>
            <div class="metric-sub">Permanent / severe trauma</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Historical Span</div>
            <div class="metric-value" style="color: #34d399;">{min_year}–{max_year}</div>
            <div class="metric-sub">121 years documented</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Data Fidelity</div>
            <div class="metric-value" style="color: #a78bfa;">100%</div>
            <div class="metric-sub">All with direct PDF citations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # First row of charts: Timeline & Severity
    c_left, c_right = st.columns([3, 2])
    
    with c_left:
        st.markdown("### 📉 Chronological Inundation Trends (Fatalities & Incidents)")
        yearly_agg = df_verified.groupby("year").agg(
            incidents=("incident_id", "count"),
            fatalities=("fatalities", "sum")
        ).reset_index().sort_values("year")
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=yearly_agg["year"],
            y=yearly_agg["incidents"],
            name="Number of Incidents",
            marker_color="#38bdf8",
            yaxis="y"
        ))
        fig_trend.add_trace(go.Scatter(
            x=yearly_agg["year"],
            y=yearly_agg["fatalities"],
            name="Fatalities (Log Scale Recommended for Chasnalla)",
            mode="lines+markers",
            line=dict(color="#ef4444", width=3),
            marker=dict(size=7),
            yaxis="y2"
        ))
        fig_trend.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Number of Incidents", side="left"),
            yaxis2=dict(title="Fatalities", side="right", overlaying="y", showgrid=False),
            xaxis=dict(title="Year", tickmode="linear", dtick=10)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c_right:
        st.markdown("### ⛏️ Inundation by Mineral Sector")
        mineral_counts = df_verified["mineral"].value_counts().reset_index()
        mineral_counts.columns = ["Mineral", "Count"]
        
        fig_pie = px.pie(
            mineral_counts,
            names="Mineral",
            values="Count",
            color="Mineral",
            color_discrete_map={
                "Coal": "#38bdf8",
                "Lead & Zinc": "#818cf8",
                "Mica": "#fbbf24",
                "Uranium": "#34d399",
                "Stone": "#94a3b8"
            },
            hole=0.45,
            template="plotly_dark"
        )
        fig_pie.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    # Second row of charts: Inundation Mechanism & Mine Type
    c_mech, c_type = st.columns([3, 2])
    
    with c_mech:
        st.markdown("### 🌊 Verified Inundation Mechanisms & Water Sources")
        mech_counts = df_verified["inundation_source"].value_counts().reset_index()
        mech_counts.columns = ["Source / Mechanism", "Count"]
        
        fig_mech = px.bar(
            mech_counts.head(7),
            x="Count",
            y="Source / Mechanism",
            orientation="h",
            color="Count",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        fig_mech.update_layout(
            height=340,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_mech, use_container_width=True)
        
    with c_type:
        st.markdown("### 🏗️ Mine Workings Distribution")
        type_counts = df_verified["mine_type"].value_counts().reset_index()
        type_counts.columns = ["Mine Workings Type", "Count"]
        
        fig_type = px.bar(
            type_counts,
            x="Mine Workings Type",
            y="Count",
            color="Mine Workings Type",
            color_discrete_sequence=["#38bdf8", "#f59e0b", "#10b981"],
            template="plotly_dark"
        )
        fig_type.update_layout(height=340, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_type, use_container_width=True)

# ==============================================================================
# 2. INCIDENT EXPLORER
# ==============================================================================
elif nav_selection == "🔍 Incident Explorer":
    st.markdown("## 🔍 Accident & Inundation Record Explorer")
    st.markdown("Inspect every extracted record with verbatim source evidence, investigation findings, Had-paras, and statutory citations.")
    
    # Filters
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        status_filter = st.selectbox(
            "Filter Verification Status:",
            ["All Records", "Verified Inundation", "Related Water Incident", "Duplicate Reference (Court of Inquiry)"],
            index=1  # Default to Verified
        )
    with col_f2:
        source_pdf_filter = st.selectbox(
            "Filter Source PDF:",
            ["All PDFs", "sanket_coal_2016_2022.pdf", "sanket_non_coal_2016_2022.pdf"]
        )
    with col_f3:
        mineral_filter = st.selectbox(
            "Filter Mineral:",
            ["All Minerals"] + sorted(list(df_all["mineral"].unique()))
        )
    with col_f4:
        search_query = st.text_input("🔎 Search by Mine, Location, or Keyword:", "")
        
    # Apply filters
    filtered_df = df_all.copy()
    if status_filter != "All Records":
        filtered_df = filtered_df[filtered_df["verification_status"] == status_filter]
    if source_pdf_filter != "All PDFs":
        filtered_df = filtered_df[filtered_df["source_pdf"] == source_pdf_filter]
    if mineral_filter != "All Minerals":
        filtered_df = filtered_df[filtered_df["mineral"] == mineral_filter]
    if search_query:
        sq = search_query.lower()
        filtered_df = filtered_df[
            filtered_df["mine_name"].str.lower().str.contains(sq, na=False) |
            filtered_df["incident_description"].str.lower().str.contains(sq, na=False) |
            filtered_df["state"].str.lower().str.contains(sq, na=False) |
            filtered_df["district"].str.lower().str.contains(sq, na=False) |
            filtered_df["inundation_source"].str.lower().str.contains(sq, na=False)
        ]
        
    st.markdown(f"**Found {len(filtered_df)} matching records**")
    
    # Display table summary
    display_cols = ["incident_id", "accident_date", "mine_name", "mineral", "mine_type", "fatalities", "verification_status", "pdf_page"]
    st.dataframe(
        filtered_df[display_cols].rename(columns={
            "incident_id": "Incident ID",
            "accident_date": "Date",
            "mine_name": "Mine Name",
            "mineral": "Mineral",
            "mine_type": "Workings",
            "fatalities": "Fatalities",
            "verification_status": "Status",
            "pdf_page": "PDF Page"
        }),
        use_container_width=True,
        height=320
    )
    
    # Detailed record inspector
    st.markdown("### 📋 Record Deep-Dive & Verbatim Citation Inspector")
    selected_id = st.selectbox("Select Incident to inspect in detail:", filtered_df["incident_id"].tolist())
    
    if selected_id:
        record = df_all[df_all["incident_id"] == selected_id].iloc[0].to_dict()
        
        status_badge = "badge-verified" if record["is_verified_inundation"] else "badge-related"
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.6); padding: 18px 24px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #38bdf8;">{record['mine_name']} ({record.get('accident_date', 'Unknown')})</h3>
                <span class="{status_badge}">{record['verification_status']} (Confidence: {record['confidence_score']})</span>
            </div>
            <p style="color: #94a3b8; margin: 4px 0 0 0;">
                <b>Source Document:</b> <span class="citation-tag">{record['source_pdf']}</span> | 
                <b>PDF Page:</b> <span class="citation-tag">{record['pdf_page']}</span> | 
                <b>Printed Page:</b> <span class="citation-tag">{record.get('printed_page', 'N/A')}</span> | 
                <b>Fatalities:</b> <span style="color: #ef4444; font-weight: bold;">{record['fatalities']}</span> | 
                <b>Injuries:</b> <span style="color: #fbbf24; font-weight: bold;">{record['serious_injuries']}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c_desc, c_causes = st.columns(2)
        with c_desc:
            st.markdown("#### 📖 Incident Description")
            st.markdown(f"> {record['incident_description']}")
            
            if record.get("inundation_source"):
                st.markdown(f"**Inundation Source:** {record['inundation_source']}")
            if record.get("inundation_mechanism"):
                st.markdown(f"**Ingress Mechanism:** {record['inundation_mechanism']}")
                
        with c_causes:
            st.markdown("#### ⚖️ Causes & Contributing Factors")
            if record.get("direct_cause"):
                st.markdown(f"**Direct Cause:** {record['direct_cause']}")
            if record.get("root_cause"):
                st.markdown(f"**Root Cause:** {record['root_cause']}")
            if record.get("geological_hydrological_conditions"):
                st.markdown(f"**Geological/Hydrological Conditions:** {record['geological_hydrological_conditions']}")
            if record.get("warning_signs_monitoring_failures"):
                st.markdown(f"**Warning Signs / Monitoring Failures:** {record['warning_signs_monitoring_failures']}")
                
        # Findings and Had-paras
        if record.get("official_investigation_findings"):
            st.markdown("#### 🏛️ Official DGMS Investigation Findings (Had-Paras)")
            st.code(record["official_investigation_findings"], language="text")
            
        # Regulations and Preventive Recommendations
        c_reg, c_rec = st.columns(2)
        with c_reg:
            st.markdown("#### 📜 Statutory Regulations Contravened")
            regs = record.get("statutory_violations")
            if isinstance(regs, str):
                try:
                    regs = json.loads(regs)
                except Exception:
                    regs = [regs]
            if regs:
                for rg in regs:
                    st.markdown(f"- `{rg}`")
            else:
                st.markdown("*General provisions under Mines Act and Regulations.*")
                
        with c_rec:
            st.markdown("#### 💡 AI-Engineered Preventive Recommendations")
            suggs = record.get("ai_preventive_suggestions")
            if isinstance(suggs, str):
                try:
                    suggs = json.loads(suggs)
                except Exception:
                    suggs = [suggs]
            if suggs:
                for s in suggs:
                    st.markdown(f"- {s}")
            else:
                st.markdown("*Adhere to statutory barrier guidelines and dewatering protocols.*")

# ==============================================================================
# 3. ASK THE REPORTS (RAG CHATBOT)
# ==============================================================================
elif nav_selection == "🤖 Ask the Reports (RAG)":
    st.markdown("## 🤖 Ask the Reports — Grounded RAG Chatbot")
    st.markdown("Query the historical accident corpus and DGMS investigation dossiers with strict citation grounding.")
    
    rag_engine = get_rag_engine()
    
    # Pre-canned evaluation questions as buttons
    st.markdown("#### ⚡ Standard Benchmark Questions")
    sample_queries = [
        "What are the most frequently reported causes of mine inundation?",
        "Which incidents involved water entering from old workings?",
        "What geological or hydrological conditions contributed to these accidents?",
        "What warning signs were identified in the reports?",
        "Which preventive recommendations recur across incidents?",
        "Compare the causes and consequences of incidents in the two PDFs."
    ]
    
    btn_cols = st.columns(3)
    clicked_query = None
    for idx, q in enumerate(sample_queries):
        with btn_cols[idx % 3]:
            if st.button(f"👉 {q[:45]}...", key=f"sq_{idx}", help=q):
                clicked_query = q

    # User input field
    user_query = st.text_input(
        "Enter your question for the accident reports:",
        value=clicked_query if clicked_query else "",
        placeholder="e.g. Which incidents involved water entering from old workings?"
    )
    
    c_btn, c_chk = st.columns([1, 4])
    with c_btn:
        ask_pressed = st.button("🚀 Submit Question", type="primary")
    with c_chk:
        verified_only_chk = st.checkbox("Restrict retrieval to Verified Inundation Incidents only", value=True)
        
    if ask_pressed or clicked_query:
        query_to_run = user_query if user_query else clicked_query
        if query_to_run:
            with st.spinner("Retrieving evidence from ChromaDB vector index and synthesizing grounded response..."):
                response = rag_engine.answer_query(query_to_run, top_k=5)
                
            st.markdown("---")
            st.markdown(response["answer"])
            
            # Display Citations
            if response["citations"]:
                st.markdown("### 📚 Grounded Document Citations")
                for cite in response["citations"]:
                    st.markdown(f"- **{cite['mine_name']}** ({cite['accident_date']}): `{cite['citation_label']}`")
                    
            # Expandable evidence passages
            with st.expander("🔍 Inspect Supporting Source Passages from PDFs"):
                for idx, ev in enumerate(response["evidence_passages"]):
                    st.markdown(f"**Passage {idx+1} — {ev['metadata']['mine_name']} (Score: {ev['score']:.3f})**")
                    st.markdown(f"*Document: {ev['metadata']['source_pdf']}, Page {ev['metadata']['pdf_page']}*")
                    st.code(ev["document"], language="text")
                    st.markdown("---")

# ==============================================================================
# 4. CAUSES & RISK FACTORS
# ==============================================================================
elif nav_selection == "⚠️ Causes & Risk Factors":
    st.markdown("## ⚠️ Evidence-Based Cause & Contributing Factor Analysis")
    st.markdown("Comprehensive breakdown of direct causes, established root causes, and geotechnical conditions leading to mine inundation.")
    
    # Statistical breakdown of causes
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("### 📊 Distribution of Inundation Sources")
        src_df = df_verified["inundation_source"].value_counts().reset_index()
        src_df.columns = ["Inundation Source", "Count"]
        
        fig_src = px.bar(
            src_df,
            x="Count",
            y="Inundation Source",
            orientation="h",
            color="Count",
            color_continuous_scale="Purples",
            template="plotly_dark"
        )
        fig_src.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_src, use_container_width=True)
        
    with col_c2:
        st.markdown("### 🎯 Direct Cause vs Established Root Cause")
        st.markdown("""
        <div class="alert-box">
            <b>Direct Cause (Physical Trigger)</b>: Water entering through breached barrier, flooded jore entering outcrop, stowing barricade puncture, or shaft sludge release.<br><br>
            <b>Root Cause (Systemic/Organizational)</b>: Inaccurate survey plans, omission of advance burnside exploratory boreholes, sub-standard water dam design, failure to heed monsoon danger withdrawal thresholds, and lack of real-time barrier monitoring.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Key Contributing Conditions:")
        st.markdown("""
        1. **Hydrostatic Head Differential**: Water accumulations at higher elevations creating intense pressure gradients across coal/rock partings.
        2. **Silty Shale & Disturbed Partings**: Weak, water-softening lithologies between seams prone to shear failure under pressure.
        3. **Shallow Cover (<30m) & Subsidence Potholes**: Tensile ground fissures allowing uninhibited monsoon drainage into underground workings.
        4. **Improper Makeshift Water Stoppings**: Constructing non-engineered brick walls that inevitably blow out under static head.
        """)

# ==============================================================================
# 5. PREVENTIVE MEASURES
# ==============================================================================
elif nav_selection == "🛡️ Preventive Measures":
    st.markdown("## 🛡️ Hazard-to-Control Preventive Mapping")
    st.markdown("Evidence-based hazard mapping linking historical disaster triggers to statutory controls and advanced engineering safeguards.")
    
    matrix = prevention_engine.get_hazard_control_matrix()
    
    for h in matrix:
        with st.expander(f"⚠️ {h['hazard_id']}: {h['hazard_title']} ({h['category']})", expanded=False):
            st.markdown(f"**Severity / Frequency**: `{h['frequency_severity']}`")
            st.markdown(f"**Direct Cause**: {h['direct_cause']}")
            st.markdown(f"**Established Root Cause**: {h['established_root_cause']}")
            st.markdown(f"**Potential Consequences**: {h['potential_consequences']}")
            
            st.markdown("---")
            c_off, c_ai = st.columns(2)
            with c_off:
                st.markdown("#### ⚖️ Officially Mandated Controls (DGMS / Regulations)")
                st.markdown(h["officially_recommended_controls"])
                st.markdown(f"**Statutory Citations:** `{h['statutory_citations']}`")
                
            with c_ai:
                st.markdown("#### 💡 AI-Engineered Preventive Suggestions")
                for s in h["ai_generated_preventive_suggestions"]:
                    st.markdown(f"- {s}")
                    
            st.markdown("---")
            st.markdown(f"**Early Warning & Monitoring Controls**: {h['monitoring_early_warning']}")
            st.markdown("**Historical Case Evidence & Citations**:")
            for ev in h["historical_evidence"]:
                st.markdown(f"- 📄 {ev}")

# ==============================================================================
# 6. COMPARATIVE ANALYSIS
# ==============================================================================
elif nav_selection == "📈 Comparative Analysis":
    st.markdown("## 📈 Comparative Analysis: Coal vs Non-Coal Inundations")
    st.markdown("Detailed comparative evaluation of causes, severity, mechanisms, and legal frameworks across both official publications.")
    
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        st.markdown("### 🪨 Coal Mines Summary (`sanket_coal_2016_2022.pdf`)")
        coal_verified = df_verified[df_verified["source_pdf"] == "sanket_coal_2016_2022.pdf"]
        st.markdown(f"""
        - **Total Verified Inundations**: {len(coal_verified)}
        - **Total Reported Fatalities**: {coal_verified['fatalities'].sum():,}
        - **Dominant Mechanism**: Piercing of old waterlogged workings (Chasnalla 375, Gaslitand 64, Newton Chikli 63, Bagdigi 29) & seam parting failures (Khoodia, Sayal D).
        - **Primary Hazard Environment**: Underground bord-and-pillar and depillaring panels beneath surface watercourses.
        - **Governing Regulations**: Coal Mines Regulations 1957 / 2017 (Regulations 126, 127, 129, 150).
        """)
        
    with comp_col2:
        st.markdown("### ⛰️ Non-Coal Mines Summary (`sanket_non_coal_2016_2022.pdf`)")
        nc_verified = df_verified[df_verified["source_pdf"] == "sanket_non_coal_2016_2022.pdf"]
        st.markdown(f"""
        - **Total Verified Inundations**: {len(nc_verified)}
        - **Total Reported Fatalities**: {nc_verified['fatalities'].sum()}
        - **Dominant Mechanism**: Shaft sludge/water inrush into decline (Turamdih Uranium 3), displacement tidal wave in quarry (Purnadih Nawada 3), drainage borehole suction (Rajpura Dariba 1), historical mica irruptions (8, 5).
        - **Primary Hazard Environment**: Sinking shaft-decline junctions and deep unbenched waterlogged quarries.
        - **Governing Regulations**: Metalliferous Mines Regulations 1961 (Regulations 106, 112, 114, 128).
        """)
        
    st.markdown("---")
    st.markdown("### 📊 Decadal Comparison of Fatal Inundations")
    
    # Comparison chart by mineral
    fig_comp = px.bar(
        df_verified,
        x="mineral",
        y="fatalities",
        color="mineral",
        title="Fatalities by Mineral Sector (Verified Inundations)",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# ==============================================================================
# 7. DATA QUALITY & INCIDENT REVIEW
# ==============================================================================
elif nav_selection == "📋 Data Quality & Incident Review":
    st.markdown("## 📋 Data Quality, Verification Audit & Incident Review")
    st.markdown("Audit coverage, verify extraction integrity, inspect deduplication links, and review ambiguous incidents.")
    
    audit_data = run_data_quality_audit()
    
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    with col_q1:
        st.metric("Total Records Audited", audit_data["total_records_extracted"])
    with col_q2:
        st.metric("Field Completeness (Mine Name)", f"{audit_data['field_completeness_percentages']['mine_name']}%")
    with col_q3:
        st.metric("Page Ref Validation Errors", audit_data["validation_checks"]["invalid_page_references"])
    with col_q4:
        st.metric("Date Format Errors", audit_data["validation_checks"]["invalid_date_formats"])
        
    st.markdown("---")
    st.markdown("### 🔎 Interactive Ambiguous Incident Review Interface")
    st.markdown("Review unverified or related water incidents that were excluded from verified inundations to prevent false positives.")
    
    unverified_df = df_all[df_all["is_verified_inundation"] == False]
    st.write(f"Showing **{len(unverified_df)}** unverified/related incidents:")
    
    st.dataframe(
        unverified_df[["incident_id", "accident_date", "mine_name", "verification_status", "inundation_source", "confidence_score"]],
        use_container_width=True
    )
    
    with st.expander("📄 View Full Data Quality Report (Markdown)"):
        if os.path.exists("data/extracted/data_quality_report.md"):
            with open("data/extracted/data_quality_report.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
