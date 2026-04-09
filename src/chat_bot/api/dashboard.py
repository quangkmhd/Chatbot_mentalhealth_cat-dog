import streamlit as st
from src.chat_bot.models.vector_db import VectorDBManager
from src.chat_bot.core.chat_logic import ChatManager
from src.chat_bot.utils.logging import app_logger

@st.cache_resource
def get_managers():
    return VectorDBManager(), ChatManager()

def main():
    st.set_page_config(page_title="Pet Health Assistant", layout="wide")
    st.title("📚 Pet Health Assistant Dashboard")
    st.caption("Professional AI assistance for your pets")

    db_manager, chat_manager = get_managers()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hỏi về sức khỏe thú cưng..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.status("Searching documentation...", expanded=False):
            context = db_manager.search(prompt)
            st.write("Relevant information found.")

        with st.chat_message("assistant"):
            response = chat_manager.get_response(st.session_state.messages, context, "groq")
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
