import os
import json
import urllib.request
import urllib.parse
from flask import Flask, request, jsonify

app = Flask(__name__)

# Complete list of supported languages
LANGUAGES = {
    "auto": "Auto Detect",
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "he": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish (Kurmanji)",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia (Oriya)",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "tt": "Tatar",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "tk": "Turkmen",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu"
}

def translate_via_google_gtx(text, source, target):
    """
    Call Google's client=gtx endpoint. It's fast, free, and returns multiple translated chunks.
    """
    if not text or not text.strip():
        return ""
    
    # Map 'auto' for Google
    sl = source if source != "auto" else "auto"
    
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={sl}&tl={target}&dt=t&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            translated_chunks = [chunk[0] for chunk in res_data[0] if chunk and chunk[0]]
            return "".join(translated_chunks)
    except Exception as e:
        print(f"[Backend Google GTX Error]: {e}")
        return None

def translate_via_mymemory(text, source, target):
    """
    Fallback to MyMemory API.
    """
    if not text or not text.strip():
        return ""
    
    # Map 'auto' for MyMemory pair
    langpair = f"{source}|{target}" if source != "auto" else f"autodetect|{target}"
    
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={langpair}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if 'responseData' in res_data and 'translatedText' in res_data['responseData']:
                return res_data['responseData']['translatedText']
    except Exception as e:
        print(f"[Backend MyMemory Error]: {e}")
    return None

@app.route("/", methods=["GET"])
def index():
    """Serves the main SPA index.html from workspace root."""
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "index.html file not found in root workspace directory.", 404

@app.route("/api/languages", methods=["GET"])
def get_languages():
    """Returns the list of supported languages."""
    return jsonify(LANGUAGES)

@app.route("/api/translate", methods=["POST"])
def translate():
    """API endpoint to translate text with failover mechanism."""
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    source = data.get("source", "auto").strip()
    target = data.get("target", "en").strip()
    
    if not text:
        return jsonify({"translatedText": "", "success": True})
        
    # Try Google GTX first
    result = translate_via_google_gtx(text, source, target)
    if result is not None:
        return jsonify({"translatedText": result, "success": True, "engine": "google_gtx"})
        
    # Try MyMemory second
    result = translate_via_mymemory(text, source, target)
    if result is not None:
        return jsonify({"translatedText": result, "success": True, "engine": "mymemory"})
        
    # Return error if all engines fail
    return jsonify({
        "translatedText": f"[Offline/Error Fallback] {text}",
        "success": False,
        "error": "All translation engines failed"
    }), 500

@app.route("/api/tts", methods=["GET"])
def text_to_speech():
    """Proxy route to fetch Google Translate TTS MP3 output bypassing CORS/Referer limitations."""
    text = request.args.get("text", "").strip()
    lang = request.args.get("lang", "en").strip()
    if not text:
        return "Text parameter is required", 400
        
    try:
        # Use Google Translate free TTS API endpoint
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://translate.google.com/'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            audio_data = response.read()
            return audio_data, 200, {
                'Content-Type': 'audio/mpeg',
                'Content-Length': str(len(audio_data)),
                'Cache-Control': 'public, max-age=86400'
            }
    except Exception as e:
        print(f"[Backend TTS Proxy Error]: {e}")
        return f"Failed to retrieve TTS audio: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

