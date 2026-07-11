import streamlit as st
from datetime import datetime, timedelta
from backend.graph.workflow import build_graph
from schemas.trip import TripPreferences

st.set_page_config(page_title="🌴 Escape Portal", layout="wide", page_icon="🧳")

# Tropical CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #FFEDD5 0%, #A5F3FC 100%);}
    .stChatMessage {border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("🌴 Escape Portal")
st.markdown("### Talk to Luna — Your Personal Travel Sprite")

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Luna 🌺 Ready for your next escape?"}]

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Where are we going next?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Run LangGraph with Luna Chat Node
    graph = build_graph()
    config = {"configurable": {"thread_id": "escape_portal"}}
    
    inputs = {
        "messages": [{"role": "user", "content": prompt}],
        "dna_profile": {}  # Will be populated by DNA node later
    }
    
    result = graph.invoke(inputs, config)
    
    # Show Luna's response
    if result.get("messages"):
        assistant_msg = result["messages"][-1]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        with st.chat_message("assistant"):
            st.write(assistant_msg)

# Sidebar - Traveller DNA Preview
with st.sidebar:
    st.header("🧬 Traveller DNA")
    st.caption("Luna is learning about you...")
    # Will show profile once DNA node is added

st.caption("Escape Portal • Step-by-step Agentic AI • Luna is online 🌟")
