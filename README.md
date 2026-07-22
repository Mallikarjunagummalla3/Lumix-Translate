# 🌐 LumixTranslate - Premium AI Multilingual Translator

[![Open Live Website](https://img.shields.io/badge/🚀_Open_Live_Website-Click_Here-6366f1?style=for-the-badge&logo=github)](https://mallikarjunagummalla3.github.io/Lumix-Translate/)
![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Framework-Flask-black)

A modern, fast, and feature-rich AI-powered multilingual web translator and text-to-speech suite built with Python (Flask), HTML5, and JavaScript.

---

## 🔗 Live Web Link & Access

- 🌐 **Permanent Live Website**: **[https://mallikarjunagummalla3.github.io/Lumix-Translate/](https://mallikarjunagummalla3.github.io/Lumix-Translate/)** *(Works anytime from any browser/device!)*
- 💻 **Local Server**: `http://localhost:5000` *(Requires running `python app.py` on your machine)*
- 🐙 **GitHub Repository**: [https://github.com/Mallikarjunagummalla3/Lumix-Translate](https://github.com/Mallikarjunagummalla3/Lumix-Translate)

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