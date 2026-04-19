import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from main import summarize, MAX_CHARS  # all core logic lives in main.py

load_dotenv()
def img_to_b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()


LOGO_B64 = img_to_b64("logo.png")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YT-in-Bits",
    page_icon="data:image/png;base64," + LOGO_B64,
    layout="centered",
)

# ── Font Awesome 6 Free + Google Fonts ───────────────────────────────────────
st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/css/all.min.css">
""",
    unsafe_allow_html=True,
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ─ Reset & Base ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background: #0c0c14 !important;
    color: #f0f0f8 !important;
}
.main > div { padding-top: 2rem !important; }
.block-container { 
    max-width: 820px !important; 
    padding: 3rem 1.5rem 5rem !important; 
}

/* ─ Header bar ──────────────────────────────────────────── */
.header-bar {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 0.8rem;
}
.header-bar img {
    width: 60px;
    height: 60px;
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(255, 40, 40, 0.3);
}
.app-name {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ff3b3b 0%, #ff7a00 50%, #ffd200 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.app-tagline {
    font-size: 0.85rem;
    color: #94a3b8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
}

/* ─ Divider ─────────────────────────────────────────────── */
.bit-divider {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 1.5rem 0 2rem;
}
.bit-divider span {
    width: 10px; height: 10px;
    background: #ff3b3b;
    border-radius: 3px;
    display: inline-block;
    animation: blink 1.6s infinite;
}
.bit-divider span:nth-child(2) { animation-delay: 0.2s; background: #ff7a00; }
.bit-divider span:nth-child(3) { animation-delay: 0.4s; background: #ffd200; }
.bit-divider hr { flex: 1; border: none; border-top: 2px solid #1e293b; }
@keyframes blink {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.3; transform: scale(0.9); }
}

/* ─ URL input card ─────────────────────────────────────── */
.url-card {
    background: #141424;
    border: 1px solid #2a2a45;
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.url-label {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ff3b3b;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.stTextInput > div > div > input {
    background: #fff !important;
    border: 1.5px solid #334155 !important;
    border-radius: 12px !important;
    color: #000 !important;
    padding: 0.85rem 1.25rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff3b3b !important;
    background: #ddd !important;
    box-shadow: 0 0 0 4px rgba(255, 59, 59, 0.1) !important;
}

/* ─ Summarize button ────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #ff3b3b 0%, #ff7a00 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.8rem 2rem !important;
    width: 100%;
    box-shadow: 0 4px 15px rgba(255, 59, 59, 0.2);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stButton > button:hover {
    opacity: 0.95 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 59, 59, 0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ─ Stats row ───────────────────────────────────────────── */
.stats-row {
    display: flex;
    gap: 12px;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.stat-chip {
    background: #141424;
    border: 1px solid #2a2a45;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 0.85rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: border-color 0.2s;
}
.stat-chip:hover { border-color: #ff7a00; }
.stat-chip i { color: #ff7a00; font-size: 0.9rem; }

/* ─ Summary output card ─────────────────────────────────── */
.output-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1rem;
}
.output-badge {
    background: rgba(255, 59, 59, 0.1);
    border: 1px solid rgba(255, 59, 59, 0.2);
    color: #ff7a00;
    border-radius: 30px;
    padding: 6px 18px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.summary-box {
    background: #141424;
    border: 1px solid #2a2a45;
    border-radius: 24px;
    padding: 2.2rem 2.8rem;
    line-height: 1.9;
    font-size: 1.05rem;
    color: #e2e8f0;
    white-space: pre-wrap;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.summary-box strong, .summary-box b { color: #ffffff; font-weight: 700; }

/* ─ Download button ─────────────────────────────────────── */
.stDownloadButton > button {
    background: transparent !important;
    color: #ff7a00 !important;
    border: 2px solid #ff7a00 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1.5rem !important;
    margin-top: 1rem !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(255, 122, 0, 0.1) !important;
    border-color: #ffd200 !important;
    color: #ffd200 !important;
}

/* ─ Status / spinner ────────────────────────────────────── */
.stStatus { 
    background: #141424 !important; 
    border: 1px solid #2a2a45 !important; 
    border-radius: 16px !important;
    padding: 1rem !important;
}

/* ─ Alert / warning ─────────────────────────────────────── */
.stAlert { border-radius: 10px !important; }

/* ─ FA icon helpers ─────────────────────────────────────── */
.fa-solid, .fa-regular, .fa-brands { vertical-align: middle; margin-right: 5px; }

/* ─ Footer ──────────────────────────────────────────────── */
.footer {
    text-align: center;
    color: #333;
    font-size: 0.72rem;
    margin-top: 3rem;
    letter-spacing: 0.05em;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="header-bar">
    <img src="data:image/png;base64,{LOGO_B64}" alt="YT-in-Bits logo">
    <div>
        <div class="app-name">YT-in-Bits</div>
        <div class="app-tagline">AI-powered YouTube summaries</div>
    </div>
</div>
<div class="bit-divider">
    <span></span><span></span><span></span>
    <hr>
</div>
""",
    unsafe_allow_html=True,
)


url = st.text_input(
    label="Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed",
)

summarize_clicked = st.button(
    "⚡ Break it into Bits",
    use_container_width=True,
)

# ── Logic ─────────────────────────────────────────────────────────────────────
if summarize_clicked:
    if not url.strip():
        st.warning("Paste a YouTube URL above to get started.")
    else:
        try:
            with st.status("Grabbing transcript…", expanded=True) as status:
                summary, transcript, truncated = summarize(url)  # ← from main.py

                char_count = len(transcript)
                st.markdown(
                    f'<i class="fa-solid fa-circle-check" style="color:#22c55e;"></i> '
                    f"Transcript loaded &nbsp;·&nbsp; <code>{char_count:,} chars</code>",
                    unsafe_allow_html=True,
                )
                if truncated:
                    st.markdown(
                        f'<i class="fa-solid fa-scissors" style="color:#f59e0b;"></i> '
                        f"Clipped to <code>{MAX_CHARS:,}</code> chars to stay within token limit",
                        unsafe_allow_html=True,
                    )
                status.update(
                    label='<i class="fa-solid fa-microchip"></i> Crunching bits…',
                    state="running",
                )
                status.update(label="Done!", state="complete")

            # ── Stats chips ───────────────────────────────────────────────────
            word_count = len(summary.split())
            st.markdown(
                f"""
<div class="stats-row">
    <div class="stat-chip"><i class="fa-solid fa-align-left"></i> {word_count:,} words in summary</div>
    <div class="stat-chip"><i class="fa-solid fa-film"></i> {char_count:,} transcript chars</div>
</div>
""",
                unsafe_allow_html=True,
            )

            # ── Summary output ────────────────────────────────────────────────
            st.markdown(
                """
<div class="output-header">
    <span class="output-badge"><i class="fa-solid fa-file-lines"></i>&nbsp; Summary</span>
</div>
""",
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="summary-box">{summary}</div>',
                unsafe_allow_html=True,
            )

            # ── Download ──────────────────────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="⬇️  Download Summary  (.txt)",
                data=summary,
                file_name="yt-in-bits-summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as e:
            st.markdown(
                f'<i class="fa-solid fa-triangle-exclamation" style="color:#ef4444;"></i> '
                f"<strong>Error:</strong> {e}",
                unsafe_allow_html=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="footer">
    YT-in-Bits &nbsp;·&nbsp;
    <i class="fa-solid fa-code" style="color:#333;"></i>
    Built by Ram Acharya
</div>
""",
    unsafe_allow_html=True,
)
