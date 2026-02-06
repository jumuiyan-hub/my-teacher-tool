import streamlit as st
import google.generativeai as genai

# 1. Setup
st.set_page_config(page_title="LexiLevel - Grade 10 Chem", layout="wide")

# 2. Secure API Setup (Uses Streamlit Secrets)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key not found! Add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 3. Sidebar
with st.sidebar:
    st.header("📊 Note Settings")
    st.write("**Grade:** 10 / Form 4")
    st.write("**Voice:** Formal Teacher Notes")
    st.divider()
    st.caption("Definitions for hard words are automatically added in [brackets].")

# 4. Main Interface
st.title("🍎 LexiLevel: Grade 10 Chemistry Note Transformer")

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.subheader("📥 Textbook Input")
    user_text = st.text_area("Paste complex chemistry text here:", height=400)
    
    if st.button("✨ Create Teacher Notes", use_container_width=True):
        if user_text:
            prompt = f"Act as a formal Grade 10 Chemistry teacher. Paraphrase this into notes using active voice. Define complex terms in brackets [definition] immediately after they appear. Use bullets.\n\nTEXT: {user_text}"
            with st.spinner("Writing notes..."):
                try:
                    response = model.generate_content(prompt)
                    st.session_state.result = response.text
                except Exception as api_err:
                    st.error(f"AI Error: {api_err}")
        else:
            st.warning("Please paste some text first!")

with col_right:
    st.subheader("📝 Simplified Version")
    if "result" in st.session_state:
        st.markdown(f"""<div style="background-color: #fdf6e3; padding: 20px; border-radius: 10px; border-left: 8px solid #e67e22; color: #5d4037;">
            {st.session_state.result}
        </div>""", unsafe_allow_html=True)
    else:
        st.info("The teacher-style notes will appear here.")
