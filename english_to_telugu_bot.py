import argparse
import importlib.util
import sys

LANGUAGES = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ar": "Arabic",
}

COMMON_WORDS = {
    "hello": {"te": "నమస్తే", "hi": "नमस्ते", "ta": "வணக்கம்", "kn": "ನಮಸ್ಕಾರ", "ml": "നമസ്കാരം", "bn": "নমস্কার", "mr": "नमस्कार", "gu": "નમસ્તે", "pa": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ur": "سلام", "es": "hola", "fr": "bonjour", "de": "hallo", "ar": "مرحبًا"},
    "welcome": {"te": "స్వాగతం", "hi": "स्वागत", "ta": "வரவேற்கிறோம்", "kn": "ಸ್ವಾಗತ", "ml": "സ്വാഗതം", "bn": "স্বাগতম", "mr": "स्वागत", "gu": "સ્વાગત", "pa": "ਆਪਕਾ ਸੁਆਗਤ", "ur": "خوش آمدید", "es": "bienvenido", "fr": "bienvenue", "de": "willkommen", "ar": "مرحبًا"},
    "thank": {"te": "ధన్యవాదాలు", "hi": "धन्यवाद", "ta": "நன்றி", "kn": "ಥ್ಯಾಂಕ್ಸ್", "ml": "നന്ദി", "bn": "ধন্যবাদ", "mr": "धन्याबाद", "gu": "આભાર", "pa": "ਧੰਨਵਾਦ", "ur": "شکریہ", "es": "gracias", "fr": "merci", "de": "danke", "ar": "شكرًا"},
    "you": {"te": "మీరు", "hi": "आप", "ta": "நீங்கள்", "kn": "ನೀವು", "ml": "നിങ്ങൾ", "bn": "আপনি", "mr": "आपण", "gu": "તમે", "pa": "ਤੁਸੀ", "ur": "آپ", "es": "usted", "fr": "vous", "de": "du", "ar": "أنت"},
    "good": {"te": "మంచి", "hi": "अच्छा", "ta": "நல்ல", "kn": "ಒಳ್ಳೆಯ", "ml": "നല്ല", "bn": "ভাল", "mr": "चांगले", "gu": "સારું", "pa": "ਵਧੀਆ", "ur": "اچھا", "es": "bueno", "fr": "bon", "de": "gut", "ar": "جيد"},
    "morning": {"te": "ఉదయం", "hi": "सुबह", "ta": "காலை", "kn": "ಬೆಳಿಗ್ಗೆ", "ml": "പ്രഭാതം", "bn": "সকাল", "mr": "सकाळ", "gu": "સવાર", "pa": "ਸਵੇਰ", "ur": "صبح", "es": "mañana", "fr": "matin", "de": "morgen", "ar": "صباحًا"},
    "evening": {"te": "సాయంత్రం", "hi": "शाम", "ta": "மாலை", "kn": "ಸಂಜೆ", "ml": "സന്ധ്യ", "bn": "সন্ধ্যা", "mr": "संध्याकाळ", "gu": "સાંજ", "pa": "ਸ਼ਾਮ", "ur": "شام", "es": "tarde", "fr": "soirée", "de": "abend", "ar": "مساءً"},
    "night": {"te": "రాత్రి", "hi": "रात", "ta": "இரவு", "kn": "ರಾತ್ರಿ", "ml": "രാത്രി", "bn": "রাত", "mr": "रात", "gu": "રાત્રિ", "pa": "ਰਾਤ", "ur": "رات", "es": "noche", "fr": "nuit", "de": "nacht", "ar": "ليلًا"},
    "friend": {"te": "స్నేహితుడు", "hi": "दोस्त", "ta": "நண்பர்", "kn": "ಸ್ನೇಹಿತ", "ml": "സുഹൃത്ത്", "bn": "বন্ধু", "mr": "मित्र", "gu": "મિત્ર", "pa": "ਦੋਸਤ", "ur": "دوست", "es": "amigo", "fr": "ami", "de": "freund", "ar": "صديق"},
    "home": {"te": "ఇల్లు", "hi": "घर", "ta": "வீடு", "kn": "ಮನೆ", "ml": "വീട്", "bn": "বাড়ি", "mr": "घर", "gu": "ઘર", "pa": "ਘਰ", "ur": "گھر", "es": "hogar", "fr": "maison", "de": "haus", "ar": "بيت"},
    "water": {"te": "నీరు", "hi": "पानी", "ta": "தண்ணீர்", "kn": "ನೀರು", "ml": "വെള്ളം", "bn": "পানি", "mr": "पाणी", "gu": "પાણી", "pa": "ਪਾਣੀ", "ur": "پانی", "es": "agua", "fr": "eau", "de": "wasser", "ar": "ماء"},
    "food": {"te": "ఆహారం", "hi": "खाना", "ta": "உணவு", "kn": "ಆಹಾರ", "ml": "ഭക്ഷണം", "bn": "খাবার", "mr": "अन्न", "gu": "ખોરાક", "pa": "ਭੋਜਨ", "ur": "کھانا", "es": "comida", "fr": "nourriture", "de": "essen", "ar": "طعام"},
    "love": {"te": "ప్రేమ", "hi": "प्यार", "ta": "அன்பு", "kn": "ಪ್ರೀತಿ", "ml": "സ്നേഹം", "bn": "প্রেম", "mr": "प्रेम", "gu": "પ્રેમ", "pa": "ਪਿਆਰ", "ur": "محبت", "es": "amor", "fr": "amour", "de": "liebe", "ar": "حب"},
    "happy": {"te": "సంతోషంగా", "hi": "खुश", "ta": "மகிழ்ச்சி", "kn": "ಸಂತೋಷ", "ml": "സന്തോഷം", "bn": "খুশি", "mr": "आनंदी", "gu": "ખુશ", "pa": "ਖੁਸ਼ੀ", "ur": "خوش", "es": "feliz", "fr": "heureux", "de": "glücklich", "ar": "سعيد"},
    "book": {"te": "పుస్తకం", "hi": "किताब", "ta": "புத்தகம்", "kn": "ಪುಸ್ತಕ", "ml": "പുസ്തകം", "bn": "বই", "mr": "पुस्तक", "gu": "પુસ્તક", "pa": "ਕਿਤਾਬ", "ur": "کتاب", "es": "libro", "fr": "livre", "de": "buch", "ar": "كتاب"},
    "computer": {"te": "కంప్యూటర్", "hi": "कंप्यूटर", "ta": "கணினி", "kn": "ಕಂಪ್ಯೂಟರ್", "ml": "കമ്പ്യൂട്ടർ", "bn": "কম্পিউটার", "mr": "कंप्युटर", "gu": "કમ્પ્યુટર", "pa": "ਕੰਪਿਊਟਰ", "ur": "کمپیوٹر", "es": "computadora", "fr": "ordinateur", "de": "computer", "ar": "حاسوب"},
    "phone": {"te": "ఫోన్", "hi": "फोन", "ta": "தொலைபேசி", "kn": "ಫೋನ್", "ml": "ഫോൺ", "bn": "ফোন", "mr": "फोन", "gu": "ફોન", "pa": "ਫ਼ੋਨ", "ur": "فون", "es": "teléfono", "fr": "téléphone", "de": "telefon", "ar": "هاتف"},
}

PHRASES = {
    "how are you": {"te": "మీరు ఎలా ఉన్నారు", "hi": "आप कैसे हैं", "ta": "நீங்கள் எப்படி இருக்கிறீர்கள்", "kn": "ನೀವು ಹೇಗಿದ್ದೀರಿ", "ml": "നിങ്ങൾ എങ്ങനെയുണ്ട്", "bn": "আপনি কেমন আছেন", "mr": "आपण कसे आहात", "gu": "તમે څنګه છો", "pa": "ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ", "ur": "آپ کیسے ہیں", "es": "cómo estás", "fr": "comment ça va", "de": "wie geht es dir", "ar": "كيف حالك؟"},
    "what is your name": {"te": "మీ పేరు ఏమిటి", "hi": "आपका नाम क्या है", "ta": "உங்கள் பெயர் என்ன", "kn": "ನಿಮ್ಮ ಹೆಸರು ಏನು", "ml": "നിങ്ങളുടെ പേര് എന്താണ്", "bn": "আপনার নাম কী", "mr": "तुमचे नाव काय", "gu": "તમારું નામ શું છે", "pa": "ਤੁਹਾਡਾ ਨਾਮ ਕੀ ਹੈ", "ur": "آپ کا نام کیا ہے", "es": "cuál es tu nombre", "fr": "comment vous appelez-vous", "de": "wie heißt du", "ar": "ما اسمك؟"},
    "my name is": {"te": "నా పేరు", "hi": "मेरा नाम", "ta": "என் பெயர்", "kn": "ನನ್ನ ಹೆಸರು", "ml": "എന്റെ പേര്", "bn": "আমার নাম", "mr": "माझे नाव", "gu": "મારું નામ", "pa": "ਮੇਰਾ ਨਾਮ", "ur": "میرا نام", "es": "mi nombre es", "fr": "je m'appelle", "de": "ich heiße", "ar": "اسمي"},
    "good morning": {"te": "శుభోదయం", "hi": "सुप्रभात", "ta": "காலை வணக்கம்", "kn": "ಶುಭೋದಯ", "ml": "ശുഭപ്രഭാതം", "bn": "শুভ সকাল", "mr": "सुस्वागतम", "gu": "સુપ્રભાત", "pa": "ਸੁਭ ਸਵੇਰ", "ur": "صبح بخیر", "es": "buenos días", "fr": "bonjour", "de": "guten morgen", "ar": "صباح الخير"},
    "thank you": {"te": "ధన్యవాదాలు", "hi": "धन्यवाद", "ta": "நன்றி", "kn": "ಧನ್ಯವಾದಗಳು", "ml": "നന്ദി", "bn": "ধন্যবাদ", "mr": "धन्यवाद", "gu": "આભાર", "pa": "ਧੰਨਵਾਦ", "ur": "شکریہ", "es": "gracias", "fr": "merci", "de": "danke", "ar": "شكرًا"},
    "i love you": {"te": "నేను మీను ప్రేమిస్తున్నాను", "hi": "मैं तुमसे प्यार करता हूँ", "ta": "நான் உன்னை காதலிக்கிறேன்", "kn": "ನಾನು ನಿನ್ನನ್ನು ಪ್ರೀತಿಸುತ್ತೇನೆ", "ml": "ഞാൻ നിന്നെ സ്നേഹിക്കുന്നു", "bn": "আমি তোমাকে ভালোবাসি", "mr": "मी तुझ्यावर प्रेम करतो", "gu": "હું તને love કરું છું", "pa": "ਮੈਂ ਤੁਹਾਨੂੰ ਪਿਆਰ ਕਰਦਾ ਹਾਂ", "ur": "میں تم سے محبت کرتا ہوں", "es": "te quiero", "fr": "je t'aime", "de": "ich liebe dich", "ar": "أنا أحبك"},
}


def translate_with_dictionary(text, source="en", target="te"):
    cleaned = text.strip()
    if not cleaned:
        return ""

    lower_text = cleaned.lower()
    for phrase, translations in PHRASES.items():
        if phrase in lower_text:
            return translations.get(target, cleaned)

    words = cleaned.split()
    translated_words = []
    for word in words:
        cleaned_word = word.strip(".,!?;:'\"()[]{}")
        if not cleaned_word:
            continue
        translation_entry = COMMON_WORDS.get(cleaned_word.lower())
        if translation_entry and target in translation_entry:
            translated_words.append(translation_entry[target])
        else:
            translated_words.append(cleaned_word)
    return " ".join(translated_words)


def translate_text(text, source="en", target="te"):
    if not text or not text.strip():
        return ""
    return translate_with_dictionary(text, source=source, target=target)


def speak_text(text, language="te"):
    if not text.strip():
        return
    if importlib.util.find_spec("pyttsx3") is None:
        print("Voice output is not available yet. Install pyttsx3 to enable speech output.")
        return

    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
    except Exception as exc:
        print(f"Speech output failed: {exc}")


def listen_for_voice():
    if importlib.util.find_spec("speech_recognition") is None:
        print("Voice input is not available yet. Install SpeechRecognition and pyaudio to enable microphone input.")
        return ""

    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... speak now")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        print(f"Heard: {text}")
        return text
    except Exception as exc:
        print(f"Voice input failed: {exc}")
        return ""


def run_chatbot(source="en", target="te"):
    print("Multilingual Voice Translator")
    print("Supported languages:")
    for code, name in LANGUAGES.items():
        print(f"- {code}: {name}")
    print("Type 'exit' to quit")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Goodbye!")
            break

        translated = translate_text(user_input, source=source, target=target)
        print(f"Bot: {translated}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text between languages")
    parser.add_argument("text", nargs="?", default="", help="Text to translate")
    parser.add_argument("--source", default="en", help="Source language code")
    parser.add_argument("--target", default="te", help="Target language code")
    parser.add_argument("--voice", action="store_true", help="Speak the translated text")
    parser.add_argument("--listen", action="store_true", help="Listen to microphone input")
    args = parser.parse_args()

    if args.listen:
        text = listen_for_voice()
    elif args.text:
        text = args.text
    else:
        run_chatbot(source=args.source, target=args.target)
        sys.exit(0)

    if text:
        translated = translate_text(text, source=args.source, target=args.target)
        print(translated)
        if args.voice:
            speak_text(translated, language=args.target)
