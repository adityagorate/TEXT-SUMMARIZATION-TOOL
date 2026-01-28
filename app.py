import streamlit as st
from summarizer import summarize_text

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "length" not in st.session_state:
    st.session_state.length = 3

# ---------------- CACHED SUMMARIZER ----------------
@st.cache_data(show_spinner=False)
def cached_summary(text, length):
    return summarize_text(text, length)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f2027, #000000);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Fade animation */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
div:empty {     
    display: none !important; 
}
.card {
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
    animation: fadeUp 0.6s ease-out;
}

.card-input {
    background: rgba(30, 144, 255, 0.08);
    border-left: 5px solid #1e90ff;
}

.card-output {
    background: rgba(46, 139, 87, 0.10);
    border-left: 5px solid #2e8b57;
    min-height: 320px;
}

.card-select {
    background: rgba(138, 43, 226, 0.10);
    border-left: 5px solid #8a2be2;
}

textarea {
    background-color: #0e1621 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #1f2a38 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #ff7a18, #ffb347);
    color: black;
    border: none;
    border-radius: 12px;
    font-weight: bold;
    height: 48px;
    font-size: 16px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(255, 180, 70, 0.8);
}

.stButton > button:active {
    transform: scale(0.96);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>📝 AI Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#bbbbbb;'>Paste your text, choose length, and generate a clean summary</p>",
    unsafe_allow_html=True
)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1.1, 1])

# -------- INPUT COLUMN --------
with col1:
    st.markdown("<div class='card card-input'>", unsafe_allow_html=True)
    st.subheader("📥 Input Text")

    st.session_state.input_text = st.text_area(
        "",
        height=320,
        placeholder="Paste your long text here...",
        value=st.session_state.input_text
    )

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button("✨ Generate", use_container_width=True):
            if st.session_state.input_text.strip():
                with st.spinner("Summarizing..."):
                    st.session_state.summary = cached_summary(
                        st.session_state.input_text,
                        st.session_state.length
                    )
            else:
                st.warning("Please enter some text.")

    with btn2:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state.input_text = ""
            st.session_state.summary = ""
            st.session_state.length = 3
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card card-select'>", unsafe_allow_html=True)
    st.subheader("📏 Summary Length")

    st.session_state.length = st.selectbox(
        "Number of sentences",
        options=list(range(1, 11)),
        index=st.session_state.length - 1
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------- OUTPUT COLUMN --------
with col2:
    st.markdown("<div class='card card-output'>", unsafe_allow_html=True)
    st.subheader("📤 Summary Output")

    if st.session_state.summary:
        st.write(st.session_state.summary)
    else:
        st.write("Your summarized text will appear here.")

    st.markdown("</div>", unsafe_allow_html=True)

# python -m streamlit run app.py