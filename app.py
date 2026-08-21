import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

# Load environment variables from .env file
load_dotenv()

# ==========================================
# 1. Tools Definition
# ==========================================
@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers."""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user politely."""
    return f"Hello {name}, I hope you are having a wonderful day!"

tools = [calculator, say_hello]

# ==========================================
# 2. Agent Initialization
# ==========================================
def get_agent(api_key: str, model_name: str = "qwen/qwen3.6-27b"):
    """Creates a LangGraph ReAct agent powered by Groq free tier models."""
    if not api_key:
        raise ValueError("Groq API key is missing. Please provide a valid GROQ_API_KEY.")
    
    model = ChatGroq(
        groq_api_key=api_key,
        model=model_name,
        temperature=0.2
    )
    return create_react_agent(model, tools)

# ==========================================
# 3. Simple Streamlit Application
# ==========================================
def main():
    st.set_page_config(
        page_title="AI Chatbot",
        page_icon="💬",
        layout="centered"
    )

    st.title("💬 Groq AI Assistant")
    st.caption("A clean, simple ReAct Chatbot powered by Groq Free-Tier Models & LangGraph")

    # Sidebar Controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key Config (Securely Hidden)
        env_key = os.getenv("GROQ_API_KEY", "")
        custom_key = st.text_input(
            "Groq API Key (Override)",
            type="password",
            placeholder="Enter custom key if needed...",
            help="If GROQ_API_KEY is set in your .env file, it will be used automatically without revealing your key."
        )
        
        groq_key = custom_key.strip() if custom_key.strip() else env_key
        
        if env_key and not custom_key.strip():
            st.caption("🔒 API Key loaded securely from `.env`")
        elif custom_key.strip():
            st.caption("🟢 Custom API Key active")
        else:
            st.caption("🔴 API Key missing")
        
        # Groq Free Tier Models
        model_name = st.selectbox(
            "Free Tier Model",
            options=[
                "qwen/qwen3.6-27b",
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "gemma2-9b-it"
            ],
            index=0,
            help="Selected free-tier Groq model for fast inference."
        )

        st.divider()
        st.markdown("**Active Tools:**")
        st.markdown("- 🧮 `calculator(a, b)`")
        st.markdown("- 👋 `say_hello(name)`")
        
        st.divider()
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Chat Session History Initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Conversation History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Ask a question or test tools (e.g., 'Add 35 and 92')...")

    if user_input:
        if not groq_key:
            st.error("⚠️ Please enter your Groq API Key in the sidebar or `.env` file.")
            st.stop()

        # Render User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Render Assistant Response Stream
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Prepare Message Payload
            formatted_messages = [
                SystemMessage(content="You are a helpful, accurate, and concise AI assistant.")
            ]
            for m in st.session_state.messages:
                if m["role"] == "user":
                    formatted_messages.append(HumanMessage(content=m["content"]))
                elif m["role"] == "assistant":
                    formatted_messages.append(AIMessage(content=m["content"]))

            try:
                agent = get_agent(api_key=groq_key, model_name=model_name)

                with st.status("Processing...", expanded=False) as status:
                    for chunk in agent.stream({"messages": formatted_messages}):
                        # Check for Tool Invocation
                        if "tools" in chunk and "messages" in chunk["tools"]:
                            for tool_msg in chunk["tools"]["messages"]:
                                st.write(f"🔧 **Tool (`{tool_msg.name}`):** {tool_msg.content}")
                        
                        # Stream Assistant Tokens
                        if "agent" in chunk and "messages" in chunk["agent"]:
                            for agent_msg in chunk["agent"]["messages"]:
                                if agent_msg.content:
                                    full_response += agent_msg.content
                                    response_placeholder.markdown(full_response + "▌")

                    status.update(label="Done", state="complete")

                response_placeholder.markdown(full_response if full_response else "*(No response generated)*")
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as err:
                st.error(f"❌ Error: {err}")

if __name__ == "__main__":
    main()
