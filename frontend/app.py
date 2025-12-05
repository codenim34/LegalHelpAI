import streamlit as st
import requests
import os

# API Configuration
API_URL = "http://localhost:8000" # Points to src.api.main:app

st.set_page_config(page_title="Legal AI Doc Assistant", layout="wide")

st.title("⚖️ Legal AI Doc Assistant")
st.markdown("### Your AI Advocate & Legal Advisor")

# Sidebar for configuration and file upload
with st.sidebar:
    st.header("Configuration")
    # API Key is now handled by the backend, but we might want to pass it or keep it there.
    # For now, let's assume the backend has the key from .env
    
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or Images", 
        accept_multiple_files=True, 
        type=["pdf", "docx", "png", "jpg", "jpeg", "webp"]
    )
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Uploading and processing..."):
                try:
                    files = [("files", (file.name, file, file.type)) for file in uploaded_files]
                    response = requests.post(f"{API_URL}/ingest", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ Successfully processed {data['total_files']} file(s): {', '.join(data['files_ingested'])}")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {e}")
        else:
            st.warning("Please upload files first.")

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask for legal advice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            response = requests.post(f"{API_URL}/query", json={"query": prompt})
            if response.status_code == 200:
                data = response.json()
                bot_response = data["response"]
                # Append sources if available
                if data.get("sources"):
                    bot_response += "\n\n**Sources:**\n" + "\n".join([f"- {s}" for s in data["sources"]])
            else:
                bot_response = "Error: Could not get response from API."
        except Exception as e:
            bot_response = f"Error: Failed to connect to API. Is it running? ({e})"
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
