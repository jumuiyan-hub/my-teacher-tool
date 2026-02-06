import streamlit as st
import google.generativeai as genai

# 1. Setup & API Connection
st.set_page_config(page_title="LexiLevel - Grade 10 Tool", layout="wide")

# IMPORTANT: Replace with your actual key from aistudio.google.com
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Initialize "Memory" (Session State)
if 'result' not in st.session_state:
    st.session_state.result = ""

# 3. Custom CSS for the Dashboard Look
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem !important; }
    .stButton>button { background-color: #4F46E5; color: white; border-radius: 8px; height: 3em; width: 100%; }
    .output-box { background-color: #ffffff; padding: 25px; border-radius: 10px; border: 1px solid #e0e0e0; font-size: 1.1rem; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Analysis
with st.sidebar:
    st.title("📊 Analysis")
    st.metric("Target", "Grade 10")
    st.write("**Rules Applied:**")
    st.caption("✅ Active Voice\n✅ Formal Tone\n✅ Bracketed Definitions")

# 5. Main Interface
st.title("🎓 Grade 10 Scholar Tool")

user_input = st.text_area("Paste Original Passage:", height=200, placeholder="Paste your text here...")

# Button Logic
col1, col2, col3 = st.columns(3)

def run_ai(instruction):
    if not user_input:
        st.warning("Please paste some text first!")
        return
    full_prompt = f"{instruction}\n\nTEXT TO PROCESS:\n{user_input}"
    with st.spinner("Processing..."):
        response = model.generate_content(full_prompt)
        st.session_state.result = response.text

with col1:
    if st.button("✨ Formal Paraphrase"):
        run_ai("Rewrite this for a Grade 10 level. Use an active, formal, academic voice. Use brackets [definition] to define any complex technical terms immediately after they appear.")

with col2:
    if st.button("📚 Vocab Glossary"):
        run_ai("Identify 5 complex words from the text. Provide a formal definition for each in a list format.")

with col3:
    if st.button("❓ Comprehension"):
        run_ai("Create 3 formal multiple-choice questions based on this text to check for student understanding.")

# 6. Persistent Output Section
if st.session_state.result:
    st.divider()
    st.subheader("Result")
    st.markdown(f'<div class="output-box">{st.session_state.result}</div>', unsafe_allow_html=True)
