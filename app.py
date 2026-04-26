import streamlit as st
from data_loader import load_all_data
import sections.overview     as overview
import sections.player_roi   as player_roi
import sections.team_strategy as team_strategy
import sections.uncapped_gems as uncapped_gems
import sections.bench_warmers as bench_warmers
import sections.stat_tests   as stat_tests
import sections.visual_analysis as visual_analysis

# ── page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Auction 2023 · Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── global CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── root ── */
html, body, [class*="css"] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── main container ── */
.main .block-container {
    padding: 1.5rem 2.5rem 4rem;
    max-width: 1400px;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: #010409 !important;
    border-right: 1px solid #21262d !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.9rem !important;
    padding: 6px 0 !important;
}

/* ── headings ── */
h1 { font-family: 'Bebas Neue', sans-serif !important;
     font-size: 3rem !important; color: #f5a623 !important;
     letter-spacing: .06em; margin-bottom: 0 !important; }
h2 { font-family: 'Bebas Neue', sans-serif !important;
     font-size: 1.8rem !important; color: #e6edf3 !important;
     letter-spacing: .04em; }
h3 { font-size: 1.1rem !important; color: #79c0ff !important;
     font-weight: 600 !important; }

/* ── metric cards ── */
[data-testid="stMetric"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    padding: 18px 22px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2rem !important;
    color: #f5a623 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
    color: #8b949e !important;
}
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ── dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── select / input ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #30363d !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    color: #8b949e !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #f5a623 !important;
    color: #0d1117 !important;
    font-weight: 700 !important;
}

/* ── divider ── */
hr { border: none; border-top: 1px solid #21262d !important; margin: 1.5rem 0; }

/* ── info / warning boxes ── */
.interp-box {
    background: #161b22;
    border-left: 4px solid #f5a623;
    border-radius: 6px;
    padding: 14px 18px;
    margin-top: 10px;
    font-size: 0.9rem;
    color: #e6edf3;
    line-height: 1.6;
}
.sig-box {
    background: #0f2a1a;
    border-left: 4px solid #22c55e;
    border-radius: 6px;
    padding: 14px 18px;
    margin-top: 10px;
    font-size: 0.9rem;
    color: #86efac;
}
.nosig-box {
    background: #2a0f0f;
    border-left: 4px solid #ef4444;
    border-radius: 6px;
    padding: 14px 18px;
    margin-top: 10px;
    font-size: 0.9rem;
    color: #fca5a5;
}

/* ── pill badge ── */
.badge {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: .75rem;
    color: #f5a623;
    margin: 2px;
}

/* ── upload area ── */
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 2px dashed #30363d !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* ── buttons ── */
.stButton > button {
    background: #f5a623 !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 8px 20px !important;
}
.stButton > button:hover {
    background: #e09418 !important;
}
</style>
""", unsafe_allow_html=True)


# ── sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px'>
        <div style='font-family:"Bebas Neue",sans-serif; font-size:2rem;
                    color:#f5a623; letter-spacing:.08em;'>🏏 IPL 2023</div>
        <div style='color:#8b949e; font-size:.8rem; margin-top:4px;'>
            Auction Intelligence Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    PAGES = {
        "🏠  Overview":           "Overview",
        "📈  Player ROI":         "Player ROI",
        "💰  Team Strategy":      "Team Strategy",
        "💎  Uncapped Gems":      "Uncapped Gems",
        "🔥  Bench Warmers":      "Bench Warmers",
        "🧪  Statistical Tests":  "Statistical Tests",
        "📊  Visual Analysis":    "Visual Analysis",
    }

    page = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='color:#8b949e; font-size:.75rem; line-height:1.8'>
        <b style='color:#e6edf3'>CSV files (auto-loaded):</b><br>
        📁 data/ipl_auction_2023.csv<br>
        📁 data/ipl_player_lifetime.csv<br>
        📁 data/ipl_points_table.csv<br><br>
        <b style='color:#e6edf3'>Data source:</b><br>
        Kaggle IPL Datasets
    </div>
    """, unsafe_allow_html=True)


# ── auto-load from data/ folder ────────────────────────────────────
import os, pathlib

DATA_DIR     = pathlib.Path(__file__).parent / "data"
AUCTION_PATH = DATA_DIR / "ipl_auction_2023.csv"
PLAYER_PATH  = DATA_DIR / "ipl_player_lifetime.csv"
POINTS_PATH  = DATA_DIR / "ipl_points_table.csv"

missing = [str(p) for p in [AUCTION_PATH, PLAYER_PATH, POINTS_PATH] if not p.exists()]

if missing:
    st.markdown("# IPL AUCTION 2023")
    st.markdown("### 🏏 Auction Intelligence Dashboard")
    st.markdown("---")
    st.error("❌ **Missing CSV files.** Place the following files inside the `data/` folder:")
    for m in missing:
        st.code(m)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px'>
            <div style='font-size:2rem'>📋</div>
            <div style='font-weight:600;margin:8px 0 4px'>Auction Data</div>
            <div style='color:#8b949e;font-size:.85rem'>data/ipl_auction_2023.csv</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px'>
            <div style='font-size:2rem'>🏃</div>
            <div style='font-weight:600;margin:8px 0 4px'>Player Stats</div>
            <div style='color:#8b949e;font-size:.85rem'>data/ipl_player_lifetime.csv</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px'>
            <div style='font-size:2rem'>🏆</div>
            <div style='font-weight:600;margin:8px 0 4px'>Points Table</div>
            <div style='color:#8b949e;font-size:.85rem'>data/ipl_points_table.csv</div>
        </div>""", unsafe_allow_html=True)
    st.stop()


# ── load with spinner ──────────────────────────────────────────────
with st.spinner("⚙️ Loading and processing data..."):
    df, points_table, warnings_list = load_all_data(
        str(AUCTION_PATH), str(PLAYER_PATH), str(POINTS_PATH)
    )

if warnings_list:
    for w in warnings_list:
        st.warning(w)

if df.empty:
    st.error("❌ Could not load data. Please check your CSV files.")
    st.stop()


# ── route to section ───────────────────────────────────────────────
section_name = PAGES[page]

if section_name == "Overview":
    overview.render(df, points_table)
elif section_name == "Player ROI":
    player_roi.render(df)
elif section_name == "Team Strategy":
    team_strategy.render(df)
elif section_name == "Uncapped Gems":
    uncapped_gems.render(df)
elif section_name == "Bench Warmers":
    bench_warmers.render(df)
elif section_name == "Statistical Tests":
    stat_tests.render(df)
elif section_name == "Visual Analysis":
    visual_analysis.render(df)
