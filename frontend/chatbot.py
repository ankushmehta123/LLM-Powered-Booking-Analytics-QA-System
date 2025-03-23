import streamlit as st
import requests

st.set_page_config(page_title="Hotel Booking Chatbot", layout="wide")

st.title("🏨 Hotel Booking Q&A Chatbot")

st.write("Ask me anything about hotel bookings!")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your question...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to FastAPI backend
    response = requests.post("http://127.0.0.1:8000/ask", json={"query": user_input})
    bot_response = response.json().get("answer", "Error processing request.")

    # Display bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
