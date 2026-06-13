import requests

# ──────────────────────────────────────────────
# Language → system instruction sent to the model
# ──────────────────────────────────────────────
LANGUAGE_INSTRUCTIONS = {
    "English": (
        "You are an emergency medical assistant. "
        "You must answer only in English. "
        "Give clear, calm, step-by-step first-aid guidance."
    ),
    "Telugu": (
        "మీరు ఒక అత్యవసర వైద్య సహాయకుడు. "
        "మీరు తప్పనిసరిగా కేవలం తెలుగు లిపిలో మాత్రమే సమాధానం ఇవ్వాలి. "
        "అన్ని వివరణలు, సూచనలు మరియు సమాచారం తెలుగులో ఉండాలి. "
        "ఆసుపత్రి పేర్లు, మందుల పేర్లు వంటి నిర్దిష్ట వైద్య పదాలు మాత్రమే ఆంగ్లంలో ఉంచవచ్చు. "
        "స్పష్టమైన, శాంతంగా అడుగుల వారీగా ప్రథమ చికిత్స సలహా ఇవ్వండి."
    ),
    "Hindi": (
        "आप एक आपातकालीन चिकित्सा सहायक हैं। "
        "आपको केवल हिंदी (देवनागरी) लिपि में उत्तर देना अनिवार्य है। "
        "सभी स्पष्टीकरण, निर्देश और जानकारी हिंदी में होनी चाहिए। "
        "केवल अस्पताल के नाम, दवाओं के नाम जैसे विशिष्ट चिकित्सा शब्द अंग्रेज़ी में रख सकते हैं। "
        "स्पष्ट, शांत, चरण-दर-चरण प्राथमिक चिकित्सा सलाह दें।"
    ),
}

# ──────────────────────────────────────────────
# Friendly, fully-localised offline error messages
# (shown when Ollama is not running)
# ──────────────────────────────────────────────
OLLAMA_OFFLINE_MSG = {
    "English": (
        "⚠️ **The local AI (Ollama) is not running on your computer.**\n\n"
        "**To fix this:**\n"
        "1. Download Ollama from [https://ollama.com](https://ollama.com)\n"
        "2. Install and open the Ollama application\n"
        "3. Open a terminal and run: `ollama run gemma3:1b`\n"
        "4. Wait until the model is ready, then refresh this page and try again.\n\n"
        "Alternatively, switch the **AI Mode** dropdown above to **BYOK OpenAI** "
        "and enter your OpenAI API key."
    ),
    "Telugu": (
        "⚠️ **మీ కంప్యూటర్‌లో స్థానిక AI సేవ అందుబాటులో లేదు.**\n\n"
        "**పరిష్కారం:**\n"
        "1. [https://ollama.com](https://ollama.com) వెబ్‌సైట్ నుండి Ollama సాఫ్ట్‌వేర్‌ను డౌన్‌లోడ్ చేసుకోండి\n"
        "2. సాఫ్ట్‌వేర్‌ను ఇన్‌స్టాల్ చేసి తెరవండి\n"
        "3. కమాండ్ ప్రాంప్ట్ లేదా టెర్మినల్‌లో ఈ ఆదేశాన్ని అమలు చేయండి: `ollama run gemma3:1b`\n"
        "4. మోడల్ సిద్ధంగా ఉన్నప్పుడు, ఈ పేజీని రిఫ్రెష్ చేసి మళ్ళీ ప్రయత్నించండి.\n\n"
        "లేదా పై **AI మోడ్** ఎంపికను **BYOK OpenAI** కి మార్చి మీ OpenAI API కీని నమోదు చేయండి."
    ),
    "Hindi": (
        "⚠️ **आपके कंप्यूटर पर स्थानीय AI सेवा उपलब्ध नहीं है।**\n\n"
        "**समाधान:**\n"
        "1. [https://ollama.com](https://ollama.com) वेबसाइट से Ollama सॉफ़्टवेयर डाउनलोड करें\n"
        "2. सॉफ़्टवेयर इंस्टॉल करें और खोलें\n"
        "3. कमांड प्रॉम्प्ट या टर्मिनल में यह आदेश चलाएं: `ollama run gemma3:1b`\n"
        "4. जब मॉडल तैयार हो जाए, तो इस पेज को रिफ्रेश करें और दोबारा प्रयास करें।\n\n"
        "या ऊपर दिए **AI मोड** विकल्प को **BYOK OpenAI** में बदलें "
        "और अपनी OpenAI API कुंजी दर्ज करें।"
    ),
}

# ──────────────────────────────────────────────
# Invalid API key messages per language
# ──────────────────────────────────────────────
INVALID_KEY_MSG = {
    "English": "❌ Invalid OpenAI API key. Please check and try again.",
    "Telugu":  "❌ చెల్లని OpenAI API కీ. దయచేసి తనిఖీ చేసి మళ్ళీ ప్రయత్నించండి.",
    "Hindi":   "❌ अमान्य OpenAI API कुंजी। कृपया जांचें और पुनः प्रयास करें।",
}


def ask_ollama(question: str, language: str = "English") -> str:
    """
    Send a question to the local Ollama instance (gemma3:1b).

    Parameters
    ----------
    question : str   – The user's emergency question.
    language : str   – UI language ("English" / "Telugu" / "Hindi").
                       The model is instructed to reply in this language.

    Returns a localised error message if Ollama is not running.
    """
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(
        language, LANGUAGE_INSTRUCTIONS["English"]
    )

    # System instruction prepended so the model knows language + role
    full_prompt = (
        f"[SYSTEM INSTRUCTION]\n{lang_instruction}\n\n"
        f"[USER QUESTION]\n{question}"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:1b",
                "prompt": full_prompt,
                "stream": False,
            },
            timeout=60,
        )

        print("Ollama status:", response.status_code)
        print("Ollama response (preview):", response.text[:300])

        data = response.json()
        return data.get("response", "No response from Ollama")

    except requests.exceptions.ConnectionError:
        # Ollama not running – return a friendly, fully-localised setup guide
        return OLLAMA_OFFLINE_MSG.get(language, OLLAMA_OFFLINE_MSG["English"])

    except Exception as e:
        return f"Error: {str(e)}"


def ask_openai(question: str, api_key: str, language: str = "English") -> str:
    """
    Send a question to OpenAI's Chat Completions API (BYOK mode).

    Parameters
    ----------
    question : str   – The user's emergency question.
    api_key  : str   – User-supplied OpenAI API key.
    language : str   – UI language; the system prompt enforces this language.
    """
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(
        language, LANGUAGE_INSTRUCTIONS["English"]
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": lang_instruction},
            {"role": "user",   "content": question},
        ],
        "max_tokens": 800,
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError:
        if response.status_code == 401:
            return INVALID_KEY_MSG.get(language, INVALID_KEY_MSG["English"])
        return f"OpenAI Error {response.status_code}: {response.text[:200]}"

    except Exception as e:
        return f"Error: {str(e)}"