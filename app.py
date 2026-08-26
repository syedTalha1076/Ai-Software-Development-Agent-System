import streamlit as st
import threading
import time
from datetime import datetime

from src.pipelines.pipeline import run_software_pipeline


# ============================================================
# PIPELINE STAGE NAMES (single source of truth)
# ============================================================

STAGE_NAMES = [
    "Project Manager",
    "Architect",
    "Developer",
    "Execution",
    "Testing",
    "Debugger",
    "Code Review",
    "Documentation",
    "Git",
    "Final Review",
]


def _execute_pipeline(requirements, result_container):
    """Runs the real pipeline on a background thread so the main
    thread stays free to animate the live progress UI."""
    try:
        result_container["result"] = run_software_pipeline(requirements)
    except Exception as exc:  # noqa: BLE001
        result_container["error"] = exc


def _render_live_steps(active_idx, theme):
    """Builds the animated step-chip grid HTML for the given active index.
    Steps before active_idx render as done, the step at active_idx renders
    as active/pulsing, everything after renders as pending."""
    chips = []
    for i, name in enumerate(STAGE_NAMES):
        if i < active_idx:
            state, icon = "done", "✓"
        elif i == active_idx:
            state, icon = "active", "●"
        else:
            state, icon = "pending", f"{i + 1:02d}"
        chips.append(
            f'<div class="live-step {state}">'
            f'<div class="live-step-icon">{icon}</div>'
            f'<div class="live-step-name">{name}</div>'
            f"</div>"
        )
    return f'<div class="live-steps-grid">{"".join(chips)}</div>'


def _render_progress_bar(pct, label):
    pct = max(0, min(100, pct))
    return f"""
    <div class="progress-shell">
        <div class="progress-fill" style="width:{pct}%;"></div>
    </div>
    <div class="progress-label">{label} — {pct}%</div>
    """


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DevForge AI | Software Development Team",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEMES
# ============================================================
# Each theme defines the CSS variables the rest of the stylesheet
# is built from. Add a new dict here to add a new theme.

