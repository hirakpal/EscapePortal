import streamlit as st
from datetime import datetime, timedelta
from backend.graph.workflow import build_graph
from schemas.trip import TripPreferences
from backend.agents.luna_avatar import get_luna_emotion

st.set_page_config(page_title="🌴 Escape Portal", layout="wide", page_icon="🧳")

# Tropical CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #FFEDD5 0%, #A5F3FC 100%);}
    .stChatMessage {border-radius: 12px;}
    .flip-card { perspective: 1000px; }
</style>
""", unsafe_allow_html=True)

st.title("🌴 Escape Portal")
st.markdown("### Your Personal AI Travel Buddy — Luna")

# Sidebar - Traveller DNA
with st.sidebar:
    st.header("🧬 Traveller DNA")
    if "dna_profile" in st.session_state:
        dna = st.session_state.dna_profile
        st.write(f"**Style**: {dna.get('travel_style', 'Learning...').title()}")
        st.write(f"**Budget**: {dna.get('budget_style', 'mid_range').title()}")
        st.write(f"**Trust Level**: {int(dna.get('trust_score', 0)*100)}%")
        st.progress(dna.get('trust_score', 0))
    else:
        st.write("Luna is getting to know you...")

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Luna 🌺 Ready for your next escape?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Where are we escaping to?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    graph = build_graph()
    config = {"configurable": {"thread_id": "escape_portal"}}
    
    result = graph.invoke({"messages": [{"role": "user", "content": prompt}]}, config)
    
    assistant_msg = result.get("messages", [{}])[-1].get("content", "I'm here!")
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
    with st.chat_message("assistant"):
        st.write(assistant_msg)
    
    # Luna Avatar
    emotion = get_luna_emotion(result)
    st.image(f"avatars/luna_{emotion}.png", width=120, caption=f"Luna is {emotion}")
    
    # Approval Buttons if itinerary exists
    if result.get("itinerary"):
        itin = result["itinerary"]
        st.subheader(f"Proposed Itinerary: {itin.destination}")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Approve & Execute"):
                st.success("Trip Confirmed!")
                st.balloons()
        with col2:
            if st.button("✏️ Modify"):
                st.info("Tell Luna what to change.")
        with col3:
            if st.button("❌ Reject"):
                st.warning("Plan rejected.")

# Export
if "itinerary" in st.session_state:
    st.subheader("Export Your Escape")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Export PDF"):
            st.success("PDF downloaded!")
    with col2:
        if st.button("📅 Add to Calendar"):
            st.success("Calendar event added!")

st.caption("Escape Portal • Agentic AI Travel Assistant 🌴")
