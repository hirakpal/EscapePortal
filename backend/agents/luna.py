from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

def luna_chat_node(state):
    """Luna - the friendly, emotional travel buddy"""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.8)
    
    last_msg = state["messages"][-1]["content"] if state["messages"] else "Hello"
    
    prompt = f"""You are Luna, a cheerful travel sprite and user's best travel buddy.
    You have a playful, warm personality. Use emojis.
    User said: {last_msg}
    
    Respond naturally and helpfully. Ask clarifying questions if needed."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "messages": [AIMessage(content=response.content)],
        "next": "router"  # Loop back to router after response
    }
