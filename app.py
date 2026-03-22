import streamlit as st
import anthropic
import json

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DeepNote AI",
    page_icon="🎬",
    layout="centered",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #080A0F !important;
    color: #E8EAF0 !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 800px; }

/* Grid background */
.stApp {
    background-image:
        linear-gradient(rgba(0,255,170,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,170,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    background-color: #080A0F;
}

/* Header */
.app-header {
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 28px; padding: 12px 0;
}
.logo { font-size: 36px; }
.app-title { font-size: 26px; font-weight: 800; letter-spacing: -0.5px;
    background: linear-gradient(90deg, #fff 0%, #00C878 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.app-sub { font-size: 12px; color: #4A5568; font-family: 'JetBrains Mono', monospace; }

/* Badge */
.badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,200,120,0.08); border: 1px solid rgba(0,200,120,0.2);
    border-radius: 20px; padding: 5px 14px; font-size: 11px;
    font-family: 'JetBrains Mono', monospace; color: #00C878;
    margin-bottom: 24px;
}

/* Cards */
.result-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 20px 24px; margin-bottom: 14px;
}
.card-section-title {
    font-size: 13px; font-weight: 700; color: #00C878;
    letter-spacing: 1px; text-transform: uppercase;
    margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
}
.card-section-title::before {
    content: ''; display: inline-block; width: 3px; height: 14px;
    background: #00C878; border-radius: 2px;
}

/* Video summary */
.video-title {
    font-size: 22px; font-weight: 800; margin-bottom: 10px;
    background: linear-gradient(90deg, #fff 60%, #a0aec0 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.summary-box {
    font-size: 13.5px; color: #718096; line-height: 1.75;
    border-left: 3px solid #00C878; padding-left: 14px;
    margin-bottom: 24px;
}

/* Note bullets */
.note-bullet {
    font-size: 13px; color: #A0AEC0; padding: 4px 0 4px 16px;
    position: relative; line-height: 1.6;
}
.note-bullet::before { content: '→'; position: absolute; left: 0; color: #2D6A4F; }

/* Timestamp rows */
.ts-row {
    display: flex; gap: 12px; align-items: flex-start;
    background: rgba(255,255,255,0.02); border-radius: 10px;
    padding: 12px 14px; margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.05);
}
.ts-time {
    font-family: 'JetBrains Mono', monospace; font-size: 12px;
    color: #00A8FF; background: rgba(0,168,255,0.08);
    border: 1px solid rgba(0,168,255,0.2); border-radius: 6px;
    padding: 2px 8px; white-space: nowrap; flex-shrink: 0; margin-top: 2px;
}
.ts-topic { font-size: 13px; font-weight: 700; color: #E2E8F0; }
.ts-desc { font-size: 12px; color: #718096; margin-top: 2px; line-height: 1.5; }

/* Action items */
.action-item {
    display: flex; gap: 10px; align-items: flex-start;
    background: rgba(255,255,255,0.02); border-radius: 10px;
    padding: 12px 14px; margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.05); font-size: 13px; color: #A0AEC0;
}
.action-num {
    background: rgba(0,200,120,0.12); color: #00C878;
    border-radius: 50%; width: 20px; height: 20px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-family: 'JetBrains Mono', monospace;
}

/* Streamlit widget overrides */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important; color: #C4C9D8 !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important;
}
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #C4C9D8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #00C878 0%, #00A8FF 100%) !important;
    color: #080A0F !important; font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important; font-size: 15px !important;
    border: none !important; border-radius: 14px !important; padding: 14px !important;
}
.stButton > button:hover { box-shadow: 0 8px 30px rgba(0,200,120,0.35) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important; padding: 4px !important;
    gap: 4px !important; border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 9px !important;
    color: #4A5568 !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,200,120,0.12) !important;
    color: #00C878 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 0 !important; padding-top: 16px !important;
}
label, .stMarkdown p { color: #718096 !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="logo">🎬</div>
    <div>
        <div class="app-title">DeepNote AI</div>
        <div class="app-sub">video → structured knowledge</div>
    </div>
</div>
<div class="badge">🟢 &nbsp; AI-Powered · LLM + RAG Architecture</div>
""", unsafe_allow_html=True)


# ─── API Key Input ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.markdown("""
    <small style='color:#4A5568;font-family:JetBrains Mono,monospace;font-size:11px'>
    Get your key at<br>
    <a href='https://console.anthropic.com' style='color:#00C878'>console.anthropic.com</a>
    </small>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("**How to get transcript:**")
    st.markdown("""
    <small style='color:#718096'>
    1. Open any YouTube video<br>
    2. Click <b style='color:#fff'>⋯</b> below the video<br>
    3. Click <b style='color:#fff'>Show transcript</b><br>
    4. Select all → Copy → Paste here
    </small>
    """, unsafe_allow_html=True)


# ─── Input Form ─────────────────────────────────────────────────────────────
url = st.text_input("🔗 Video URL (optional)", placeholder="https://youtube.com/watch?v=...")

transcript = st.text_area(
    "📄 Paste Transcript *",
    height=220,
    placeholder="Paste the video transcript here...\n\nYouTube → click ⋯ below video → Show transcript → copy all text\nLectures → paste your notes or auto-generated captions",
)

analyze_clicked = st.button("🚀 Analyze Video", disabled=not transcript.strip())


# ─── Analysis Function ───────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert note-taker and information architect.
Analyze the provided video transcript and return ONLY valid JSON (no markdown, no code blocks) with this exact structure:
{
  "title": "Descriptive title of the video content",
  "summary": "2-3 sentence executive summary of what the video covers",
  "structured_notes": [
    {
      "heading": "Section heading",
      "bullets": ["Key point 1", "Key point 2", "Key point 3"]
    }
  ],
  "timestamps": [
    {
      "time": "0:00",
      "topic": "Short topic label",
      "description": "What is discussed at this point"
    }
  ],
  "action_items": [
    "Concrete action item 1",
    "Concrete action item 2"
  ]
}

Rules:
- structured_notes: 4-7 sections, each with 3-5 bullet points
- timestamps: 6-12 entries, extract or estimate from context. If no timestamps exist, space them evenly
- action_items: 5-10 concrete, actionable tasks the viewer should do
- Return ONLY the JSON object, nothing else"""


def analyze_transcript(transcript_text, video_url, key):
    client = anthropic.Anthropic(api_key=key)
    user_content = f"{'Video URL: ' + video_url + chr(10) + chr(10) if video_url else ''}Transcript:\n{transcript_text}"
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    raw = message.content[0].text.strip()
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ─── Run Analysis ────────────────────────────────────────────────────────────
if analyze_clicked:
    if not api_key:
        st.error("⚠️ Please enter your Anthropic API key in the sidebar.")
    else:
        with st.spinner("Analyzing your video with AI..."):
            try:
                result = analyze_transcript(transcript, url, api_key)
                st.session_state["result"] = result
            except json.JSONDecodeError:
                st.error("❌ Failed to parse AI response. Please try again.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ─── Display Results ─────────────────────────────────────────────────────────
if "result" in st.session_state:
    r = st.session_state["result"]

    # Title & Summary
    st.markdown(f'<div class="video-title">{r["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-box">{r["summary"]}</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs([
        f"📋 Structured Notes ({len(r['structured_notes'])})",
        f"⏱ Timestamps ({len(r['timestamps'])})",
        f"✅ Action Items ({len(r['action_items'])})",
    ])

    # --- Notes Tab ---
    with tab1:
        for section in r["structured_notes"]:
            bullets_html = "".join(
                f'<div class="note-bullet">{b}</div>' for b in section["bullets"]
            )
            st.markdown(f"""
            <div class="result-card">
                <div class="card-section-title">{section['heading']}</div>
                {bullets_html}
            </div>
            """, unsafe_allow_html=True)

    # --- Timestamps Tab ---
    with tab2:
        for ts in r["timestamps"]:
            st.markdown(f"""
            <div class="ts-row">
                <span class="ts-time">{ts['time']}</span>
                <div>
                    <div class="ts-topic">{ts['topic']}</div>
                    <div class="ts-desc">{ts['description']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- Action Items Tab ---
    with tab3:
        for i, action in enumerate(r["action_items"], 1):
            st.markdown(f"""
            <div class="action-item">
                <span class="action-num">{i}</span>
                <span>{action}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Export as Markdown
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<small style="color:#4A5568;font-family:JetBrains Mono,monospace">Export all notes as markdown</small>', unsafe_allow_html=True)
    with col2:
        md_lines = [
            f"# {r['title']}", f"\n## Summary\n{r['summary']}",
            "\n## Structured Notes",
            *[f"\n### {s['heading']}\n" + "\n".join(f"- {b}" for b in s["bullets"]) for s in r["structured_notes"]],
            "\n## Timestamps",
            *[f"{t['time']} — **{t['topic']}**: {t['description']}" for t in r["timestamps"]],
            "\n## Action Items",
            *[f"{i+1}. {a}" for i, a in enumerate(r["action_items"])],
        ]
        st.download_button(
            "⬇ Download .md",
            data="\n".join(md_lines),
            file_name="deepnote_output.md",
            mime="text/markdown",
        )

    if st.button("← Analyze another video"):
        del st.session_state["result"]
        st.rerun()
