# GenAI Workshop - Simple Groq ReAct AI Assistant

A clean, lightweight, single-file Streamlit AI Assistant built with Python, **LangChain**, **LangGraph**, and **Groq**.

This application is powered by Groq's **free tier models** (e.g. `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`) and implements a **ReAct (Reasoning + Acting)** workflow with automatic tool execution (`calculator`, `say_hello`).

---

## ⚡ Features

- 💬 **Clean & Simple UI**: Built with Streamlit chat components (`st.chat_message`, `st.chat_input`).
- 🚀 **Groq Free-Tier Inference**: Default model set to `qwen/qwen3.6-27b` with options for `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, and `gemma2-9b-it`.
- 🛠️ **ReAct Tools**: Autonomously calls math and greeting functions when needed.
- 📦 **Single File Architecture**: All logic (tools, agent setup, Streamlit UI) is consolidated inside [`main.py`](file:///c:/Users/vpman/OneDrive/Desktop/GenAI_Workshop/main.py).

---

## 📁 Project Structure

```
GenAI_Workshop/
├── main.py             # Single entry-point containing tools, agent, and Streamlit UI
├── requirement.txt     # Python dependencies
├── .env                # Environment configuration (GROQ_API_KEY)
└── README.md           # Documentation
```

---

## 🚀 How to Run

### 1. Activate Virtual Environment

```powershell
.\.venv\Scripts\activate
```

### 2. Run the Streamlit Application

```powershell
.venv\Scripts\streamlit.exe run main.py
```

*The application will launch in your browser at `http://localhost:8501`.*

---

## 💬 Usage Examples

- **Math Calculation**: Ask `"What is 154 + 289?"` -> *Invokes `calculator` tool.*
- **Greeting**: Ask `"Say hello to Alex"` -> *Invokes `say_hello` tool.*
- **General Queries**: Ask `"Explain gravity in two sentences."` -> *Responds directly using Groq LLM.*
