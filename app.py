import streamlit as st
import google.generativeai as genai

# 1. Page Config (Wide mode creates the side-by-side look)
st.set_page_config(page_title="LexiLevel - Chem Teacher Tool", layout="wide")

# IMPORTANT: Paste your actual API Key from aistudio.google.com here
API_KEY = AIzaSyCsY3c_vINChuBJL00Rm5UlQkn1Sm-CDps
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Memory Bank (Prevents content from disappearing on rerun)
if 'teacher_notes' not in st.session_state:
    st.session_state.teacher_notes = ""

# 3. Teacher Handout Styling (CSS)
st.markdown("""
    <style>
    .teacher-paper {
        background-color: #ffffff;
        padding: 30px;
        border: 1px solid #d1d5db;
        border-top: 10px solid #4F46E5;
        border-radius: 8px;
        color: #1f2937;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stTextArea textarea { font-size: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Header Section
st.title("🍎 LexiLevel: Teacher Note Generator")
st.markdown("Convert dense textbooks into **human-sounding** notes for Grade 10 Chemistry.")

# 5. Side-by-Side Interface
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Original Textbook Text")
    user_input = st.text_area(
        "Paste the passage from the curriculum or book:",
        height=350,
        placeholder="Paste here (e.g., information about exothermic reactions or periodic trends)..."
    )
    
    # Button to trigger AI
    if st.button("✨ Generate Grade 10 Notes", use_container_width=True):
        if user_input:
            teacher_prompt = f"""
            You are a helpful, formal, and clear Grade 10 Chemistry teacher. 
            Rewrite the following text as study notes for your 15-year-old students.
            
            STRICT RULES:
            - Use ACTIVE VOICE (e.g., 'The atom loses an electron' instead of 'An electron is lost').
            - Maintain a FORMAL but encouraging teacher persona.
            - Provide context for hard words: Define complex terms in brackets [like this] immediately after they appear.
            - Use bullet points for key concepts.
            - End with a one-sentence 'Key Takeaway'.
            
            TEXT TO CONVERT:
            {user_input}
            """
            with st.spinner("Writing your notes..."):
                response = model.generate_content(teacher_prompt)
                st.session_state.teacher_notes = response.text
        else:
            st.warning("Please paste some text first!")

with col2:
    st.subheader("💡 Teacher's Version")
    
    if st.session_state.teacher_notes:
        # Displaying the stylized note
        st.markdown(f'<div class="teacher-paper">{st.session_state.teacher_notes}</div>', unsafe_allow_html=True)
        
        # Download Option
        st.divider()
        st.download_button(
            label="💾 Download Notes as .txt",
            data=st.session_state.teacher_notes,
            file_name="Grade_10_Chem_Notes.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("Your simplified teacher's notes will appear here. They will include bracketed definitions and active voice formatting.")

# 6. Sidebar Reference
with st.sidebar:
    st.header("⚙️ Tool Settings")
    st.write("**Subject:** Chemistry")
    st.write("**Level:** Grade 10 (Form 4)")
    st.divider()
    st.caption("This tool uses Gemini 1.5 Flash to ensure scientific accuracy while maintaining a human-like teaching tone.")
