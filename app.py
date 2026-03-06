import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()  # 🔥 This loads variables from .env file

api_key = os.getenv("GEMINI_API_KEY")
st.title("Gemini Chatbot")


if not api_key:
    st.error("API key not found. Please configure secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"**YOU:** {text}")
    else:
        st.markdown(f"**BOT:** {text}")

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # ✅ FIXED MODEL NAME
            contents=user_input
        )

        bot_reply = response.text if response.text else "No response received."

    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        st.stop()

    st.session_state.messages.append(("bot", bot_reply))
    st.rerun()




