import os
import streamlit as st
from google import genai
import time

# API key
API_KEY = "insert_your_api_key_here"

# Gemini client
client = genai.Client(api_key=API_KEY)

# Streamlit interface
st.set_page_config(page_title="TalkAI", page_icon="🤖")
st.title("💬 TalkAI - A Simple AI Chatbot")
st.write("Chat with TalkAI!")

# chat history and clear flag
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "clear_chat" not in st.session_state:
    st.session_state["clear_chat"] = False

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state["messages"] = []
    st.session_state["clear_chat"] = True

# User input
user_input = st.text_input("You: ")

# Only process input if chat was not just cleared
if user_input and not st.session_state["clear_chat"]:
    bot_reply = ""
    # Retry mechanism for temporary disconnects
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[user_input]  # Gemini expects a list
            )
            bot_reply = response.text
            break
        except Exception as e:
            print("Temporary error, retrying:", e)
            time.sleep(2)

    if bot_reply == "":
        bot_reply = "Sorry, I couldn't connect to the Gemini API. Try again later."

    # Save to chat history
    st.session_state["messages"].append(("You", user_input))
    st.session_state["messages"].append(("TalkAI", bot_reply))

# Reset clear flag after rerun
st.session_state["clear_chat"] = False

# Display chat history
for role, msg in st.session_state["messages"]:
    if role == "You":
        st.markdown(f"👨 You: {msg}")
    else:
        st.markdown(f" 🤖 TalkAI: {msg}")

st.markdown(
    "<div style='text-align: center; color: gray; font-size:12px; margin-top:20px;'>Made by Akshat ☠️</div>",
    unsafe_allow_html=True
)
