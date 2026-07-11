import streamlit as st
from datetime import datetime, timedelta
from schemas.trip import TripPreferences
from graph.workflow import build_graph
import random

st.set_page_config(page_title="🌴 Escape Portal ", layout="wide")

# ... (keep your tropical CSS)

st.title("🌴 Escape Portal")
st.markdown("### Agentic AI Travel Experience – Powered by 2026 Patterns")

# Enhanced Chat with Multi-Agent + Memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Luna. Tell me your dream escape and watch the magic happen ✨"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Where are we escaping?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Agentic Response (simulated multi-agent)
    with st.chat_message("assistant"):
        st.write("Luna is consulting the team...")
        # Trigger LangGraph multi-agent workflow
        prefs = TripPreferences(destination=prompt[:50], start_date=datetime.now(), end_date=datetime.now()+timedelta(days=7), budget=50000)
        graph = build_graph()
        result = graph.invoke({"preferences": prefs})
        
        response = f"Team assembled! Here's a personalized escape plan for {prompt}."
        st.write(response)
        
        # Show enhanced interactive cards (Agentic RAG style)
        st.subheader("🌟 Agent-Curated Escapes")
        # ... (your flip card code enhanced with more dynamic data)

# Sidebar + Monitoring (HITL)
# ... 

st.caption("Escape Portal • 2026 AI Patterns Applied • Luna is learning from you 🌺")
