# import os
# from dotenv import load_dotenv
# # Naya import: Google Generative AI ke liye
# from langchain_google_genai import ChatGoogleGenerativeAI 
# from langchain_core.messages import SystemMessage, HumanMessage
# from backend.state import AgentState

# # Yeh command .env file se GOOGLE_API_KEY load karegi
# load_dotenv() 

# # Ab hum OpenAI ki jagah Gemini (Google) ka model use kar rahe hain
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)






import os
import json
import streamlit as st
from dotenv import load_dotenv

# 1. Google ki jagah OpenAI ka import
from langchain_openai import ChatOpenAI 
from langchain_core.messages import SystemMessage, HumanMessage
from backend.state import AgentState, DeveloperOutput

# Local testing ke liye .env load karein
load_dotenv() 

# 2. OpenAI API Key ko Streamlit Secrets se load karein
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Agar key nahi milti toh error throw karein
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("API Key nahi mili! Streamlit secrets ya .env check karein.")

# 3. LLM Initialization (ChatGPT model set karein)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ==========================================
# 📐 AGENT 1: THE ARCHITECT
# ==========================================
def architect_node(state: AgentState):
    user_prompt = state.get("user_prompt", "")
    
    # System Prompt: Architect ko uski duty samjhana
    sys_msg = SystemMessage(content="""
    You are an expert Software Architect. 
    Analyze the user's project idea.
    Design a clean folder structure and define the necessary Pydantic schemas.
    Keep it modular and follow top-tier software engineering practices.
    """)
    
    hum_msg = HumanMessage(content=f"Project Idea: {user_prompt}")
    
    # LLM ko call karna
    response = llm.invoke([sys_msg, hum_msg])
    
    # State update karna (Sirf architecture_plan update hoga)
    return {"architecture_plan": response.content}

# ==========================================
# 💻 AGENT 2: THE DEVELOPER
# ==========================================
def developer_node(state: AgentState):
    user_prompt = state.get("user_prompt", "")
    plan = state.get("architecture_plan", "")
    feedback = state.get("validation_feedback", "")
    
    sys_msg = SystemMessage(content="""
    You are an Expert Python FastAPI Developer. 
    Write clean, production-ready code based on the Architect's plan.
    If the Tester provides error feedback, YOU MUST fix your previous code based on those errors.
    Output ONLY Python code, no markdown explanations.
    """)
    
    hum_msg = HumanMessage(content=f"""
    Project Idea: {user_prompt}
    Architecture Plan: {plan}
    Tester Feedback (if any): {feedback}
    """)
    
    response = llm.invoke([sys_msg, hum_msg])
    
    # State update karna (Generated code save hoga)
    return {"generated_code": response.content}

# ==========================================
# 🧪 AGENT 3: THE TESTER
# ==========================================
def tester_node(state: AgentState):
    code = state.get("generated_code", "")
    current_iterations = state.get("iterations", 0)
    
    sys_msg = SystemMessage(content="""
    You are a strict QA Tester. 
    Review the provided FastAPI and Pydantic code. Look for missing fields, syntax errors, or logic flaws. 
    If the code is 100% perfect, reply EXACTLY with the word 'PASSED'. 
    If there are errors, explain them clearly so the Developer can fix them.
    """)
    
    hum_msg = HumanMessage(content=f"Code to test:\n{code}")
    
    response = llm.invoke([sys_msg, hum_msg])
    feedback = response.content
    
    # Agar code paas ho jaye
    if "PASSED" in feedback:
        return {
            "test_passed": True, 
            "validation_feedback": "All validations passed successfully.",
            "iterations": current_iterations + 1
        }
    # Agar code fail ho jaye
    else:
        return {
            "test_passed": False, 
            "validation_feedback": feedback,
            "iterations": current_iterations + 1
        }
