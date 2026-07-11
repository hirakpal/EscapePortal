from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute
from backend.utils.circuit_breaker import circuit_breaker

def _luna_logic(state):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)
    last_msg = state["messages"][-1].get("content", "Hello")
    prompt = f"You are Luna, cheerful travel buddy. Respond warmly:\nUser: {last_msg}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "messages": [HumanMessage(content=response.content)],
        "next": "router"
    }

def luna_chat_node(state):
    def wrapped():
        return _luna_logic(state)
    return safe_execute(circuit_breaker.call(wrapped), state, "Luna Chat")
