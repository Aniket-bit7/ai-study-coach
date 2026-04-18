import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.graph import build_graph
from services.llm_service import generate_response
from agent.config import GROQ_API_KEY
from agent.memory import add_to_memory



@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()



st.set_page_config(
    page_title="StudyAI — Your AI Study Coach",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)



defaults = {
    "page": "landing",
    "api_key": "",
    "student_data": None,
    "subject": "",
    "analysis_result": None,
    "chat_history": [],
    "history": [],
    "setup_complete": False,
    "user_name": "",
    "profile_saved": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


params = st.query_params
if params.get("user_name") and not st.session_state.profile_saved:
    st.session_state.user_name = params.get("user_name", "")
    st.session_state.profile_saved = True
    if params.get("api_key"):
        st.session_state.api_key = params.get("api_key", "")

if params.get("page") and st.session_state.page == "landing":
    st.session_state.page = params.get("page")


def get_active_key():
    return st.session_state.api_key or GROQ_API_KEY

def has_env_key():
    return bool(GROQ_API_KEY)



st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ═══ RESET + GLOBAL ═══ */
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }

    .stApp {
        background: #04060c;
        color: #e6edf3;
    }

    /* Hide default streamlit stuff */
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stMainBlockContainer, .block-container { padding-top: 0 !important; }

    /* ═══ FORCE WHITE TEXT EVERYWHERE ═══ */
    .stApp, .stApp * { color: #e6edf3; }
    .stApp p, .stApp span, .stApp div, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #e6edf3 !important;
    }
    .stApp small { color: #8b949e !important; }
    .stApp .stCaption, .stApp [data-testid="stCaptionContainer"] { color: #8b949e !important; }
    .stApp [data-testid="stFileUploaderDropzone"] { background: #0d1117 !important; border-color: #1c2333 !important; }
    .stApp [data-testid="stFileUploaderDropzone"] * { color: #8b949e !important; }
    .stApp [data-testid="stMarkdownContainer"] p { color: #e6edf3 !important; }
    .stApp .stWarning, .stApp .stInfo, .stApp .stError, .stApp .stSuccess {
        background-color: #161b22 !important;
        border-color: #30363d !important;
    }

    /* ═══ HIDE ALL BROKEN MATERIAL ICON / ARROW TEXT ═══ */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    button[kind="headerNoPadding"] { display: none !important; }
    [data-testid="stBaseButton-headerNoPadding"] { display: none !important; }

    /* Hide broken Material Icon text bleeding through */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {
        /* Let Streamlit's own CSS handle the fonts, just hide any empty ones if needed */
    }

    /* Re-show emoji icons */
    .feature-icon, .metric-icon {
        font-size: inherit !important;
        overflow: visible !important;
        width: auto !important;
        display: block !important;
    }

    /* ═══ NATIVE CHAT MESSAGE STYLING ═══ */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, #0a0e1790, #0d111790) !important;
        border: 1px solid #1c233380 !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] code {
        color: #e6edf3 !important;
    }
    [data-testid="stChatMessage"] code {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    [data-testid="stChatMessage"] a {
        color: #58a6ff !important;
    }
    /* Chat input styling */
    [data-testid="stChatInput"] {
        background: #0d1117 !important;
        border-color: #30363d !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #e6edf3 !important;
    }

    /* ═══ KEYFRAME ANIMATIONS (kept only for non-landing pages) ═══ */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes typing-dot {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }

    /* ═══ SIDEBAR ═══ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #08090f 0%, #0d1117 100%);
        border-right: 1px solid #161b2280;
    }

    /* ═══ LANDING PAGE — DARK THEME ═══ */
    .landing-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        overflow: hidden;
    }

    /* Hero */
    .hero {
        text-align: center;
        padding: 20px 20px 40px;
        position: relative;
        z-index: 1;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 20px;
        border-radius: 24px;
        background: linear-gradient(135deg, #58a6ff15, #a371f715);
        border: 1px solid #58a6ff30;
        font-size: 0.82rem;
        font-weight: 600;
        color: #58a6ff;
        margin-bottom: 28px;
    }
    .hero-title {
        font-size: 4.2rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #ffffff 0%, #58a6ff 40%, #a371f7 70%, #f778ba 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #8b949e;
        max-width: 600px;
        margin: 0 auto 40px;
        line-height: 1.7;
    }
    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 16px 40px;
        border-radius: 14px;
        background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%);
        color: #fff;
        font-weight: 700;
        font-size: 1.05rem;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(88,166,255,0.3);
        cursor: pointer;
        border: none;
    }
    .hero-cta:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 40px rgba(88,166,255,0.4);
    }

    /* Feature Cards (Dark) */
    .features {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        max-width: 1000px;
        margin: 40px auto;
        padding: 0 20px;
        position: relative;
        z-index: 1;
    }
    .feature-card {
        background: linear-gradient(135deg, #0d111780, #161b2260);
        backdrop-filter: blur(20px);
        border: 1px solid #1c233380;
        border-radius: 20px;
        padding: 32px 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: #58a6ff60;
        box-shadow: 0 20px 60px rgba(88,166,255,0.1);
    }
    .feature-icon {
        font-size: 2.5rem !important;
        margin-bottom: 16px;
        display: block;
    }
    .feature-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e6edf3;
        margin-bottom: 8px;
    }
    .feature-desc {
        font-size: 0.85rem;
        color: #8b949e;
        line-height: 1.6;
    }

    /* Tech Stack (Dark) */
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin: 40px 0 20px;
    }
    .tech-badge {
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: #161b22;
        border: 1px solid #30363d;
        color: #8b949e;
        transition: all 0.3s;
    }
    .tech-badge:hover {
        border-color: #58a6ff;
        color: #58a6ff;
        background: #58a6ff10;
    }

    /* ═══ GLASS CARDS ═══ */
    .glass-card {
        background: linear-gradient(135deg, #0d111790, #161b2260);
        backdrop-filter: blur(12px);
        border: 1px solid #1c2333;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        border-color: #58a6ff50;
        box-shadow: 0 8px 32px rgba(88,166,255,0.06);
        transform: translateY(-2px);
    }

    /* ═══ METRIC CARDS ═══ */
    .metric-card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #1c2333;
        border-radius: 16px;
        padding: 22px 16px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 48px rgba(88,166,255,0.08);
        border-color: #58a6ff40;
    }
    .metric-icon { font-size: 1.8rem !important; margin-bottom: 8px; }
    .metric-value { font-size: 1rem; font-weight: 700; margin: 4px 0; }
    .metric-label {
        font-size: 0.7rem;
        color: #484f58;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    /* ═══ BADGES ═══ */
    .badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .badge-danger  { background: #f8514918; color: #f85149; border: 1px solid #f8514933; }
    .badge-success { background: #3fb95018; color: #3fb950; border: 1px solid #3fb95033; }
    .badge-warning { background: #d2992218; color: #d29922; border: 1px solid #d2992233; }
    .badge-info    { background: #58a6ff18; color: #58a6ff; border: 1px solid #58a6ff33; }

    /* ═══ CHAT BUBBLES ═══ */
    .chat-user {
        display: block;
        background: linear-gradient(135deg, #1a2332, #1c2333);
        border: 1px solid #30363d50;
        border-radius: 20px 20px 4px 20px;
        padding: 18px 22px;
        margin: 14px 0 14px 80px;
        position: relative;
        animation: slideInRight 0.4s ease-out;
        font-size: 0.92rem;
        line-height: 1.6;
    }
    .chat-user-label {
        display: block;
        position: absolute;
        top: -10px;
        right: 14px;
        font-size: 0.68rem;
        background: #0a0e17;
        padding: 2px 10px;
        border-radius: 10px;
        border: 1px solid #30363d50;
        color: #8b949e !important;
        font-weight: 600;
        width: fit-content;
    }
    .chat-ai {
        display: block;
        background: linear-gradient(135deg, #0a0e1790, #0d111790);
        border: 1px solid #1c233380;
        border-left: 3px solid #58a6ff;
        border-radius: 4px 20px 20px 20px;
        padding: 22px 26px;
        margin: 14px 80px 14px 0;
        position: relative;
        line-height: 1.8;
        animation: slideInLeft 0.4s ease-out;
        font-size: 0.92rem;
    }
    .chat-ai-label {
        display: block;
        position: absolute;
        top: -10px;
        left: 14px;
        font-size: 0.68rem;
        background: #0a0e17;
        padding: 2px 10px;
        border-radius: 10px;
        border: 1px solid #1c233380;
        color: #58a6ff !important;
        font-weight: 600;
        width: fit-content;
    }
    .api-key-warning {
        display: block;
        background: linear-gradient(135deg, #d2992210, #f8514910);
        border: 1px solid #d2992240;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 14px 80px 14px 0;
        text-align: center;
    }
    .api-key-warning-icon { display: block; font-size: 2rem; margin-bottom: 8px; }
    .api-key-warning-text { display: block; color: #d29922 !important; font-weight: 600; font-size: 0.9rem; }
    .api-key-warning-sub { display: block; color: #8b949e !important; font-size: 0.82rem; margin-top: 6px; }

    /* ═══ WEAK TAGS ═══ */
    .weak-tag {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px 4px;
        background: #f8514912;
        color: #f85149;
        border: 1px solid #f8514925;
    }

    /* ═══ PLAN ITEMS ═══ */
    .plan-item {
        display: block;
        background: #0d1117;
        border-left: 3px solid #58a6ff;
        padding: 12px 18px;
        margin-bottom: 6px;
        border-radius: 0 12px 12px 0;
        font-size: 0.88rem;
        color: #c9d1d9 !important;
        transition: all 0.3s;
    }
    .plan-item:hover {
        background: #161b22;
        border-left-color: #a371f7;
        transform: translateX(4px);
    }

    /* ═══ RESOURCE CARDS ═══ */
    .resource-card {
        background: linear-gradient(135deg, #0d1117, #161b22);
        border: 1px solid #1c2333;
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 14px;
        transition: all 0.3s ease;
        text-decoration: none !important;
        color: inherit !important;
    }
    .resource-card:hover {
        border-color: #58a6ff50;
        box-shadow: 0 8px 28px rgba(88,166,255,0.08);
        transform: translateY(-3px);
    }
    .resource-thumb {
        width: 100px; height: 60px;
        border-radius: 10px;
        object-fit: cover;
        flex-shrink: 0;
    }
    .resource-info { flex: 1; }
    .resource-title {
        font-weight: 600;
        font-size: 0.88rem;
        color: #e6edf3;
        margin-bottom: 6px;
    }
    .resource-type {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        background: #58a6ff15;
        color: #58a6ff;
    }

    /* ═══ BUTTONS ═══ */
    .stButton > button {
        background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(88,166,255,0.2) !important;
        letter-spacing: 0.2px;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(88,166,255,0.3) !important;
    }

    /* ═══ INPUTS ═══ */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #0a0e17 !important;
        border: 1px solid #1c2333 !important;
        color: #e6edf3 !important;
        border-radius: 12px !important;
        transition: border-color 0.3s !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 2px rgba(88,166,255,0.1) !important;
    }
    .stSelectbox > div > div > div {
        background-color: #0a0e17 !important;
        border-color: #1c2333 !important;
        color: #e6edf3 !important;
        border-radius: 12px !important;
    }

    /* ═══ DIVIDER ═══ */
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #1c233380, transparent);
        margin: 28px 0;
    }

    /* ═══ STATUS DOTS ═══ */
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .status-green { background: #3fb950; box-shadow: 0 0 8px #3fb95060; }
    .status-red   { background: #f85149; box-shadow: 0 0 8px #f8514960; }
    .status-amber { background: #d29922; box-shadow: 0 0 8px #d2992260; }

    /* ═══ CHAT INPUT ═══ */
    .stChatInput > div {
        background-color: #0d1117 !important;
        border: 1px solid #1c2333 !important;
        border-radius: 16px !important;
    }
    .stChatInput textarea { color: #e6edf3 !important; }

    /* ═══ EXPANDER ═══ */
    div[data-testid="stExpander"] { border-color: #1c2333 !important; border-radius: 14px !important; }
    .streamlit-expanderHeader { color: #c9d1d9 !important; }

    /* ═══ NAV PILL (active page indicator) ═══ */
    .nav-active {
        background: linear-gradient(135deg, #58a6ff20, #a371f720) !important;
        border: 1px solid #58a6ff40 !important;
    }

    /* ═══ FOOTER ═══ */
    .footer {
        text-align: center;
        color: #484f58;
        font-size: 0.72rem;
        padding: 24px 0 12px;
        margin-top: 40px;
        letter-spacing: 0.5px;
    }

    /* ═══ PROFILE CARD (landing) ═══ */
    .profile-card {
        background: linear-gradient(135deg, #0d111790, #161b2260);
        backdrop-filter: blur(12px);
        border: 1px solid #1c2333;
        border-radius: 20px;
        padding: 36px 40px;
        max-width: 480px;
        margin: 30px auto;
        z-index: 1;
        position: relative;
    }
    .profile-card h3 {
        color: #e6edf3;
        margin-bottom: 20px;
        font-size: 1.3rem;
    }
    .profile-card label {
        color: #c9d1d9 !important;
    }

    /* ═══ API KEY GATE ═══ */
    .api-gate {
        background: linear-gradient(135deg, #0d111790, #161b2260);
        backdrop-filter: blur(12px);
        border: 1px solid #1c2333;
        border-radius: 20px;
        padding: 40px;
        max-width: 500px;
        margin: 30px auto;
        text-align: center;
    }
    .api-gate h3 {
        color: #e6edf3;
        margin-bottom: 12px;
    }
    .api-gate p {
        color: #8b949e;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }

    /* ═══ PROFILE DISPLAY ═══ */
    .profile-avatar-placeholder {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #58a6ff, #a371f7);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-weight: 800;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


def create_initial_state(query, student_data, subject, api_key, history=None):
    return {
        "user_query": query,
        "student_data": student_data,
        "subject": subject,
        "api_key": api_key,
        "intent": None,
        "prediction": None,
        "cluster": None,
        "metrics": {},
        "weak_areas": [],
        "reasoning": None,
        "difficulty": None,
        "trend": None,
        "study_plan": None,
        "retrieved_content": None,
        "course_recommendations": [],
        "history": history or [],
        "final_response": None
    }


def navigate(page):
    st.session_state.page = page
    save_state_to_params()
    st.rerun()


def save_state_to_params():
    """Persist user profile + current page in query params so it survives refresh."""
    params = {}
    if st.session_state.user_name:
        params["user_name"] = st.session_state.user_name
    if st.session_state.api_key:
        params["api_key"] = st.session_state.api_key
    if st.session_state.page:
        params["page"] = st.session_state.page
    st.query_params.update(params)



def page_landing():


    st.markdown("""<div class='hero'>
        <div class='hero-badge'>✨ AI-Powered Learning Analytics</div>
        <div class='hero-title'>Study Smarter,<br>Not Harder.</div>
        <div class='hero-subtitle'>Your personal AI study coach that analyzes your performance, identifies weak areas, and creates personalized learning paths — all powered by advanced machine learning.</div>
    </div>""", unsafe_allow_html=True)


    _, cta_col, _ = st.columns([1, 1, 1])
    with cta_col:
        if st.button("🚀  Get Started — It's Free", use_container_width=True, key="landing_cta"):
            navigate("onboarding")


    st.markdown("""
    <div class='features'>
        <div class='feature-card'>
            <span class='feature-icon'>🧠</span>
            <div class='feature-title'>AI Analysis</div>
            <div class='feature-desc'>ML models predict your performance and identify weak areas with smart reasoning</div>
        </div>
        <div class='feature-card'>
            <span class='feature-icon'>📚</span>
            <div class='feature-title'>Smart Resources</div>
            <div class='feature-desc'>Get curated video tutorials and courses tailored to your exact weak points</div>
        </div>
        <div class='feature-card'>
            <span class='feature-icon'>💬</span>
            <div class='feature-title'>AI Chat Coach</div>
            <div class='feature-desc'>Ask anything — your AI mentor explains, motivates, and guides you step by step</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class='tech-stack'>
        <span class='tech-badge'>LangGraph</span>
        <span class='tech-badge'>Groq LLM</span>
        <span class='tech-badge'>ChromaDB</span>
        <span class='tech-badge'>Scikit-Learn</span>
        <span class='tech-badge'>SentenceTransformers</span>
        <span class='tech-badge'>SerpAPI</span>
    </div>
    <div class='footer'>Built with ❤️ · © 2026</div>
    """, unsafe_allow_html=True)


def page_onboarding():
    st.markdown("""<div style='text-align:center;padding:60px 20px 20px'>
        <div style='font-size:2.5rem;margin-bottom:8px'>🎓</div>
        <div style='font-size:1.8rem;font-weight:800;color:#e6edf3'>Welcome to StudyAI</div>
        <div style='font-size:1rem;color:#8b949e;margin-top:8px'>Enter your details to get started</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


    _, form_col, _ = st.columns([1, 2, 1])
    with form_col:
        st.markdown("### 👤 Your Name")
        name_input = st.text_input(
            "Name",
            value=st.session_state.user_name,
            placeholder="e.g. Aniket Pathak",
            key="onboard_name",
            label_visibility="collapsed"
        )

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        st.markdown("### 🔑 Groq API Key")
        st.markdown("<p style='color:#8b949e;font-size:0.85rem;margin-top:-10px'>Required to power AI features. Get one free at <a href='https://console.groq.com/keys' target='_blank' style='color:#58a6ff'>console.groq.com/keys</a></p>", unsafe_allow_html=True)
        api_key_input = st.text_input(
            "API Key",
            value=st.session_state.api_key,
            type="password",
            placeholder="gsk_...",
            key="onboard_api_key",
            label_visibility="collapsed"
        )

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        if st.button("✅  Continue to Setup", use_container_width=True, key="onboard_cta"):
            if not name_input.strip():
                st.error("Please enter your name to continue.")
            elif not api_key_input.strip():
                st.error("Please enter your Groq API key. It's required for AI features.")
            else:
                st.session_state.user_name = name_input.strip()
                st.session_state.api_key = api_key_input.strip()
                st.session_state.profile_saved = True
                save_state_to_params()
                navigate("setup")


def render_sidebar():
    with st.sidebar:
        # User info with initial avatar
        name = st.session_state.user_name or "Student"
        initial = name[0].upper() if name else "S"
        avatar_html = f"<div class='profile-avatar-placeholder'>{initial}</div>"

        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:12px;padding:8px 0 4px'>
            {avatar_html}
            <div>
                <div style='font-weight:800;font-size:1.1rem;color:#e6edf3'>🎓 StudyAI</div>
                <div style='font-size:0.78rem;color:#8b949e;margin-top:2px'>Hello, {name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Navigation
        current = st.session_state.page
        if st.button("⚙️  Setup" + (" ●" if current == "setup" else ""), use_container_width=True, key="s_setup"):
            navigate("setup")
        if st.button("💬  Chat" + (" ●" if current == "chat" else ""), use_container_width=True, key="s_chat"):
            navigate("chat")
        if st.button("📊  Dashboard" + (" ●" if current == "dashboard" else ""), use_container_width=True, key="s_dash"):
            navigate("dashboard")

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # API key
        st.markdown("<div style='font-weight:700;font-size:0.85rem;color:#c9d1d9;margin-bottom:8px'>🔑 Groq API Key</div>", unsafe_allow_html=True)
        sidebar_key = st.text_input(
            "groq_key",
            value=st.session_state.api_key or "",
            type="password",
            placeholder="gsk_...",
            label_visibility="collapsed"
        )
        if sidebar_key:
            st.session_state.api_key = sidebar_key

        active_key = get_active_key()
        if active_key:
            st.markdown("<span class='status-dot status-green'></span> <small style='color:#3fb950;font-weight:600'>Connected</small>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='status-dot status-red'></span> <small style='color:#f85149;font-weight:600'>Not configured</small>", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Status
        if st.session_state.setup_complete:
            st.markdown(f"<div style='font-size:0.82rem'><strong>Subject:</strong> {st.session_state.subject}</div>", unsafe_allow_html=True)
            st.markdown("<span class='status-dot status-green'></span> <small style='color:#3fb950'>Ready</small>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='status-dot status-amber'></span> <small style='color:#d29922'>Setup needed</small>", unsafe_allow_html=True)

        st.markdown("<div class='footer'>StudyAI v1.0</div>", unsafe_allow_html=True)



def page_setup():
    render_sidebar()

    # Gate: require API key
    if not get_active_key():
        st.warning("🔑 Please enter your Groq API key in the sidebar before proceeding.")
        return

    st.markdown("# ⚙️ Setup Your Profile")
    st.caption("Enter your academic data. You only need to do this once.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Name
    st.markdown("### 👤 Your Name")
    name_input = st.text_input("name", value=st.session_state.user_name, placeholder="e.g. Aniket Pathak", label_visibility="collapsed")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Subject
    st.markdown("### 📘 Your Subject")
    subject = st.selectbox(
        "subject",
        ["Machine Learning", "Data Structures", "Mathematics", "DBMS", "Operating Systems", "Other"],
        label_visibility="collapsed"
    )
    if subject == "Other":
        subject = st.text_input("Enter subject", placeholder="e.g. Computer Networks")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Data
    st.markdown("### 📊 Performance Data")
    c1, c2, c3 = st.columns(3)
    with c1:
        quiz1 = st.number_input("📝 Quiz 1", 0, 100, 50, key="p_q1")
        quiz2 = st.number_input("📝 Quiz 2", 0, 100, 50, key="p_q2")
    with c2:
        quiz3 = st.number_input("📝 Quiz 3", 0, 100, 50, key="p_q3")
        time_spent = st.number_input("⏱️ Study Hrs/Day", 0.0, 10.0, 2.0, key="p_ts")
    with c3:
        assignments = st.number_input("📋 Assignments", 0, 10, 5, key="p_asgn")
        attendance = st.number_input("📅 Attendance %", 0, 100, 75, key="p_att")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        if st.button("✅  Save & Start Chatting", use_container_width=True, key="save"):
            if not name_input.strip():
                st.error("Please enter your name.")
            elif not subject or subject == "Other":
                st.error("Please select or enter a subject.")
            else:
                st.session_state.user_name = name_input.strip()
                st.session_state.student_data = {
                    "Quiz1": quiz1, "Quiz2": quiz2, "Quiz3": quiz3,
                    "Time_Spent": time_spent, "Assignments": assignments, "Attendance": attendance
                }
                st.session_state.subject = subject
                st.session_state.setup_complete = True
                st.session_state.chat_history = []
                st.session_state.history = []
                st.session_state.analysis_result = None
                save_state_to_params()
                navigate("chat")



def page_chat():
    render_sidebar()

    st.markdown("# 💬 Chat with Your AI Coach")

    # Gate: API key required
    if not get_active_key():
        st.warning("🔑 Please enter your Groq API key in the sidebar to use the chat.")
        return

    if not st.session_state.setup_complete:
        st.warning("⚠️ Please complete your profile setup first.")
        if st.button("Go to Setup"):
            navigate("setup")
        return

    st.caption(f"Subject: **{st.session_state.subject}** · Ask anything about your performance")

    active_key = get_active_key()

    # Render chat history using Streamlit's native chat widget
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "assistant"
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask your AI coach... e.g. 'Why am I weak?' or 'Give me a study plan'")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Run the full AI pipeline for every query (with memory)
        with st.spinner("🧠 Analyzing & generating response..."):
            state = create_initial_state(
                user_input,
                st.session_state.student_data,
                st.session_state.subject,
                active_key,
                history=st.session_state.history
            )
            result = graph.invoke(state)
            st.session_state.analysis_result = result

        # Get the final response from the LLM node
        response_text = result.get("final_response", "Sorry, I couldn't generate a response. Please try again.")

        # Save to chat history for display
        st.session_state.chat_history.append({"role": "ai", "content": response_text})

        # Save to session memory for context in future queries
        st.session_state.history = add_to_memory(
            st.session_state.history,
            user_input,
            response_text
        )

        st.rerun()



def page_dashboard():
    render_sidebar()

    st.markdown("# 📊 Analysis Dashboard")

    if not st.session_state.setup_complete:
        st.warning("⚠️ Please complete your profile setup first.")
        if st.button("Go to Setup"):
            navigate("setup")
        return

    # Auto-run AI pipeline if not yet run
    if not st.session_state.analysis_result:
        active_key = get_active_key()
        if not active_key:
            st.warning("🔑 Please enter your Groq API key in the sidebar.")
            return
        with st.spinner("🧠 Running AI analysis pipeline..."):
            state = create_initial_state(
                "Analyze my performance",
                st.session_state.student_data,
                st.session_state.subject,
                active_key,
                history=st.session_state.history
            )
            result = graph.invoke(state)
            st.session_state.analysis_result = result

    result = st.session_state.analysis_result

    # ── Metrics Row (styled cards) ──
    prediction = result.get("prediction", "N/A")
    cluster = result.get("cluster", "N/A")
    difficulty = result.get("difficulty", "N/A")
    trend = result.get("trend", "N/A")
    t_icon = "📉" if trend == "declining" else ("📈" if trend == "improving" else "➡️")
    pred_color = "#f85149" if prediction == "Fail" else "#3fb950"
    clust_color = "#f85149" if "At Risk" in str(cluster) else ("#3fb950" if "High" in str(cluster) else "#d29922")

    def metric_card(icon, label, value, color):
        return f"""<div style='background:linear-gradient(135deg,#0d1117,#161b22);
            border:1px solid #30363d;border-radius:16px;padding:20px 16px;
            text-align:center;'>
            <div style='font-size:1.8rem;margin-bottom:6px'>{icon}</div>
            <div style='font-size:1.4rem;font-weight:700;color:{color};margin-bottom:4px'>{value}</div>
            <div style='font-size:0.78rem;color:#8b949e;text-transform:uppercase;letter-spacing:1px'>{label}</div>
        </div>"""

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(metric_card("📊", "Prediction", prediction, pred_color), unsafe_allow_html=True)
    with m2:
        st.markdown(metric_card("📍", "Cluster", cluster, clust_color), unsafe_allow_html=True)
    with m3:
        st.markdown(metric_card("🎯", "Difficulty", difficulty, "#d29922"), unsafe_allow_html=True)
    with m4:
        st.markdown(metric_card(t_icon, "Trend", trend, "#58a6ff"), unsafe_allow_html=True)

    st.markdown("<div style='margin:24px 0'></div>", unsafe_allow_html=True)

    # ── Weak Areas + Reasoning ──
    left, right = st.columns([1, 1])
    with left:
        st.markdown("### ⚠️ Weak Areas")
        weak_areas = result.get("weak_areas", [])
        if weak_areas:
            for area in weak_areas:
                st.markdown(f"""<div style='background:#f8514912;border:1px solid #f8514925;
                    border-radius:12px;padding:10px 16px;margin-bottom:8px;
                    font-size:0.9rem;color:#f85149;font-weight:600'>🔴 {area}</div>""", unsafe_allow_html=True)
        else:
            st.success("No weak areas! 🎉")
    with right:
        st.markdown("### 🧠 AI Reasoning")
        st.markdown(f"""<div style='background:#0d1117;border:1px solid #30363d;
            border-radius:12px;padding:16px 20px;font-size:0.88rem;
            line-height:1.7;color:#c9d1d9'>{result.get('reasoning', 'N/A')}</div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:24px 0'></div>", unsafe_allow_html=True)

    # ── Study Plan ──
    st.markdown("### 📅 Study Plan")
    sp = result.get("study_plan", "")
    if sp:
        for line in sp.split("\n"):
            c = line.strip().lstrip("- ").strip()
            if c:
                st.markdown(f"""<div style='background:#0d1117;border-left:3px solid #58a6ff;
                    padding:12px 18px;margin-bottom:6px;border-radius:0 12px 12px 0;
                    font-size:0.88rem;color:#c9d1d9'>📌 {c}</div>""", unsafe_allow_html=True)
    else:
        st.caption("No study plan generated yet.")

    st.markdown("<div style='margin:24px 0'></div>", unsafe_allow_html=True)

    # ── Resources ──
    st.markdown("### 🎓 Resources")
    resources = result.get("course_recommendations", [])
    if resources:
        for r in resources:
            t = r.get("title", "Untitled")
            l = r.get("link", "#")
            th = r.get("thumbnail", "")
            tp = r.get("type", "resource")
            thumb_h = f"<img src='{th}' style='width:100px;height:60px;border-radius:10px;object-fit:cover'/>" if th else "<span style='display:inline-block;background:#1c2333;width:100px;height:60px;border-radius:10px;text-align:center;line-height:60px;font-size:1.2rem'>📚</span>"
            st.markdown(f"""<a href='{l}' target='_blank' style='text-decoration:none;color:inherit'>
                <div style='display:flex;align-items:center;gap:14px;background:linear-gradient(135deg,#0d1117,#161b22);
                border:1px solid #1c2333;border-radius:16px;padding:14px 18px;margin-bottom:10px;
                transition:all 0.3s'>{thumb_h}
                <div><div style='font-weight:600;font-size:0.95rem;color:#e6edf3;margin-bottom:4px'>{t}</div>
                <span style='font-size:0.8rem;color:#58a6ff'>{'🎬 '+tp if tp=='video' else '📘 '+tp}</span></div>
                </div></a>""", unsafe_allow_html=True)
    else:
        st.caption("No resources available yet.")



page = st.session_state.page

if page == "landing":
    page_landing()
elif page == "onboarding":
    page_onboarding()
elif page == "setup":
    page_setup()
elif page == "chat":
    page_chat()
elif page == "dashboard":
    page_dashboard()
else:
    page_landing()