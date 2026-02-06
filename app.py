import streamlit as st
import google.generativeai as genai

# 1. Setup
st.set_page_config(page_title="LexiLevel - Grade 10 Chem", layout="wide")

# 2. Secure API Setup (Tries Secrets first)
try:
    # Set this up in Streamlit Cloud > Settings > Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Using the latest stable model
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception:
    st.error("API Key missing! Add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 3. Sidebar Reference
with st.sidebar:
    st.header("📊 Note Analysis")
    st.write("**Grade:** 10 (Form 4)")
    st.write("**Subject:** Chemistry")
    st.write("**Tone:** Formal Teacher")
    st.divider()
    st.caption("Active voice and bracketed definitions are applied automatically.")

# 4. Main Interface
st.title("🧪 LexiLevel: Teacher's Chemistry Notes")
st.write("Transform textbook passages into clear, active-voice notes.")

# Create two equal columns
col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.subheader("📥 Paste Textbook Text")
    user_input = st.text_area("Original Passage:", height=450, placeholder="Paste complex jargon here...")
    
    if st.button("🍎 Generate Teacher Notes", use_container_width=True):
        if user_input:
            # The "Teacher Note" Instruction
            prompt = f"""
            Act as a formal Grade 10 Chemistry teacher. 
            Rewrite the following text as clear study notes.
            - Use ACTIVE VOICE only.
            - Define any technical or hard words in brackets [definition] immediately.
            - Use bullet points for steps or concepts.
            - Maintain a professional, human-sounding teaching tone.
            
            TEXT: {user_input}
            """
            with st.spinner("Preparing your notes..."):
                try:
                    response = model.generate_content(prompt)
                    st.session_state.final_notes = response.text
                except Exception as e:
                    st.error(f"API Error: {e}")
        else:
            st.warning("Please paste some text before clicking the button!")

with col_out:
    st.subheader("📝 Your Grade 10 Notes")
    if "final_notes" in st.session_state and st.session_state.final_notes:
        # Displaying with a subtle "paper" background
        st.markdown(f"""
            <div style="background-color: #fdf6e3; padding: 25px; border-radius: 10px; 
            border-left: 10px solid #e67e22; color: #5d4037; font-size: 1.1rem;">
                {st.session_state.final_notes}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("The simplified teacher's version will appear here.")
