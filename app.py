import streamlit as st
import json
from groq import Groq

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DeepNote AI",
    page_icon="🎬",
    layout="wide",
)

# ─── API Config ─────────────────────────────────────────────────────────────
GROQ_API_KEY = "your_groq_api_key_here"   # 🔑 Replace with your Groq API key
GROQ_MODEL   = "llama-3.3-70b-versatile"

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
* { font-family: Arial, sans-serif !important; box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    background-color: #05070D !important;
    color: #F1F5F9 !important;
    font-family: Arial, sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #05070D; }
::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 3px; }

/* BG */
.bg-blobs { position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden; }
.blob { position:absolute; border-radius:50%; filter:blur(130px); opacity:0.13; animation:blobDrift 18s ease-in-out infinite; }
.blob1 { width:700px; height:700px; background:#6366F1; top:-200px; left:-200px; }
.blob2 { width:600px; height:600px; background:#8B5CF6; bottom:-200px; right:-150px; animation-delay:-6s; }
.blob3 { width:400px; height:400px; background:#06B6D4; top:40%; left:40%; animation-delay:-12s; }
@keyframes blobDrift { 0%,100%{transform:translate(0,0) scale(1);} 33%{transform:translate(40px,-40px) scale(1.05);} 66%{transform:translate(-30px,30px) scale(0.95);} }
.grid-lines {
    position:fixed; inset:0; z-index:0; pointer-events:none;
    background-image: linear-gradient(rgba(255,255,255,0.022) 1px,transparent 1px), linear-gradient(90deg,rgba(255,255,255,0.022) 1px,transparent 1px);
    background-size:60px 60px;
}

/* NAV */
.nav {
    position:sticky; top:0; z-index:100; display:flex; align-items:center; justify-content:space-between;
    padding:18px 52px; background:rgba(5,7,13,0.75); backdrop-filter:blur(24px);
    border-bottom:1px solid rgba(255,255,255,0.07);
    animation:slideDown 0.6s cubic-bezier(.16,1,.3,1) both;
}
@keyframes slideDown { from{opacity:0;transform:translateY(-20px);} to{opacity:1;transform:translateY(0);} }
.nav-logo { display:flex; align-items:center; gap:12px; }
.nav-icon { width:44px; height:44px; border-radius:12px; background:linear-gradient(135deg,#6366F1,#8B5CF6); display:flex; align-items:center; justify-content:center; font-size:22px; box-shadow:0 0 28px rgba(99,102,241,0.5); animation:iconPulse 3s ease-in-out infinite; }
@keyframes iconPulse { 0%,100%{box-shadow:0 0 28px rgba(99,102,241,0.5);} 50%{box-shadow:0 0 48px rgba(99,102,241,0.9);} }
.nav-brand { font-size:24px; font-weight:900; color:#fff; letter-spacing:-0.5px; }
.nav-brand span { background:linear-gradient(90deg,#6366F1,#06B6D4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.nav-pill { background:rgba(99,102,241,0.12); border:1px solid rgba(99,102,241,0.3); border-radius:24px; padding:8px 18px; font-size:14px; font-weight:800; color:#A5B4FC; display:flex; align-items:center; gap:8px; }
.nav-dot { width:8px; height:8px; border-radius:50%; background:#10B981; display:inline-block; animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* MAIN */
.main-wrap { position:relative; z-index:1; padding:0 52px 80px; }

/* HERO */
.hero { text-align:center; padding:70px 24px 50px; animation:heroUp 0.8s cubic-bezier(.16,1,.3,1) 0.2s both; }
@keyframes heroUp { from{opacity:0;transform:translateY(40px);} to{opacity:1;transform:translateY(0);} }
.hero-badge { display:inline-flex; align-items:center; gap:8px; background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.25); border-radius:30px; padding:9px 22px; margin-bottom:28px; font-size:15px; font-weight:800; color:#A5B4FC; }
.hero-title { font-size:clamp(42px,6vw,80px); font-weight:900; line-height:1.05; letter-spacing:-2.5px; color:#fff; margin-bottom:22px; }
.hero-title .grad { background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 45%,#06B6D4 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; filter:drop-shadow(0 0 32px rgba(99,102,241,0.5)); }
.hero-sub { font-size:clamp(16px,2.2vw,20px); color:#64748B; max-width:580px; margin:0 auto; line-height:1.7; font-weight:500; }

/* INPUT */
.inp-wrap { max-width:900px; margin:0 auto; animation:heroUp 0.8s cubic-bezier(.16,1,.3,1) 0.35s both; }
.chips { display:flex; gap:8px; flex-wrap:wrap; padding:12px 0 4px; }
.chip { font-size:12px; font-weight:700; padding:5px 13px; border-radius:20px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08); color:#64748B; }

/* Widget overrides */
label, .stTextInput label, .stTextArea label { display:none !important; }
.stTextInput > div > div > input {
    background:rgba(255,255,255,0.04) !important; border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:12px !important; color:#F1F5F9 !important;
    font-family:Arial,sans-serif !important; font-size:16px !important; font-weight:600 !important;
    padding:14px 18px !important;
}
.stTextInput > div > div > input::placeholder { color:#1E293B !important; }
.stTextArea > div > div > textarea {
    background:rgba(255,255,255,0.03) !important; border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:16px !important; color:#CBD5E1 !important;
    font-family:Arial,sans-serif !important; font-size:15px !important; font-weight:500 !important;
    line-height:1.75 !important; padding:18px 22px !important; min-height:220px !important;
}
.stTextArea > div > div > textarea::placeholder { color:#1E293B !important; }

/* BUTTON */
.stButton > button {
    width:100% !important; background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%) !important;
    color:#fff !important; font-family:Arial,sans-serif !important; font-size:19px !important;
    font-weight:900 !important; border:none !important; border-radius:18px !important;
    padding:18px 36px !important; margin-top:8px !important;
    box-shadow:0 8px 36px rgba(99,102,241,0.45) !important; transition:all 0.25s !important;
}
.stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 18px 52px rgba(99,102,241,0.6) !important; }
.stButton > button:disabled { opacity:0.35 !important; }

/* ERROR */
.err-box { background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2); border-radius:16px; padding:18px 22px; font-size:15px; font-weight:700; color:#FCA5A5; display:flex; gap:10px; align-items:center; margin-top:14px; }

/* RESULTS */
.res-eyebrow { font-size:12px; font-weight:900; letter-spacing:2.5px; text-transform:uppercase; color:#6366F1; margin-bottom:10px; display:flex; align-items:center; gap:10px; }
.res-eyebrow::before { content:''; display:block; width:28px; height:2.5px; background:#6366F1; border-radius:2px; }
.res-video-title { font-size:clamp(26px,4vw,44px); font-weight:900; color:#fff; line-height:1.12; letter-spacing:-1.5px; margin-bottom:16px; }
.res-summary { font-size:17px; color:#94A3B8; line-height:1.75; font-weight:500; border-left:3px solid #6366F1; padding-left:20px; max-width:760px; margin-bottom:20px; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background:rgba(255,255,255,0.03) !important; border:1px solid rgba(255,255,255,0.08) !important; border-radius:20px !important; padding:5px !important; gap:4px !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; border-radius:15px !important; color:#64748B !important; font-family:Arial,sans-serif !important; font-size:15px !important; font-weight:800 !important; padding:12px 20px !important; border:none !important; transition:all 0.25s !important; }
.stTabs [aria-selected="true"] { background:rgba(99,102,241,0.15) !important; color:#fff !important; }
.stTabs [data-baseweb="tab-panel"] { padding:0 !important; padding-top:24px !important; }
.stTabs [data-baseweb="tab-highlight"] { display:none !important; }

/* NOTES */
.notes-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(310px,1fr)); gap:16px; }
.note-card { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:22px; padding:26px; transition:all 0.3s; animation:cardIn 0.4s cubic-bezier(.16,1,.3,1) both; }
.note-card:hover { border-color:rgba(99,102,241,0.3); background:rgba(99,102,241,0.05); transform:translateY(-4px); box-shadow:0 20px 48px rgba(0,0,0,0.35); }
@keyframes cardIn { from{opacity:0;transform:translateY(18px);} to{opacity:1;transform:translateY(0);} }
.note-num { font-size:11px; font-weight:900; color:#6366F1; background:rgba(99,102,241,0.12); border-radius:6px; padding:4px 10px; display:inline-block; margin-bottom:14px; letter-spacing:1.5px; }
.note-head { font-size:19px; font-weight:900; color:#fff; margin-bottom:14px; line-height:1.25; }
.note-divider { height:1px; background:rgba(255,255,255,0.07); margin-bottom:14px; }
.note-list { list-style:none; display:flex; flex-direction:column; gap:9px; padding:0; margin:0; }
.note-list li { font-size:14px; color:#94A3B8; line-height:1.65; font-weight:500; display:flex; gap:10px; align-items:flex-start; }
.arr { color:#6366F1; flex-shrink:0; font-size:12px; margin-top:3px; }

/* TIMESTAMPS */
.ts-timeline { position:relative; padding-left:38px; }
.ts-line { position:absolute; left:12px; top:10px; bottom:10px; width:2.5px; background:linear-gradient(to bottom,#6366F1,#8B5CF6,#06B6D4); border-radius:3px; }
.ts-item { position:relative; display:flex; gap:18px; align-items:flex-start; margin-bottom:10px; background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:20px 22px; transition:all 0.3s; animation:cardIn 0.4s cubic-bezier(.16,1,.3,1) both; }
.ts-item::before { content:''; position:absolute; left:-31px; top:50%; transform:translateY(-50%); width:14px; height:14px; border-radius:50%; background:#6366F1; border:2.5px solid #05070D; box-shadow:0 0 10px rgba(99,102,241,0.6); }
.ts-item:hover { border-color:rgba(99,102,241,0.35); background:rgba(99,102,241,0.05); transform:translateX(5px); }
.ts-badge { background:linear-gradient(135deg,#6366F1,#8B5CF6); border-radius:12px; padding:8px 16px; font-size:15px; font-weight:900; color:#fff; flex-shrink:0; align-self:flex-start; box-shadow:0 4px 14px rgba(99,102,241,0.35); white-space:nowrap; }
.ts-topic { font-size:18px; font-weight:900; color:#fff; margin-bottom:5px; }
.ts-desc  { font-size:14px; color:#64748B; line-height:1.6; font-weight:500; }

/* ACTIONS */
.prog-header { display:flex; justify-content:space-between; margin-bottom:10px; }
.prog-label { font-size:15px; font-weight:800; color:#64748B; }
.prog-label span { color:#10B981; font-size:17px; }
.prog-wrap { height:5px; background:#1E293B; border-radius:5px; overflow:hidden; margin-bottom:22px; }
.prog-fill { height:100%; background:linear-gradient(90deg,#10B981,#06B6D4); border-radius:5px; transition:width 0.6s cubic-bezier(.16,1,.3,1); }
.act-row { display:flex; align-items:flex-start; gap:14px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:18px; padding:18px 22px; margin-bottom:8px; transition:all 0.25s; animation:cardIn 0.4s cubic-bezier(.16,1,.3,1) both; }
.act-num { font-size:13px; font-weight:900; color:#64748B; flex-shrink:0; min-width:26px; margin-top:3px; }
.act-text { font-size:17px; font-weight:700; color:#CBD5E1; line-height:1.55; flex:1; }

/* INSIGHTS */
.ins-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; }
.ins-card { border-radius:22px; padding:26px; animation:cardIn 0.4s cubic-bezier(.16,1,.3,1) both; border:1px solid; }
.ins-card.t0 { background:rgba(99,102,241,0.07); border-color:rgba(99,102,241,0.2); }
.ins-card.t1 { background:rgba(139,92,246,0.07); border-color:rgba(139,92,246,0.2); }
.ins-card.t2 { background:rgba(6,182,212,0.07); border-color:rgba(6,182,212,0.2); }
.ins-card.t3 { background:rgba(16,185,129,0.07); border-color:rgba(16,185,129,0.2); }
.ins-icon { font-size:30px; margin-bottom:14px; display:block; }
.ins-label { font-size:11px; font-weight:900; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.t0 .ins-label{color:#818CF8;} .t1 .ins-label{color:#A78BFA;} .t2 .ins-label{color:#67E8F9;} .t3 .ins-label{color:#6EE7B7;}
.ins-text { font-size:16px; font-weight:700; color:#E2E8F0; line-height:1.55; }

/* SIDEBAR */
section[data-testid="stSidebar"] { background:rgba(5,7,13,0.95) !important; border-right:1px solid rgba(255,255,255,0.07) !important; }
section[data-testid="stSidebar"] * { font-family:Arial,sans-serif !important; }
.sidebar-logo { font-size:26px; font-weight:900; color:#fff; margin-bottom:4px; }
.sidebar-logo span { background:linear-gradient(90deg,#6366F1,#06B6D4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.sidebar-sub { font-size:12px; color:#64748B; margin-bottom:20px; }
.sidebar-section { font-size:11px; font-weight:900; letter-spacing:2px; text-transform:uppercase; color:#6366F1; margin:20px 0 10px; }
.how-step { display:flex; gap:10px; align-items:flex-start; margin-bottom:10px; font-size:13px; color:#94A3B8; line-height:1.5; }
.step-n { background:rgba(99,102,241,0.15); color:#A5B4FC; border-radius:50%; width:22px; height:22px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:900; flex-shrink:0; }

/* DOWNLOAD BTN */
.stDownloadButton > button { background:rgba(16,185,129,0.1) !important; border:1px solid rgba(16,185,129,0.3) !important; color:#6EE7B7 !important; font-family:Arial,sans-serif !important; font-size:14px !important; font-weight:800 !important; border-radius:12px !important; padding:10px 20px !important; }
.stDownloadButton > button:hover { background:rgba(16,185,129,0.2) !important; }

/* CHECKBOX */
.stCheckbox > label { color:#CBD5E1 !important; font-size:16px !important; font-weight:700 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Background ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="bg-blobs">
  <div class="blob blob1"></div><div class="blob blob2"></div><div class="blob blob3"></div>
</div>
<div class="grid-lines"></div>
""", unsafe_allow_html=True)

# ─── Nav ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav">
  <div class="nav-logo">
    <div class="nav-icon">🎬</div>
    <div class="nav-brand">Deep<span>Note</span> AI</div>
  </div>
  <div class="nav-pill"><span class="nav-dot"></span>&nbsp; Groq · LLaMA 3.3 70B · RAG-Ready</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">Deep<span>Note</span> AI</div>
    <div class="sidebar-sub">video → structured knowledge</div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-section">How to get transcript</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="how-step"><span class="step-n">1</span>Open any YouTube video</div>
    <div class="how-step"><span class="step-n">2</span>Click <b style="color:#fff">⋯</b> below the video</div>
    <div class="how-step"><span class="step-n">3</span>Click <b style="color:#fff">Show transcript</b></div>
    <div class="how-step"><span class="step-n">4</span>Select all → Copy → Paste here</div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-section">Supported Sources</div>', unsafe_allow_html=True)
    for src in ["🎬 YouTube", "📹 Loom", "📞 Zoom / Meet", "🎓 Lectures", "🎙️ Podcasts"]:
        st.markdown(f"<div style='font-size:13px;color:#64748B;padding:4px 0'>{src}</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-section">Tech Stack</div>', unsafe_allow_html=True)
    for item in ["⚡ Groq LLaMA 3.3 70B", "🐍 Python + Streamlit", "🧠 Structured Prompting", "📦 RAG-Ready Architecture"]:
        st.markdown(f"<div style='font-size:12px;color:#64748B;padding:3px 0'>{item}</div>", unsafe_allow_html=True)

# ─── Prompt ───────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an elite video content analyst.
Return ONLY valid JSON — no markdown, no backticks, no preamble:
{
  "title": "Engaging title of the video",
  "summary": "2-3 sentence executive summary of core value and takeaways",
  "structured_notes": [{"heading": "Section heading", "bullets": ["Point 1","Point 2","Point 3","Point 4"]}],
  "timestamps": [{"time": "0:00", "topic": "Topic label", "description": "What is discussed here"}],
  "action_items": ["Concrete task 1", "Concrete task 2"],
  "key_insights": [{"icon": "💡", "label": "Core Concept", "text": "Insight text"}]
}
Rules:
- structured_notes: 6-8 sections, 3-5 bullets each
- timestamps: 8-14 entries, estimate if not given
- action_items: 6-10 high-value tasks
- key_insights: exactly 8 items, labels from: Core Concept, Key Quote, Pro Tip, Warning, Key Stat, Framework, Resource, Main Takeaway
- Return ONLY the JSON object"""


def run_analysis(text, video_url):
    client  = Groq(api_key=GROQ_API_KEY)
    content = f"{'Video URL: ' + video_url + chr(10)*2 if video_url else ''}TRANSCRIPT:\n{text}"
    resp    = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":content}],
        max_tokens=4096, temperature=0.3,
    )
    raw   = resp.choices[0].message.content.strip()
    clean = raw.replace("```json","").replace("```","").strip()
    return json.loads(clean)


# ─── Page ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# ══════════════ INPUT PAGE ══════════════
if "result" not in st.session_state:
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">✨ More Advanced Than ScreenApp — Powered by Groq LLaMA 3.3 70B</div>
      <h1 class="hero-title">Turn Any Video Into<br/><span class="grad">Structured Knowledge</span></h1>
      <p class="hero-sub">Paste a transcript — get structured notes, timestamps, action items & key insights instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="inp-wrap">', unsafe_allow_html=True)
    url = st.text_input("url", placeholder="🔗  Video URL — YouTube, Loom, Zoom, etc.  (optional)", label_visibility="collapsed")
    st.markdown('<div class="chips"><span class="chip">YouTube</span><span class="chip">Loom</span><span class="chip">Zoom</span><span class="chip">Lectures</span><span class="chip">Podcasts</span><span class="chip">Meetings</span></div>', unsafe_allow_html=True)
    transcript = st.text_area("transcript", placeholder="Paste your video transcript here...\n\n• YouTube → click ⋯ below video → Show transcript → Select all → Copy\n• Loom / Zoom → use the auto-captions panel\n• Lectures → paste notes or subtitle (.srt) text", height=240, label_visibility="collapsed")
    if st.session_state.get("err"):
        st.markdown(f'<div class="err-box">⚠️ {st.session_state.err}</div>', unsafe_allow_html=True)
        st.session_state.err = ""
    go = st.button("🚀  Analyze Video with AI", disabled=not (transcript or "").strip(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if go:
        with st.spinner("Running LLaMA 3.3 70B via Groq — ultra-fast inference..."):
            try:
                st.session_state.result = run_analysis(transcript, url or "")
                st.session_state.done_tasks = []
                st.rerun()
            except json.JSONDecodeError:
                st.session_state.err = "Failed to parse AI response. Please try again."
                st.rerun()
            except Exception as e:
                st.session_state.err = f"Error: {str(e)}"
                st.rerun()

# ══════════════ RESULTS PAGE ══════════════
else:
    r = st.session_state.result

    # Build markdown export
    md = "\n".join([
        f"# {r['title']}", f"\n## Summary\n{r['summary']}",
        "\n## Structured Notes",
        *[f"\n### {s['heading']}\n" + "\n".join(f"- {b}" for b in s["bullets"]) for s in r["structured_notes"]],
        "\n## Timestamps",
        *[f"**{t['time']}** — {t['topic']}: {t['description']}" for t in r["timestamps"]],
        "\n## Action Items",
        *[f"{i+1}. {a}" for i, a in enumerate(r["action_items"])],
        "\n## Key Insights",
        *[f"**{k['label']}**: {k['text']}" for k in r["key_insights"]],
    ])

    hc1, hc2 = st.columns([3, 1])
    with hc1:
        st.markdown(f"""
        <div class="res-eyebrow">Analysis Complete</div>
        <div class="res-video-title">{r['title']}</div>
        <div class="res-summary">{r['summary']}</div>
        """, unsafe_allow_html=True)
    with hc2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.download_button("📋 Download Notes (.md)", data=md, file_name="deepnote.md", mime="text/markdown", use_container_width=True)
        if st.button("↩  New Video", use_container_width=True):
            del st.session_state.result
            st.rerun()

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        f"📋  Structured Notes  ({len(r['structured_notes'])})",
        f"⏱️  Timestamps  ({len(r['timestamps'])})",
        f"✅  Action Items  ({len(r['action_items'])})",
        f"💡  Key Insights  ({len(r['key_insights'])})",
    ])

    # ── NOTES ──
    with tab1:
        html = '<div class="notes-grid">'
        for i, s in enumerate(r["structured_notes"]):
            bullets = "".join(f'<li><span class="arr">▸</span>{b}</li>' for b in s["bullets"])
            html += f'<div class="note-card" style="animation-delay:{i*0.06}s"><div class="note-num">SECTION {str(i+1).zfill(2)}</div><div class="note-head">{s["heading"]}</div><div class="note-divider"></div><ul class="note-list">{bullets}</ul></div>'
        st.markdown(html + "</div>", unsafe_allow_html=True)

    # ── TIMESTAMPS ──
    with tab2:
        html = '<div class="ts-timeline"><div class="ts-line"></div>'
        for i, ts in enumerate(r["timestamps"]):
            html += f'<div class="ts-item" style="animation-delay:{i*0.05}s"><span class="ts-badge">{ts["time"]}</span><div><div class="ts-topic">{ts["topic"]}</div><div class="ts-desc">{ts["description"]}</div></div></div>'
        st.markdown(html + "</div>", unsafe_allow_html=True)

    # ── ACTIONS ──
    with tab3:
        total = len(r["action_items"])
        done  = st.session_state.get("done_tasks", [False] * total)
        if len(done) != total: done = [False] * total
        n_done = sum(done)
        pct    = int((n_done / total) * 100) if total else 0
        st.markdown(f'<div class="prog-header"><div class="prog-label"><span>{n_done}</span> / {total} completed</div><div class="prog-label"><span>{pct}%</span></div></div><div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)
        for i, action in enumerate(r["action_items"]):
            c1, c2 = st.columns([0.04, 0.96])
            with c1:
                checked = st.checkbox("", value=done[i], key=f"chk_{i}", label_visibility="collapsed")
                done[i] = checked
            with c2:
                style = "text-decoration:line-through;color:#64748B;" if checked else "color:#CBD5E1;"
                st.markdown(f'<div class="act-row"><div class="act-num">#{i+1}</div><div class="act-text" style="{style}">{action}</div></div>', unsafe_allow_html=True)
        st.session_state.done_tasks = done

    # ── INSIGHTS ──
    with tab4:
        html = '<div class="ins-grid">'
        for i, k in enumerate(r["key_insights"]):
            html += f'<div class="ins-card t{i%4}" style="animation-delay:{i*0.06}s"><span class="ins-icon">{k["icon"]}</span><div class="ins-label">{k["label"]}</div><div class="ins-text">{k["text"]}</div></div>'
        st.markdown(html + "</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
