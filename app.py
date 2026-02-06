import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Grade 10 Scholar Tool", layout="wide")
API_KEY = "YOUR_GEMINI_API_KEY_HERE" # Get this from aistudio.google.com
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI STYLING ---
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem !important; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; height: 3em; width: 100%; }
    .output-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4F46E5; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR METRICS ---
with st.sidebar:
    st.title("📊 Analysis")
    st.metric("Target Level", "Grade 10")
    st.info("Voice: Active & Formal")
    st.divider()
    st.caption("Instructions: Definitions for complex terms will appear in [brackets].")

# --- MAIN INTERFACE ---
st.title("🎓 Grade 10 Paraphraser")
input_text = st.text_area("Paste Original Passage:", height=200, placeholder="Enter the complex text here...")

# Button Row
col1, col2, col3 = st.columns(3)

def call_gemini(custom_prompt):
    full_prompt = f"{custom_prompt}\n\nTEXT: {input_text}"
    response = model.generate_content(full_prompt)
    return response.text

if input_text:
    with col1:
        if st.button("✨ Formal Paraphrase"):
            prompt = "Rewrite this for Grade 10 students. Use active, formal voice. Define complex terms in brackets [like this] immediately after the word."
            st.session_state.result = call_gemini(prompt)
            
    with col2:
        if st.button("📚 Extract Vocab"):
            prompt = "List the 5 most difficult words from this text and provide simple Grade 10 definitions for each."
            st.session_state.result = call_gemini(prompt)

    with col3:
        if st.button("❓ Quick Quiz"):
            prompt = "Create 3 multiple choice questions based on this text for a Grade 10 level."
            st.session_state.result = call_gemini(prompt)

# --- OUTPUT DISPLAY ---
if 'result' in st.session_state:
    st.subheader("Results")
    st.markdown(f'<div class="output-box">{st.session_state.result}</div>', unsafe_allow_html=True)
