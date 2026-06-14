## 1. Apa itu Chatbot AI?
 
Chatbot AI adalah program komputer yang bisa **berkomunikasi dengan manusia menggunakan bahasa alami** (bahasa sehari-hari), bukan perintah kode.
 
Berbeda dengan chatbot lama yang hanya mencocokkan kata kunci, chatbot berbasis AI modern menggunakan **Large Language Model (LLM)** — model bahasa yang sudah dilatih dengan miliaran teks sehingga bisa memahami konteks percakapan.
 
### Cara Kerja Sederhana
 
```
Pengguna ketik pesan
        ↓
Pesan dikirim ke LLM (misal: Gemini / GPT)
        ↓
LLM memproses + memahami konteks
        ↓
LLM menghasilkan respons yang relevan
        ↓
Respons ditampilkan ke pengguna
```
 
### Contoh Penggunaan Chatbot AI
 
| Use Case | Contoh |
|---|---|
| Customer Service | Bot toko, bank, e-commerce |
| Edukasi | Tutor belajar, kuis interaktif |
| Produktivitas | Asisten notulen, ringkasan dokumen |
| Kesehatan | Cek gejala awal, pengingat obat |
| Hiburan | Cerita interaktif, teman ngobrol |
 
---
 
## 2. Teknologi yang Digunakan
 
### Stack Utama
 
| Teknologi | Fungsi | Keterangan |
|---|---|---|
| **Python** | Bahasa pemrograman utama | Versi 3.9+ |
| **Streamlit** | Membuat tampilan web chatbot | Mudah, no HTML/CSS wajib |
| **LangChain** | Menghubungkan kode ke LLM | Framework AI populer |
| **Gemini / Groq** | Model AI (otak chatbot) | Butuh API key |
| **python-dotenv** | Menyimpan API key dengan aman | Jangan hardcode di kode! |
 
### Diagram Arsitektur
 
```
┌─────────────┐     HTTP Request     ┌──────────────────┐
│   Streamlit │ ──────────────────→  │  LangChain Layer │
│  (Tampilan) │                      │  (Penghubung)    │
└─────────────┘ ←──────────────────  └──────────────────┘
                  Streaming Response          │
                                             ↓
                                    ┌──────────────────┐
                                    │   LLM API        │
                                    │ (Gemini / Groq)  │
                                    └──────────────────┘
```
 