THEMES = {
    "Nebula Purple": {
        "bg": "#0b1020",
        "glow1": "rgba(99,102,241,.12)",
        "glow2": "rgba(14,165,233,.10)",
        "panel": "rgba(15,23,42,.72)",
        "panel_soft": "rgba(255,255,255,.045)",
        "border": "rgba(255,255,255,.10)",
        "text": "#f8fafc",
        "text_soft": "#cbd5e1",
        "text_muted": "#94a3b8",
        "accent1": "#8b5cf6",
        "accent2": "#38bdf8",
        "accent3": "#22c55e",
        "btn_grad": "linear-gradient(90deg, #7c3aed, #2563eb)",
        "banner": "linear-gradient(135deg, rgba(34,197,94,.12), rgba(59,130,246,.10))",
        "banner_border": "rgba(34,197,94,.22)",
    },
    "Midnight Ocean": {
        "bg": "#081018",
        "glow1": "rgba(14,165,233,.14)",
        "glow2": "rgba(56,189,248,.10)",
        "panel": "rgba(10,25,38,.75)",
        "panel_soft": "rgba(255,255,255,.045)",
        "border": "rgba(255,255,255,.10)",
        "text": "#f0f9ff",
        "text_soft": "#bae6fd",
        "text_muted": "#7dd3fc",
        "accent1": "#0ea5e9",
        "accent2": "#22d3ee",
        "accent3": "#34d399",
        "btn_grad": "linear-gradient(90deg, #0284c7, #0ea5e9)",
        "banner": "linear-gradient(135deg, rgba(14,165,233,.15), rgba(34,211,238,.10))",
        "banner_border": "rgba(14,165,233,.25)",
    },
    "Emerald Tech": {
        "bg": "#07120d",
        "glow1": "rgba(16,185,129,.14)",
        "glow2": "rgba(52,211,153,.10)",
        "panel": "rgba(6,26,20,.75)",
        "panel_soft": "rgba(255,255,255,.045)",
        "border": "rgba(255,255,255,.10)",
        "text": "#ecfdf5",
        "text_soft": "#a7f3d0",
        "text_muted": "#6ee7b7",
        "accent1": "#10b981",
        "accent2": "#34d399",
        "accent3": "#a3e635",
        "btn_grad": "linear-gradient(90deg, #047857, #10b981)",
        "banner": "linear-gradient(135deg, rgba(16,185,129,.15), rgba(163,230,53,.08))",
        "banner_border": "rgba(16,185,129,.25)",
    },
    "Sunset Forge": {
        "bg": "#160b08",
        "glow1": "rgba(249,115,22,.14)",
        "glow2": "rgba(244,63,94,.10)",
        "panel": "rgba(30,12,8,.75)",
        "panel_soft": "rgba(255,255,255,.045)",
        "border": "rgba(255,255,255,.10)",
        "text": "#fff7ed",
        "text_soft": "#fed7aa",
        "text_muted": "#fdba74",
        "accent1": "#f97316",
        "accent2": "#f43f5e",
        "accent3": "#facc15",
        "btn_grad": "linear-gradient(90deg, #ea580c, #e11d48)",
        "banner": "linear-gradient(135deg, rgba(249,115,22,.15), rgba(244,63,94,.10))",
        "banner_border": "rgba(249,115,22,.25)",
    },
    "Light Studio": {
        "bg": "#f4f6fb",
        "glow1": "rgba(99,102,241,.10)",
        "glow2": "rgba(14,165,233,.08)",
        "panel": "rgba(255,255,255,.85)",
        "panel_soft": "rgba(15,23,42,.03)",
        "border": "rgba(15,23,42,.08)",
        "text": "#0f172a",
        "text_soft": "#334155",
        "text_muted": "#64748b",
        "accent1": "#7c3aed",
        "accent2": "#0284c7",
        "accent3": "#16a34a",
        "btn_grad": "linear-gradient(90deg, #7c3aed, #0284c7)",
        "banner": "linear-gradient(135deg, rgba(124,58,237,.10), rgba(2,132,199,.08))",
        "banner_border": "rgba(124,58,237,.20)",
    },
}


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "requirements" not in st.session_state:
    st.session_state.requirements = ""

if "run_time" not in st.session_state:
    st.session_state.run_time = None

if "theme" not in st.session_state:
    st.session_state.theme = "Nebula Purple"


# ============================================================
# SIDEBAR — THEME + DEVELOPER INFO
# ============================================================

with st.sidebar:
    st.markdown("### ⚙️ Appearance")
    st.session_state.theme = st.selectbox(
        "Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
        label_visibility="collapsed",
    )

    st.markdown("---")

    with st.expander("👤  About the Developer"):
        st.markdown(
            """
**Syed Talha Ali Shah**
Computer Systems Engineering Undergraduate — UET Peshawar

Builds AI-powered tools spanning agentic pipelines, computer vision
and applied ML systems, with a hands-on, project-first approach to
learning and shipping.

**Focus areas**
- Artificial Intelligence & Machine Learning
- Computer Vision
- Embedded Systems
- Agentic AI systems & LLM security

**Experience**
- AWS Cloud Club — Co-Lead (Technical), UET Peshawar
- AI/ML Intern — National Center for Big Data & Cloud Computing (NCBC)
- Data Science Intern — Aptura Tech Solutions
- AI Intern — DecodeLabs

**Contact**
📧 syedtalhaa1076@gmail.com
            """
        )

    st.caption("DevForge AI — internal build")

THEME = THEMES[st.session_state.theme]


# ============================================================
# CUSTOM CSS (built dynamically from the active theme)
# ============================================================

