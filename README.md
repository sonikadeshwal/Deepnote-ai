<div align="center">

# 🎬 DeepNote AI

### Turn Any Video Into Structured Knowledge — Instantly

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge)](https://deepnote-ai-hfii7eyby2ywibtusxwdiv.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> Paste any video transcript → Get **structured notes**, **key timestamps**, **action items** & **key insights** powered by Groq's LLaMA 3.3 70B — ultra-fast AI inference.

<br/>

![DeepNote AI Banner](https://deepnote-ai-hfii7eyby2ywibtusxwdiv.streamlit.app/)

</div>

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📋 **Structured Notes** | 6-8 organized sections with detailed bullet points |
| ⏱️ **Key Timestamps** | Visual timeline of topics with descriptions |
| ✅ **Action Items** | Interactive checklist with live progress tracking |
| 💡 **Key Insights** | Core concepts, tips, stats & main takeaways |
| ⬇️ **Markdown Export** | Download all notes as a `.md` file instantly |
| ⚡ **Ultra-Fast** | Powered by Groq's LLaMA 3.3 70B — sub-second inference |

---

## 🚀 Live Demo

👉 **[Try it now → deepnote-ai.streamlit.app](https://deepnote-ai-hfii7eyby2ywibtusxwdiv.streamlit.app/)**

---

## 🧠 How It Works

```
User pastes transcript
        ↓
  Streamlit Frontend
        ↓
  Groq API (LLaMA 3.3 70B)  ←── Structured JSON Prompt Engineering
        ↓
     Parse Response
        ↓
  ┌─────────────────────────────────────┐
  │  📋 Notes  ⏱️ Timestamps  ✅ Actions  💡 Insights  │
  └─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit + Custom CSS |
| **AI Model** | LLaMA 3.3 70B (via Groq) |
| **Inference** | Groq API — ultra-low latency |
| **Language** | Python 3.10+ |
| **Deployment** | Streamlit Cloud |
| **Architecture** | LLM + RAG-Ready |

---

## 📦 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/sonikadeshwal/deepnote-ai.git
cd deepnote-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key
Get a free key at [console.groq.com](https://console.groq.com)

```python
# In app.py, replace line 12:
GROQ_API_KEY = "gsk_your_key_here"
```

### 4. Run the app
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser 🎉

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to **[share.streamlit.io](https://share.streamlit.io)**
3. Click **New App** → select your repo → set file as `app.py`
4. Go to **Settings → Secrets** and add:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
5. Click **Deploy** → get a live public URL ✅

---

## 📖 How to Get a Transcript

### YouTube (Easiest)
1. Open any YouTube video on desktop
2. Click **`···`** (three dots) below the video
3. Click **Show transcript**
4. Select all → Copy → Paste into the app

### Other Sources
- **Loom / Zoom** → use the auto-captions panel
- **Lectures** → paste your notes or `.srt` subtitle file
- **Podcasts** → use [otter.ai](https://otter.ai) to transcribe first

---

## 📁 Project Structure

```
deepnote-ai/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # You are here
└── .gitignore
```

---

## 💡 Sample Output

Given a transcript, DeepNote AI produces:

**📋 Structured Notes**
```
SECTION 01 — Introduction to Machine Learning
  ▸ ML is a subset of AI that learns from data
  ▸ Three types: supervised, unsupervised, reinforcement
  ▸ Applications include image recognition, NLP, recommendation systems
```

**⏱️ Timestamps**
```
0:00  Introduction    → Speaker introduces the topic and agenda
2:30  Core Concepts   → Deep dive into supervised learning
8:15  Practical Demo  → Live coding a simple classifier
```

**✅ Action Items**
```
1. Install scikit-learn and practice on the Iris dataset
2. Read the original ML paper by Tom Mitchell
3. Build your first classification model this weekend
```

---

## 🎯 Why This Project?

This project was built to demonstrate:

- ✅ **LLM Integration** — real-world API usage with structured prompt engineering
- ✅ **JSON Schema Prompting** — extracting structured data from unstructured text
- ✅ **RAG-Ready Architecture** — easily extendable with vector DB for multi-video search
- ✅ **Full-Stack Python** — end-to-end app from UI to AI inference
- ✅ **Production Deployment** — live on Streamlit Cloud

---

## 🔮 Future Enhancements

- [ ] 🎥 Direct YouTube URL → auto-fetch transcript
- [ ] 🔍 Multi-video search using RAG + vector database
- [ ] 🗣️ Audio file upload → Whisper transcription → notes
- [ ] 📧 Email notes directly from the app
- [ ] 🌐 Multi-language transcript support

---

## 👨‍💻 Author

Built with ❤️ for learning and placement interviews.

[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github)](https://github.com/sonikadeshwal)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sonikadeshwal/)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify and share.

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

*Made with Python 🐍 + Groq ⚡ + Streamlit 🎈*

</div>
