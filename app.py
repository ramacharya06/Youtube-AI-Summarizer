import streamlit as st
from main import summarize, MAX_CHARS  # ← all core logic lives in main.py

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube AI Summarizer",
    page_icon="🎬",
    layout="centered",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background: #0f0f0f; }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff4e4e, #ff8c00, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .summary-box {
        background: #fff;
        border: 1px solid #2e2e2e;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-top: 1.5rem;
        line-height: 1.8;
    }
    .stTextInput > div > div > input {
        background: #fff !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #000 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #ff4e4e, #ff8c00) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.6rem 2rem !important;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }
    .badge {
        display: inline-block;
        background: #2a2a2a;
        color: #ff8c00;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Font Awesome 6 Free (open-source icon library via jsDelivr CDN) ───────────
st.markdown("""
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/css/all.min.css"
/>
<style>
    .fa-solid, .fa-regular, .fa-brands { vertical-align: middle; margin-right: 5px; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero-title">'
    '<i class="fa-brands fa-youtube" style="color:#ff0000;-webkit-text-fill-color:#ff0000;"></i> '
    'YouTube AI Summarizer'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">'
    '<i class="fa-solid fa-wand-magic-sparkles"></i> '
    'Paste any YouTube URL and get an instant AI-powered summary'
    '</div>',
    unsafe_allow_html=True,
)

# ── Input ────────────────────────────────────────────────────────────────────
url = st.text_input(
    label="YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed",
)

summarize_clicked = st.button("✨ Summarize", use_container_width=True)

# ── Logic (delegates entirely to main.summarize) ─────────────────────────────
if summarize_clicked:
    if not url.strip():
        st.warning("Please enter a YouTube URL first.")
    else:
        try:
            with st.status("Fetching transcript…", expanded=True) as status:
                summary, transcript, truncated = summarize(url)  # ← from main.py

                st.markdown(
                    f'<i class="fa-solid fa-circle-check" style="color:#22c55e;"></i> '
                    f'Transcript fetched ({len(transcript):,} chars)',
                    unsafe_allow_html=True,
                )
                if truncated:
                    st.markdown(
                        f'<i class="fa-solid fa-scissors" style="color:#f59e0b;"></i> '
                        f'Truncated to {MAX_CHARS:,} chars to fit token limits',
                        unsafe_allow_html=True,
                    )

                status.update(label="Done!", state="complete")

            # ── Output ───────────────────────────────────────────────────────
            st.markdown(
                '<div class="badge"><i class="fa-solid fa-file-lines"></i> AI Summary</div>',
                unsafe_allow_html=True,
            )
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

            st.download_button(
                label="⬇️ Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain",
            )

        except Exception as e:
            st.markdown(
                f'<i class="fa-solid fa-triangle-exclamation" style="color:#ef4444;"></i> '
                f'<strong>Error:</strong> {e}',
                unsafe_allow_html=True,
            )
