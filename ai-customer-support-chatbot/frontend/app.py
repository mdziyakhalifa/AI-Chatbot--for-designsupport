import streamlit as st
import requests
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Ziya Digital - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    .st-emotion-cache-1c7n2ka {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1e3d59;
        font-family: 'Inter', sans-serif;
    }
    .source-tag {
        font-size: 0.8rem;
        background-color: #e1f5fe;
        color: #01579b;
        padding: 2px 8px;
        border-radius: 10px;
        margin-right: 5px;
        display: inline-block;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- Backend URL ---
BACKEND_URL = "http://localhost:8000/api/v1"

# --- Sidebar ---
with st.sidebar:
    st.title("Settings & Knowledge")
    st.image("https://via.placeholder.com/150", caption="Ziya Digital Agency")
    
    st.divider()
    
    st.subheader("📁 Upload Knowledge")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT documents", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    
    if st.button("🚀 Process Documents", use_container_width=True):
        if uploaded_files:
            files = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
            with st.spinner("Processing documents and updating vector database..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success("Knowledge base updated!")
                    else:
                        st.error(f"Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
        else:
            st.warning("Please select files first.")

    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        try:
            requests.post(f"{BACKEND_URL}/clear-history")
            st.session_state.messages = []
            st.rerun()
        except:
            st.error("Failed to clear history.")

    st.info("System Status: Online 🟢")

# --- Main App ---
st.title("🤖 AI Customer Support Assistant")
st.markdown("Welcome! I'm the Ziya Digital assistant. Ask me anything about our services, pricing, or company policies.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            st.markdown("---")
            st.caption("Sources:")
            cols = st.columns(len(message["sources"]))
            for i, source in enumerate(message["sources"]):
                st.markdown(f'<span class="source-tag">{os.path.basename(source)}</span>', unsafe_allow_html=True)

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{BACKEND_URL}/query", 
                    json={"question": prompt}
                )
            
            if response.status_code == 200:
                data = response.json()
                full_response = data["answer"]
                sources = data["sources"]
                
                # Simulate streaming effect
                for chunk in full_response.split():
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.02)
                
                message_placeholder.markdown(full_response)
                
                if sources:
                    st.markdown("---")
                    st.caption("Sources:")
                    for source in sources:
                        st.markdown(f'<span class="source-tag">{os.path.basename(source)}</span>', unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response,
                    "sources": sources
                })
            else:
                st.error("Error from backend.")
        except Exception as e:
            st.error(f"Connection Error: {e}")
            st.info("Make sure the FastAPI backend is running on http://localhost:8000")