st.markdown(
    f"""
    <style>
        /* ---------- Global ---------- */
        .stApp {{
            background:
                radial-gradient(circle at 10% 0%, {THEME['glow1']}, transparent 28%),
                radial-gradient(circle at 90% 10%, {THEME['glow2']}, transparent 28%),
                {THEME['bg']};
        }}

        .main .block-container {{
            max-width: 1180px;
            padding-top: 1.2rem;
            padding-bottom: 3rem;
        }}

        section[data-testid="stSidebar"] {{
            background: {THEME['panel']};
            border-right: 1px solid {THEME['border']};
        }}

        section[data-testid="stSidebar"] * {{
            color: {THEME['text_soft']};
        }}

        section[data-testid="stSidebar"] h3 {{
            color: {THEME['text']};
        }}

        /* ---------- Header ---------- */
        .hero {{
            padding: 2.0rem 1.4rem 1.6rem 1.4rem;
            border: 1px solid {THEME['border']};
            border-radius: 24px;
            background: {THEME['panel']};
            box-shadow: 0 20px 60px rgba(0,0,0,.24);
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, {THEME['accent1']}22, transparent 70%);
            pointer-events: none;
        }}

        .eyebrow {{
            display: inline-block;
            font-size: .74rem;
            font-weight: 700;
            letter-spacing: .12em;
            text-transform: uppercase;
            color: {THEME['accent2']};
            background: {THEME['panel_soft']};
            border: 1px solid {THEME['border']};
            padding: .3rem .7rem;
            border-radius: 999px;
            margin-bottom: .8rem;
        }}

        .brand {{
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 800;
            letter-spacing: -0.04em;
            margin: 0;
            color: {THEME['text']};
        }}

        .gradient-text {{
            background: linear-gradient(90deg, {THEME['accent1']}, {THEME['accent2']}, {THEME['accent3']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subtitle {{
            color: {THEME['text_soft']};
            font-size: 1.02rem;
            line-height: 1.7;
            margin-top: .55rem;
            max-width: 850px;
        }}

        .developer-card {{
            margin-top: 1.2rem;
            padding: .95rem 1rem;
            border-radius: 16px;
            background: {THEME['panel_soft']};
            border: 1px solid {THEME['border']};
            color: {THEME['text_soft']};
        }}

        .developer-card strong {{
            color: {THEME['text']};
        }}

        .dev-name-stylish {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-style: italic;
            font-weight: 700;
            font-size: 1.05rem;
            background: linear-gradient(90deg, {THEME['accent1']}, {THEME['accent2']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: .01em;
        }}

        /* ---------- Cards ---------- */
        .feature-card {{
            min-height: 145px;
            padding: 1.15rem;
            border-radius: 18px;
            background: {THEME['panel']};
            border: 1px solid {THEME['border']};
            margin-bottom: .8rem;
        }}

        .feature-title {{
            color: {THEME['text']};
            font-weight: 700;
            font-size: 1.05rem;
            margin-bottom: .4rem;
        }}

        .feature-text {{
            color: {THEME['text_muted']};
            line-height: 1.55;
            font-size: .92rem;
        }}

        .step-card {{
            padding: .9rem .6rem;
            border-radius: 14px;
            background: {THEME['panel_soft']};
            border: 1px solid {THEME['border']};
            text-align: center;
            color: {THEME['text_soft']};
            min-height: 100px;
            transition: transform .15s ease, border-color .15s ease;
        }}

        .step-card:hover {{
            transform: translateY(-2px);
            border-color: {THEME['accent1']}66;
        }}

        .step-number {{
            font-size: 1.35rem;
            font-weight: 800;
            color: {THEME['accent1']};
        }}

        .step-name {{
            color: {THEME['text']};
            font-weight: 650;
            margin-top: .25rem;
        }}

        /* ---------- Results ---------- */
        .result-banner {{
            padding: 1rem 1.1rem;
            border-radius: 16px;
            background: {THEME['banner']};
            border: 1px solid {THEME['banner_border']};
            margin: .8rem 0 1rem 0;
            color: {THEME['text_soft']};
        }}

        .result-banner strong {{
            color: {THEME['text']};
        }}

        /* ---------- Streamlit controls ---------- */
        div.stButton > button {{
            width: 100%;
            border-radius: 13px;
            min-height: 48px;
            font-weight: 700;
            border: 1px solid {THEME['border']};
        }}

        div.stButton > button[kind="primary"] {{
            background: {THEME['btn_grad']};
            color: white;
            border: none;
        }}

        textarea {{
            border-radius: 14px !important;
        }}

        h2, h3, h4, p, span, label, .stMarkdown {{
            color: {THEME['text']};
        }}

        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {THEME['text_muted']} !important;
        }}

        /* ---------- Animations ---------- */
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes pulseGlow {{
            0%, 100% {{ box-shadow: 0 0 0 0 {THEME['accent1']}55; transform: translateY(0); }}
            50% {{ box-shadow: 0 0 14px 3px {THEME['accent1']}33; transform: translateY(-2px); }}
        }}

        @keyframes blobPulse {{
            0%, 100% {{ opacity: .55; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.12); }}
        }}

        .gradient-text {{
            background-size: 200% 200%;
            animation: gradientShift 6s ease infinite;
        }}

        .hero::before {{
            animation: blobPulse 5s ease-in-out infinite;
        }}

        .dev-name-stylish {{
            background-size: 200% 200%;
            animation: gradientShift 8s ease infinite;
        }}

        /* ---------- Live pipeline progress ---------- */
        .live-steps-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: .6rem;
            margin: .9rem 0;
        }}

        .live-step {{
            padding: .85rem .5rem;
            border-radius: 14px;
            text-align: center;
            border: 1px solid {THEME['border']};
            background: {THEME['panel_soft']};
            transition: all .35s ease;
        }}

        .live-step.pending {{
            opacity: .5;
        }}

        .live-step.active {{
            border-color: {THEME['accent1']};
            background: linear-gradient(135deg, {THEME['accent1']}26, {THEME['accent2']}14);
            animation: pulseGlow 1.3s ease-in-out infinite;
        }}

        .live-step.done {{
            border-color: {THEME['accent3']}99;
            background: {THEME['accent3']}17;
            opacity: 1;
        }}

        .live-step-icon {{
            font-size: 1.15rem;
            font-weight: 800;
            color: {THEME['accent1']};
        }}

        .live-step.done .live-step-icon {{
            color: {THEME['accent3']};
        }}

        .live-step.pending .live-step-icon {{
            color: {THEME['text_muted']};
        }}

        .live-step-name {{
            font-size: .76rem;
            font-weight: 650;
            color: {THEME['text']};
            margin-top: .3rem;
            line-height: 1.2;
        }}

        .progress-shell {{
            width: 100%;
            height: 15px;
            border-radius: 999px;
            background: {THEME['panel_soft']};
            border: 1px solid {THEME['border']};
            overflow: hidden;
            margin-top: .7rem;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, {THEME['accent1']}, {THEME['accent2']}, {THEME['accent3']}, {THEME['accent1']});
            background-size: 300% 100%;
            animation: gradientShift 2s linear infinite;
            transition: width .45s ease;
        }}

        .progress-label {{
            margin-top: .4rem;
            font-size: .84rem;
            font-weight: 650;
            color: {THEME['text_muted']};
            text-align: right;
        }}

        @media (max-width: 768px) {{
            .live-steps-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        /* ---------- Mobile ---------- */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: .7rem .75rem 2rem .75rem;
            }}

            .hero {{
                padding: 1.35rem 1rem;
                border-radius: 18px;
            }}

            .subtitle {{
                font-size: .94rem;
            }}

            .developer-card {{
                font-size: .9rem;
            }}

            .feature-card {{
                min-height: auto;
            }}

            .stTabs [data-baseweb="tab-list"] {{
                gap: 2px;
            }}

            .stTabs [data-baseweb="tab"] {{
                font-size: .82rem;
                padding-left: .55rem;
                padding-right: .55rem;
            }}

            div.stButton > button {{
                min-height: 50px;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <section class="hero">
        <span class="eyebrow">AI Software Delivery Platform</span>
        <h1 class="brand">
            <span class="gradient-text">DevForge AI</span>
        </h1>
        <div class="subtitle">
            An AI-powered software development team that transforms
            your requirements into a structured, tested and reviewed
            software project — end to end, with no manual handoffs.
        </div>

        <div class="developer-card">
            <span class="dev-name-stylish">Syed Talha Ali Shah</span>
            &nbsp;•&nbsp;
            <strong>Computer Systems Engineer</strong>
            &nbsp;•&nbsp;
            <strong>UET Peshawar</strong>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PIPELINE OVERVIEW
# ============================================================

st.markdown("### AI Development Pipeline")

cols = st.columns(5)

for i, name in enumerate(STAGE_NAMES):
    with cols[i % 5]:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="step-number">{i + 1:02d}</div>
                <div class="step-name">{name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")


# ============================================================
# PROJECT INPUT
# ============================================================

st.markdown("### Describe Your Software")

st.caption(
    "Tell the AI team what you want to build. Be as specific as possible "
    "about features, users, APIs, database requirements and technology preferences."
)

requirements = st.text_area(
    "Software requirements",
    value=st.session_state.requirements,
    height=190,
    placeholder=(
        "Example:\n\n"
        "Build a FastAPI student management system.\n"
        "- Student registration and login\n"
        "- JWT authentication\n"
        "- CRUD operations for students\n"
        "- PostgreSQL database\n"
        "- Pydantic validation\n"
        "- Pytest unit tests\n"
        "- Clean project structure\n"
        "- Generate documentation"
    ),
    label_visibility="collapsed",
)


# ============================================================
# EXAMPLE REQUIREMENTS
# ============================================================

with st.expander("Need an idea? Try an example"):
    examples = {
        "FastAPI Student API": (
            "Build a FastAPI student management system with CRUD operations, "
            "JWT authentication, Pydantic validation, PostgreSQL and pytest."
        ),
        "AI Chatbot API": (
            "Build a FastAPI chatbot backend with a clean REST API, "
            "conversation history, environment variables and unit tests."
        ),
        "Task Manager": (
            "Build a Python task management application with user accounts, "
            "task creation, editing, deletion, filtering and automated tests."
        ),
    }

    for label, example in examples.items():
        if st.button(label, key=f"example_{label}"):
            st.session_state.requirements = example
            st.rerun()


# ============================================================
# RUN PIPELINE
# ============================================================

run_col, clear_col = st.columns([3, 1])

with run_col:
    run_project = st.button(
        "Build Project with AI Team",
        type="primary",
        use_container_width=True,
    )

with clear_col:
    clear = st.button(
        "Clear",
        use_container_width=True,
    )

if clear:
    st.session_state.requirements = ""
    st.session_state.result = None
    st.session_state.run_time = None
    st.rerun()


if run_project:

    if not requirements.strip():
        st.warning("Please describe the software you want to build.")
        st.stop()

    st.session_state.requirements = requirements

    st.markdown("### 🚀 Build in Progress")
    status = st.empty()
    steps_placeholder = st.empty()
    bar_placeholder = st.empty()

    status.info("Starting the AI Software Development Team...")

    # Run the real pipeline on a background thread so this thread is
    # free to keep animating the live step tracker and progress bar.
    result_container = {}
    worker = threading.Thread(
        target=_execute_pipeline,
        args=(requirements, result_container),
        daemon=True,
    )
    worker.start()

    stage_idx = 0
    progress_pct = 4
    ticks = 0

    steps_placeholder.markdown(
        _render_live_steps(stage_idx, THEME), unsafe_allow_html=True
    )
    bar_placeholder.markdown(
        _render_progress_bar(progress_pct, STAGE_NAMES[stage_idx]),
        unsafe_allow_html=True,
    )

    while worker.is_alive():
        time.sleep(0.45)
        ticks += 1

        # Advance to the next stage every few ticks, but never let the
        # animation claim the LAST stage is done before the pipeline
        # actually finishes.
        if ticks % 3 == 0 and stage_idx < len(STAGE_NAMES) - 1:
            stage_idx += 1

        # Creep the bar forward, capped short of 100% until the real
        # result comes back.
        progress_pct = min(96, progress_pct + 2)

        status.info(f"Running stage: {STAGE_NAMES[stage_idx]}...")
        steps_placeholder.markdown(
            _render_live_steps(stage_idx, THEME), unsafe_allow_html=True
        )
        bar_placeholder.markdown(
            _render_progress_bar(progress_pct, STAGE_NAMES[stage_idx]),
            unsafe_allow_html=True,
        )

    worker.join()

    if "error" in result_container:
        steps_placeholder.empty()
        bar_placeholder.empty()
        status.empty()

        st.error("The development pipeline encountered an error.")

        with st.expander("Show technical error"):
            st.exception(result_container["error"])

        st.stop()

    else:
        steps_placeholder.markdown(
            _render_live_steps(len(STAGE_NAMES), THEME), unsafe_allow_html=True
        )
        bar_placeholder.markdown(
            _render_progress_bar(100, "Completed"), unsafe_allow_html=True
        )
        status.success("Project development pipeline completed successfully.")

        st.session_state.result = result_container["result"]
        st.session_state.run_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result:

    result = st.session_state.result

    st.markdown("---")
    st.markdown("## Project Results")

    if st.session_state.run_time:
        st.caption(
            f"Pipeline completed: {st.session_state.run_time}"
        )

    st.markdown(
        """
        <div class="result-banner">
            <strong>Development pipeline completed.</strong><br>
            Review the architecture, implementation, tests, code review,
            documentation and final assessment below.
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs(
        [
            "Final Review",
            "Architecture",
            "Development",
            "Execution",
            "Tests",
            "Debugging",
            "Code Review",
            "Documentation",
            "Git",
            "Plan",
        ]
    )

    with tabs[0]:
        st.markdown("### Final Project Assessment")
        st.markdown(result.get("final_review", "No final review available."))

    with tabs[1]:
        st.markdown("### System Architecture")
        st.markdown(result.get("architecture", "No architecture available."))

    with tabs[2]:
        st.markdown("### Developer Output")
        st.markdown(
            result.get(
                "development_result",
                "No development result available."
            )
        )

    with tabs[3]:
        st.markdown("### Execution Result")
        st.code(
            result.get(
                "execution_result",
                "No execution result available."
            )
        )

    with tabs[4]:
        st.markdown("### Final Test Results")
        st.code(
            result.get(
                "final_test_results",
                "No test results available."
            )
        )

    with tabs[5]:
        st.markdown("### Debugging Result")
        st.markdown(
            result.get(
                "debugging_result",
                "No debugging result available."
            )
        )

    with tabs[6]:
        st.markdown("### Code Review")
        st.markdown(
            result.get(
                "code_review",
                "No code review available."
            )
        )

    with tabs[7]:
        st.markdown("### Project Documentation")
        st.markdown(
            result.get(
                "documentation",
                "No documentation available."
            )
        )

    with tabs[8]:
        st.markdown("### Git Result")
        st.code(
            result.get(
                "git_result",
                "No Git result available."
            )
        )

    with tabs[9]:
        st.markdown("### Development Plan")
        st.markdown(
            result.get(
                "plan",
                "No development plan available."
            )
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align:center; color:{THEME['text_muted']}; padding:1rem 0;">
        <div style="font-weight:700; color:{THEME['text']};">
            DevForge AI
        </div>
        <div style="margin-top:.35rem;">
            Built by <span class="dev-name-stylish">Syed Talha Ali Shah</span>
            • Computer Systems Engineer • UET Peshawar
        </div>
        <div style="margin-top:.35rem; font-size:.82rem;">
            AI Software Development Team
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)