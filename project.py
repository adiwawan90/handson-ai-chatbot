import os
import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# os.environ["GOOGLE_API_KEY"] = api_key
# os.environ["GROQ_API_KEY"] = api_key

# Konfigurasi Halaman
st.set_page_config(
  page_title="My Chatbot App",
  page_icon=":robot_face:",
  layout="wide"
)

# CSS custom 
st.markdown("""
<style>
  .main-header {
    background: linear-gradient(90deg, #1e3a5f 0%, #2563eb 100%);
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    color: white;
  }
  .status-badge {
    background: #22c55e;
    color: white;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
  }
  .quick-btn {
    margin: 2px;
  }
  .chat-timestamp {
    font-size: 11px;
    color: #94a3b8;
    margin-top: -8px;
    margin-bottom: 4px;
  }
</style>
  """, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
  <h2 style="margin:0;padding:0">Griya Akbar Customer Support</h2>
  <p style="margin:0;font-size:18px">Toko kelontong yang ramah dan helpful. Mulai dari sembako, perlengkapan rumah tangga, minuman, makanan serta perlengkapan sekolah.</p>
  <p style="margin:0;opacity:0.8;font-size:14px;margin-top:16px">
    Agen virtual siap membantu Anda 24/7 &nbsp;
    <span class="status-badge">● Online</span>
  </p>
</div>
""", unsafe_allow_html=True)

# System prompt
SYSTEM_PROMPT = SystemMessage(content="""
Anda adalah Arina, asisten virtual toko kelontong "Griya Akbar" yang ramah dan helpful.

PERSONA & GAYA BAHASA:
- Gunakan bahasa Indonesia yang santai, hangat, dan akrab seperti pelayan toko tetangga
- Sapa pelanggan dengan "Kak", "Pak", atau "Bu" sesuai konteks
- Boleh sesekali gunakan sapaan khas lokal seperti "Monggo", "Silakan" agar terasa dekat
- Gunakan emoji secukupnya untuk membuat percakapan lebih hidup (🛒 🧴 🍚 ✅ 💰)
- Hindari bahasa yang terlalu formal atau kaku

PRODUK YANG TERSEDIA (domain pengetahuan):
1. SEMBAKO (Sembilan Bahan Pokok)
  - Beras (berbagai merek & ukuran)
  - Gula pasir, gula merah
  - Minyak goreng (curah & kemasan)
  - Tepung terigu, tepung beras
  - Telur ayam & telur bebek
  - Garam, mie instan, ikan kaleng

2. BUMBU & DAPUR
  - Bumbu masak (kemasan & curah)
  - Kecap, saus, sambal botol
  - Santan, kaldu blok
  - Bawang merah, bawang putih, cabai (jika tersedia)

3. MINUMAN & MAKANAN RINGAN
  - Air mineral (gelas, botol, galon)
  - Minuman sachet (kopi, teh, susu)
  - Snack & biskuit
  - Minuman energi & isotonic

4. KEBUTUHAN RUMAH TANGGA
  - Sabun mandi, sabun cuci (bubuk & cair)
  - Sampo, pasta gigi, sikat gigi
  - Deterjen, pewangi pakaian
  - Pembersih lantai, sabun cuci piring
  - Tisu, kantong plastik, kresek
  - Bola lampu, baterai

5. PERLENGKAPAN BAYI (jika ada)
  - Popok bayi, tisu basah
  - Susu formula

6. PERLENGKAPAN SEKOLAH
  - Pensil, penghapus, buku, buku gambar
  - Aksesories, pulpen, crayon, spidol
  - Kertas origami, gasper, seragam, solasi, dasi

KEMAMPUAN ASISTEN:
- Bantu pelanggan cek ketersediaan produk
- Rekomendasikan produk alternatif jika stok habis
- Informasikan promo atau bundling yang sedang berjalan
- Bantu hitung estimasi total belanja sederhana
- Terima & catat pesanan untuk diambil/diantar
- Jawab pertanyaan seputar jam operasional & lokasi toko

ATURAN PENTING:
1. Jika stok produk tidak pasti, sampaikan jujur dan tawarkan untuk dicek dulu
2. JANGAN konfirmasi harga pasti jika tidak ada data — arahkan tanya langsung ke toko
3. Untuk pesanan delivery, tanyakan alamat & waktu pengiriman yang diinginkan
4. Jika ada keluhan (produk rusak, pengiriman terlambat), tunjukkan empati dulu lalu tawarkan solusi
5. Selalu tutup percakapan dengan menawarkan bantuan lain atau ucapan terima kasih

FORMAT RESPONS:
- Singkat dan padat, maksimal 2-3 kalimat untuk pertanyaan sederhana
- Gunakan daftar poin hanya jika pelanggan tanya banyak produk sekaligus
- Jika pelanggan mau pesan, konfirmasi ulang pesanan dengan ringkas sebelum diproses

CONTOH SKENARIO:
- "Stok beras habis" → tawarkan merek/ukuran lain yang tersedia
- "Mau pesan sabun + minyak + beras 5kg" → rangkum pesanan & tanya metode pengambilan
- "Berapa harga gula?" → informasikan harga jika tahu, atau minta cek langsung ke toko
- Pelanggan komplain → empati dulu ("Aduh, maaf ya Kak..."), baru tawarkan solusi
""")

# Inisialisasi chat history dengan system message untuk pertama kali
if "chat_history" not in st.session_state:
  st.session_state["chat_history"] = []

if "timestamps" not in st.session_state:
  st.session_state["timestamps"] = []

if "api_key_google" not in st.session_state:
  st.session_state["api_key_google"] = os.getenv("GOOGLE_API_KEY", "")

if "api_key_groq" not in st.session_state:
  st.session_state.api_key_groq = os.getenv("GROQ_API_KEY", "")

if "model_choice" not in st.session_state:
  st.session_state.model_choice = "Gemini (Google)"

with st.sidebar:
    st.header("⚙️ Konfigurasi")

    # Model selector
    model_choice = st.selectbox(
      "Pilih Model AI",
      ["Gemini (Google)", "LLaMA 4 (Groq)"],
      index=0,
    )
    st.session_state.model_choice = model_choice

    st.divider()

    # Input API key jika belum ada
    st.subheader("🔑 API Keys")

    if not st.session_state.api_key_google:
      google_key = st.text_input("Google API Key", type="password", key="input_google")
      if st.button("Simpan Google Key"):
        st.session_state.api_key_google = google_key
        st.success("Google API Key tersimpan!")
        st.rerun()

    if not st.session_state.api_key_groq:
      groq_key = st.text_input("Groq API Key", type="password", key="input_groq")
      if st.button("Simpan Groq Key"):
        st.session_state.api_key_groq = groq_key
        st.success("Groq API Key tersimpan!")
        st.rerun()

    if st.session_state.model_choice == "Gemini (Google)":
      st.success("✅ Google Key aktif")
    elif st.session_state.model_choice == "LLaMA 4 (Groq)":
      st.success("✅ Groq Key aktif")
    else :
      st.error("❌ API key belum diaktifkan")

    st.divider()

    # Tombol aksi
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
      st.session_state.chat_history = []
      st.session_state.timestamps = []
      st.rerun()

# Client
client = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# ── Quick reply buttons ──────────────────────────────────────────────────────
st.markdown("**💬 Pertanyaan umum:**")
quick_replies = [
    "Apa saja produk sembako yang tersedia?",
    "Apakah ada layanan pesan antar?",
    "Stok beras hari ini ada?",
    "Minyak goreng merek apa yang ada?",
    "Jam buka toko sampai jam berapa?",
    "Ada promo atau diskon hari ini?",
    "Saya mau pesan beberapa barang",
    "Cara pembayaran apa yang diterima?",
]

# Baris pertama: 4 tombol
row1 = quick_replies[:4]
cols1 = st.columns(4)
quick_input = None
for i, q in enumerate(row1):
    with cols1[i]:
        if st.button(q, key=f"quick_{i}", use_container_width=True):
            quick_input = q

# Baris kedua: 4 tombol
row2 = quick_replies[4:]
cols2 = st.columns(4)
for i, q in enumerate(row2):
    with cols2[i]:
        if st.button(q, key=f"quick_{i+4}", use_container_width=True):
            quick_input = q

st.divider()

# Menampilkan riwayat chat -----

for i, chat in enumerate(st.session_state["chat_history"]):
  if isinstance(chat, HumanMessage):
    role = "human"
  else:
    role = "ai"
  with st.chat_message(role):
    st.markdown(chat.content)
    # Tampilkan timestamp jika ada
    if i < len(st.session_state["timestamps"]):
      st.markdown(
        f'<div class="timestamp">{st.session_state["timestamps"][i]}</div>',
        unsafe_allow_html=True
      )

# Minta input chat dari user
user_input = st.chat_input("Ketik pesan Anda di sini...") or quick_input

if not user_input:
  st.stop()

# Tampilkan user input ke history dan simpan di session state
now = datetime.datetime.now().strftime("%H:%M, %d %b %Y")
st.session_state.chat_history.append(HumanMessage(user_input))
st.session_state.timestamps.append(now)


with st.chat_message("human"):
  st.markdown(user_input)
  st.markdown(f'<div class="chat-timestamp">{now}</div>', unsafe_allow_html=True)

# ── Generate & streaming respons AI ─────────────────────────────────────────
messages_to_send = [SYSTEM_PROMPT] + st.session_state.chat_history

try:
  with st.chat_message("assistant"):
    response_placeholder = st.empty()
    full_response = ""

    # Streaming token per token
    for chunk in client.stream(messages_to_send):
      if chunk.content:
        full_response += chunk.content
        response_placeholder.markdown(full_response)  # kursor berkedip

    now_ai = datetime.datetime.now().strftime("%H:%M, %d %b %Y")
    st.markdown(f'<div class="chat-timestamp">Arina · {now_ai}</div>', unsafe_allow_html=True)

  st.session_state.chat_history.append(AIMessage(full_response))
  st.session_state.timestamps.append(f"Arina · {now_ai}")

except Exception as e:
  error_msg = str(e)
  st.error(f"❌ Terjadi kesalahan: {error_msg}")