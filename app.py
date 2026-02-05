import streamlit as st
import random
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="LearnFlow AI | Bit Wizards", page_icon="🚀", layout="wide")

# --- CUSTOM CSS FOR BRANDING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF9900; color: white; }
    .stProgress > div > div > div > div { background-color: #FF9900; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & TEAM INFO ---
with st.sidebar:
    #st.image("https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg", width=100)
    #st.set_page_config(page_title="LearnFlow AI - Bit Wizards", layout="wide")
    st.sidebar.title("🚀 LearnFlow AI")
    st.divider()
    app_mode = st.radio("Navigate", ["🎓 Learning Path", "💻 Debugger Buddy", "🏆 Skill Challenge"])

# --- MODE 1: INTERACTIVE LEARNING PATH ---
if app_mode == "🎓 Learning Path":
    st.title("Personalized Learning Journey")
    col_a, col_b = st.columns([2, 1])

    with col_a:
        topic = st.text_input("What technology do you want to master?", placeholder="e.g. Python, SQL, AWS Bedrock")
        intensity = st.select_slider("Select learning intensity", options=["Casual", "Steady", "Intense"])
        
        if st.button("Construct My Path"):
            with st.status("Gathering resources...", expanded=True) as status:
                st.write("Extracting key concepts...")
                time.sleep(1)
                st.write("Organizing 7-day schedule...")
                time.sleep(1)
                status.update(label="Path Constructed!", state="complete", expanded=False)
            
            st.session_state['path_ready'] = True

    if st.session_state.get('path_ready'):
        st.divider()
        st.subheader(f"Your {intensity} Roadmap for {topic}")
        
        # Interactive Checkboxes for Progress
        days = ["Day 1: Setup & Syntax", "Day 2: Logic & Control Flow", "Day 3: Data Structures", "Day 4: API Integration"]
        progress = 0
        for i, day in enumerate(days):
            if st.checkbox(day, key=f"day_{i}"):
                progress += 25
        
        st.progress(progress)
        st.write(f"**Course Completion:** {progress}%")

# --- MODE 2: CODE DEBUGGER BUDDY ---
elif app_mode == "💻 Debugger Buddy":
    st.title("Real-time Debugger & Tutor")
    st.info("Paste your code below. I'll not only fix it but explain the concept.")
    
    code_col, explain_col = st.columns(2)
    
    with code_col:
        user_code = st.text_area("Your Code:", height=250, placeholder="def hello():\nprint('Hi')")
        if st.button("Fix My Code"):
            if "print" in user_code and "    " not in user_code: # Simple check for demo
                st.session_state['bug_found'] = True
            else:
                st.balloons()
                st.success("Code looks clean! No obvious syntax errors.")

    with explain_col:
        if st.session_state.get('bug_found'):
            st.error("🚨 Indentation Error Detected")
            st.code("def hello():\n    print('Hi')  # Added 4 spaces here", language="python")
            with st.expander("Why did this happen?"):
                st.write("In Python, indentation is used to define a block of code. Without it, the computer doesn't know which code belongs to your function!")

# --- MODE 3: SKILL CHALLENGE (GAMIFIED QUIZ) ---
elif app_mode == "🏆 Skill Challenge":
    st.title("Weekly Skill Challenge")
    
    if 'score' not in st.session_state:
        st.session_state.score = 0

    st.metric("Current Streak", f"{st.session_state.score} pts")
    
    st.write("### Question 1")
    q1 = st.radio("Which AWS service is best for running code without managing servers?", 
                  ["EC2", "Lambda", "S3", "RDS"])
    
    if st.button("Submit"):
        if q1 == "Lambda":
            st.success("Bullseye! +10 points.")
            st.session_state.score += 10
        else:
            st.error("Not quite. Hint: Think 'Serverless'.")
