from pathlib import Path
import json

import streamlit as st

from spam_model import predict_spam_probability

BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "spam_nb_model.json"
SUSPICIOUS_WORDS = ["free", "winner", "won", "win", "prize", "urgent", "click", "offer",
                    "claim", "reward", "cash", "loan", "discount", "gift", "verify"]

st.set_page_config(page_title="Spam Email Detector", page_icon="📧")
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #dbeafe 0%, #f5f3ff 42%, #fff7ed 100%);
        color: #1e293b;
    }
    .block-container {max-width: 920px; padding-top: 2.5rem;}
    .stApp p, .stApp label, .stApp span, .stApp div {color: #1e293b;}
    .hero {
        background: linear-gradient(125deg, #312e81, #7c3aed 55%, #db2777);
        color: white;
        border-radius: 24px;
        padding: 2.1rem 2.2rem;
        box-shadow: 0 14px 32px rgba(88, 28, 135, .24);
        margin-bottom: 1.5rem;
    }
    .hero h1 {font-size: 2.35rem; margin: 0 0 .45rem 0; color: white !important;}
    .hero p {font-size: 1.05rem; margin: 0; opacity: .93; color: white !important;}
    div[data-testid="stTextArea"] textarea {
        background-color: white !important;
        border: 2px solid #c4b5fd !important;
        border-radius: 14px !important;
        color: #1f2937 !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #7c3aed, #db2777);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: .55rem 1.6rem;
    }
    div.stButton > button:hover {color: white; transform: translateY(-1px);}
    div[data-testid="stMetric"] {
        background: white;
        border-radius: 16px;
        padding: .8rem 1.2rem;
        border-left: 6px solid #7c3aed;
        box-shadow: 0 5px 16px rgba(76, 29, 149, .10);
    }
    h2, h3 {color: #312e81 !important; font-weight: 750 !important;}
    div[data-testid="stMetricLabel"] p {color: #475569 !important; font-weight: 700 !important;}
    div[data-testid="stMetricValue"] div {color: #5b21b6 !important; font-weight: 800 !important;}
    div[data-testid="stAlert"] p {color: #1e293b !important; font-weight: 600;}
    div[data-testid="stAlert"] svg {fill: #1e293b !important;}
    div[data-testid="stDataFrame"] * {color: #1e293b !important;}
    .stCaption, [data-testid="stCaptionContainer"] p {color: #475569 !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>📧 Spam Email Detector</h1>
  <p>AI-powered protection for suspicious emails — paste a message and get an instant safety check.</p>
</div>
""", unsafe_allow_html=True)

if not MODEL_PATH.exists():
    st.error("Model not found. Run `py train.py` in the project folder first.")
    st.stop()

model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
message = st.text_area("Email message", height=180, placeholder="Enter or paste an email here...")
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Detect", type="primary"):
    if not message.strip():
        st.warning("Please enter an email message.")
    else:
        spam_probability = predict_spam_probability(message, model)
        prediction = "spam" if spam_probability >= 0.5 else "ham"
        st.subheader("✨ Detection result")
        st.metric("Spam probability", f"{spam_probability:.1%}")
        st.progress(int(spam_probability * 100))
        if prediction == "spam":
            st.error("⚠️ Prediction: SPAM")
        else:
            st.success("✅ Prediction: NOT SPAM")
        found_words = [word for word in SUSPICIOUS_WORDS if word in message.lower()]
        if found_words:
            st.warning("Suspicious keywords found: " + ", ".join(found_words))
        else:
            st.info("No common suspicious keywords were found in this message.")
        st.caption("Tip: Do not click unknown links or share passwords, OTPs, or bank details.")
        st.session_state.history.insert(0, {"Message": message[:55] + ("..." if len(message) > 55 else ""),
                                            "Result": prediction.upper(),
                                            "Spam probability": f"{spam_probability:.1%}"})
        st.session_state.history = st.session_state.history[:10]

if st.session_state.history:
    st.divider()
    st.subheader("🕘 Recent detection history")
    st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)
    if st.button("Clear history"):
        st.session_state.history = []
        st.rerun()
