# 🌐 LumixTranslate - Premium AI Multilingual Translator

![LumixTranslate](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Framework-Flask-black)

A modern, fast, and feature-rich AI-powered multilingual web translator and text-to-speech suite built with Python (Flask), HTML5, and JavaScript.

---

## 🔗 Project Access & Live Links

> ⚠️ **Note on `localhost:5000`**: `http://localhost:5000` works **only on your local computer** when `app.py` is running. If you click it on GitHub without running `app.py` on your machine, it will show *"can't reach this page" / Connection Refused*.

- 💻 **Local Development**: `http://localhost:5000` (Requires `python app.py` running)
- 🐙 **GitHub Repository**: [https://github.com/Mallikarjunagummalla3/Lumix-Translate](https://github.com/Mallikarjunagummalla3/Lumix-Translate)
- 🚀 **Free Live Hosting Options**: 
  - Deploy to **[Render.com](https://render.com)** for a permanent public link like `https://lumix-translate.onrender.com`
  - Deploy to **[Vercel](https://vercel.com)** or **[PythonAnywhere](https://www.pythonanywhere.com/)**

---

## ✨ Features

- 🌍 **Multi-Language Translation**: Supports auto-detection and translation across 100+ global languages.
- ⚡ **Dual Engine Failover**: Integrated Google GTX and MyMemory translation backends with automatic failover.
- 🗣️ **Text-to-Speech (TTS)**: High-quality audio playback using Google Translate TTS API proxy.
- 🖼️ **Client-Side OCR**: Optical Character Recognition powered by Tesseract.js.
- 🎨 **Modern UI Themes**: Multiple themes (Sunset, Emerald, Gold, Crimson) with glassmorphism aesthetics.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Setup & Run Local Web Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mallikarjunagummalla3/Lumix-Translate.git
   cd Lumix-Translate
   ```

2. **Activate Virtual Environment & Install Dependencies**:
   ```bash
   .venv\Scripts\python.exe -m pip install flask
   ```

3. **Start the Flask Server**:
   ```bash
   .venv\Scripts\python.exe app.py
   ```

4. **Access the Website**:
   Open **[http://localhost:5000](http://localhost:5000)** in your web browser.

---

## 📁 Project Structure

```
.
├── app.py                     # Flask backend server & translation API proxy
├── index.html                 # Frontend single page application
├── english_to_telugu_bot.py   # Specialized English to Telugu translation bot module
└── .gitignore                 # Environment and build exclusion rules
```