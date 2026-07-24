import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.graph import graph_engine

# Set page configuration
st.set_page_config(page_title="Multi-Agent Workspace", layout="wide", page_icon="🧠")

# Initialize session state 
if "project_prompt" not in st.session_state:
    st.session_state.project_prompt = None
if "final_state" not in st.session_state:
    st.session_state.final_state = None

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🤖 AI Team Modules")
selected_module = st.sidebar.radio(
    "Select View:",
    ["📐 Architecture", "💻 Code", "🧪 Testing"]
)
st.sidebar.divider()

with st.sidebar:
  st.markdown("---")
  st.markdown("### 👨‍💻 Developed By")
  st.markdown("**Rasheed Ahmad**")
  st.markdown("🤖 AI Student @ COMSATS University Islamabad")
  st.markdown("💻 Machine Learning Engineer & Backend Developer(FastAPI)")
  st.markdown("---")

# --- MAIN SCREEN HEADER ---
st.title("🚀 Project Workspace")

# --- BOTTOM PROMPT INPUT ---
prompt = st.chat_input("📝 Enter your project idea here (e.g., Build a FastAPI auth system...)")

if prompt:
    st.session_state.project_prompt = prompt
    st.session_state.final_state = None 

# --- MAIN SCREEN DISPLAY LOGIC ---
if st.session_state.project_prompt:
    st.markdown("### 💡 Project Concept")
    st.info(st.session_state.project_prompt)
    st.divider()
    
 
    # GRAPH EXECUTION (Frontend meets Backend)
    
    if st.session_state.final_state is None:
        with st.spinner("🚀 The AI Team is working on your project. Please wait..."):
           
            initial_state = {
                "user_prompt": st.session_state.project_prompt,
                "iterations": 0
            }
            
            
            st.session_state.final_state = graph_engine.invoke(initial_state)
            st.success("Workflow Completed!")

    
    # DISPLAYING THE REAL OUTPUTS
    
    result = st.session_state.final_state
    
    if selected_module == "📐 Architecture":
        st.markdown("### 📐 Architecture Design")
        st.markdown("**Generated Plan from Architect:**")
        
        st.write(result.get("architecture_plan", "No plan generated."))
        
    elif selected_module == "💻 Code":
        st.markdown("### 💻 Generated Source Code")
        st.markdown("**Python Code from Developer:**")
        
        st.code(result.get("generated_code", ""), language="python")

    elif selected_module == "🧪 Testing":
        st.markdown("### 🧪 Testing & Validation Logs")
        passed = result.get("test_passed", False)
        
        if passed:
            st.success("✅ All Validations Passed!")
        else:
            st.error("❌ Validations Failed or Reached Max Iterations.")
            
        st.markdown("**Feedback Logs:**")
        
        st.code(result.get("validation_feedback", ""), language="bash")
        
        st.markdown(f"**Total Iterations (Fixes attempted):** {result.get('iterations', 0)}")

else:
    st.markdown("<h3 style='text-align: center; color: #6b7280; margin-top: 100px;'>Awaiting project instructions... <br> Type your idea below! 👇</h3>", unsafe_allow_html=True)
