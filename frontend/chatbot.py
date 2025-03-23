import streamlit as st
import requests

st.title("📊 Hotel Booking Analytics Chatbot")

st.write("Ask me anything about hotel revenue trends and cancellations!")

user_input = st.text_input("Type your question here:")

if st.button("Ask"):
    if user_input:
        response = requests.post("http://127.0.0.1:8000/ask", json={"query": user_input})
        
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer found.")
            st.write(f"🤖 Chatbot: {answer}")
        else:
            st.write("❌ Error: Unable to fetch response")
