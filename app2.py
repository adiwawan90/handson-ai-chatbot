# jalankan file dengan perintah streamlit run <nama file> kasus kita jalankan streamlit run app2.py
import getpass
import os
from inspect import markcoroutinefunction

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

st.title("My Chatbot")
st.write("This is app 2")
# is_clicked = st.button("Click me")
# if is_clicked:
#   st.markdown("You clicked the button")

# if is_clicked:
#   st.write("You clicked the button")

# pertama kali inisialisasi session state API key kosong 
if "api_key" not in st.session_state:
  st.session_state["api_key"] = ""

# Menampilkan input API key
if st.session_state["api_key"] == "":
  st.write("Please enter your API Key")
  input_api_key = st.text_input("Enter your API Key: ", type="password")
  submit_key = st.button("Submit key")
  # Jika tombol submit key di klik maka API key di simpan di session state
  if submit_key:
    st.session_state["api_key"] = input_api_key
  if st.session_state["api_key"] != "":
    st.rerun()
  # Jangan menampilkan lainnya jika tombol submit key belum di klik
  st.stop()

# dari line ini kebawah akan ditampilkan jika API key sudah tersimpan / sudah ada

# Memanggil API key
os.environ["GOOGLE_API_KEY"] = st.session_state["api_key"]
os.environ["GROQ_API_KEY"] = st.session_state["api_key"]

# Bikin client LLM
client = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# client = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

# Inisialisasi chat history dengan system message untuk pertama kali
if "chat_history" not in st.session_state:
  st.session_state["chat_history"] = []

# Display chat history bubble sampai sekarang
for chat in st.session_state["chat_history"]:
  if isinstance(chat, HumanMessage):
    role = "human"
  else:
    role = "ai"
  with st.chat_message(role):
    st.write(chat.content)

# Minta input chat dari user
user_input = st.chat_input("Chat here...")
if not user_input:
  st.stop()

# Tambahkan input user ke history, dan langsung tampilkan di bubble
st.session_state["chat_history"].append(HumanMessage(user_input))
with st.chat_message("human"):
  st.markdown(st.session_state["chat_history"][-1].content)

# Jalankan LLM, dan rerun semuanya agar output LLM masuk ke bubble
response = client.invoke(st.session_state["chat_history"])
st.session_state["chat_history"].append(AIMessage(response.content))
with st.chat_message("assistant"):
  st.write(response.content)

