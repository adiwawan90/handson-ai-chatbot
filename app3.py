# jalankan file dengan perintah streamlit run <nama file> kasus kita jalankan streamlit run app2.py
import getpass
import os
from inspect import markcoroutinefunction

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key
os.environ["GROQ_API_KEY"] = api_key

st.title("My Chatbot")
st.write("This is app final project")

# Taampilkan input API KEY jika Key blm ada
if os.environ.get("GOOGLE_API_KEY") is None and os.environ.get("GROQ_API_KEY") is None:
  input_api_key = st.text_input("Enter your API Key: ", type="password")
  submit_key= st.button("Submit key")

# Jika tombol submit key di klik maka API key di simpan di session state
  if submit_key:
    os.environ["GOOGLE_API_KEY"] = input_api_key
    os.environ["GROQ_API_KEY"] = input_api_key
  if st.session_state["api_key"] != "":
    st.rerun()
  # Jangan menampilkan content selanjutnya sebelum api key diisi
  st.stop()

# Dari sini akan ditampilkan jika API key sudah diisi

client = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# client = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

# Inisialisasi chat history dengan system message untuk pertama kali
if "chat_history" not in st.session_state:
  st.session_state["chat_history"] = []

# Display chat history bubble
for chat in st.session_state["chat_history"]:
  if isinstance(chat, HumanMessage):
    role = "human"
  else:
    role = "ai"
  with st.chat_message(role):
    st.markdown(chat.content)

# Minta input chat dari user
user_input = st.chat_input("Chat here...")
if not user_input:
  st.stop()

# Tampilkan user input ke history dan simpan di session state
st.session_state["chat_history"].append(HumanMessage(user_input))
with st.chat_message("human"):
  st.markdown(st.session_state["chat_history"][-1].content)

# Menjalankan LLM, dan rerun semua agar output ditampilkan di bubble
response = client.invoke(st.session_state["chat_history"])
st.session_state["chat_history"].append(AIMessage(response.content))
with st.chat_message("assistant"):
  st.markdown(response.content)