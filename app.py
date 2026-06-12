import streamlit as st
import folium
from streamlit_folium import st_folium
from services.location import get_coordinates
from services.hospitals import get_nearby_hospitals
from services.routes import get_route, traffic_status
from services.ai_assistant import ask_ollama

# -----------------------------------
# CENTRALIZED TRANSLATION DICTIONARY
# -----------------------------------
LANGUAGES = {
    "English": {
        # Hero
        "hero_title": "RapidAid — Get help, faster.",
        "hero_subtitle": "Real-time hospital routing, live traffic intelligence, and one-tap access to emergency services.",
        "hero_badge": "AI Emergency Navigator · Live",

        # Section headings
        "section_location": "📍 Your Location",
        "section_hospitals": "🏥 Nearby Hospitals",
        "section_hospital_list": "📋 Hospital List",
        "section_map": "🗺️ Live Map",
        "section_contacts": "🚨 Emergency Contacts",
        "section_assistant": "🤖 AI Emergency Assistant",

        # Location inputs
        "label_city": "City or area",
        "btn_use_location": "📍  Use Current Location",
        "btn_find_help": "🔍  Find Nearest Help",

        # Hospital table columns
        "col_hospital": "Hospital",
        "col_distance": "Distance",
        "col_eta": "ETA",
        "col_traffic": "Traffic",
        "btn_directions": "Directions",
        "label_top_hospital": "Top Hospital",

        # Map
        "map_destination": "🏥 Destination",

        # Emergency contacts
        "ec_ambulance_label": "Ambulance",
        "ec_ambulance_sub": "24/7 Medical Emergency",
        "ec_police_label": "Police",
        "ec_police_sub": "National Emergency Line",
        "ec_fire_label": "Fire Brigade",
        "ec_fire_sub": "Fire & Rescue Services",

        # AI Assistant
        "label_ai_mode": "Choose AI Mode",
        "label_api_key": "Enter OpenAI API Key",
        "label_question": "Ask an emergency question",
        "placeholder_question": "Example: What should I do before reaching the hospital for chest pain?",
        "btn_get_advice": "Get AI Advice",
        "ai_response_header": "### AI Response",
        "warn_no_question": "Please enter a question.",
        "err_ai": "Error",
        "spinner_ai": "Getting AI advice...",

        # AI language instruction (injected into prompt)
        "ai_lang_instruction": "Answer in English.",

        # Errors / warnings
        "err_location_not_found": "Location not found",
        "msg_selected": "Selected",

        # Footer
        "footer_tagline": "Smart Emergency Route Finder",
        "footer_credit": "Built with ❤️ for safer cities - By: M.Anila, P.Shivani",

        # Language screen
        "lang_screen_title": "Choose Your Language",
        "lang_select_label": "Select Language",
        "btn_continue": "Continue",
    },

    "Telugu": {
        # Hero
        "hero_title": "రాపిడ్ ఎయిడ్ — వేగంగా సహాయం పొందండి.",
        "hero_subtitle": "రియల్-టైమ్ ఆసుపత్రి మార్గం, లైవ్ ట్రాఫిక్ సమాచారం, మరియు అత్యవసర సేవలకు వన్-ట్యాప్ యాక్సెస్.",
        "hero_badge": "AI అత్యవసర నావిగేటర్ · లైవ్",

        # Section headings
        "section_location": "📍 మీ స్థానం",
        "section_hospitals": "🏥 సమీప ఆసుపత్రులు",
        "section_hospital_list": "📋 ఆసుపత్రి జాబితా",
        "section_map": "🗺️ లైవ్ మ్యాప్",
        "section_contacts": "🚨 అత్యవసర సంప్రదింపులు",
        "section_assistant": "🤖 AI అత్యవసర సహాయకుడు",

        # Location inputs
        "label_city": "నగరం లేదా ప్రాంతం",
        "btn_use_location": "📍  ప్రస్తుత స్థానాన్ని ఉపయోగించండి",
        "btn_find_help": "🔍  సమీప సహాయం కనుగొనండి",

        # Hospital table columns
        "col_hospital": "ఆసుపత్రి",
        "col_distance": "దూరం",
        "col_eta": "సమయం",
        "col_traffic": "ట్రాఫిక్",
        "btn_directions": "దిశలు",
        "label_top_hospital": "అగ్రశ్రేణి ఆసుపత్రి",

        # Map
        "map_destination": "🏥 గమ్యస్థానం",

        # Emergency contacts
        "ec_ambulance_label": "అంబులెన్స్",
        "ec_ambulance_sub": "24/7 వైద్య అత్యవసర స్థితి",
        "ec_police_label": "పోలీసు",
        "ec_police_sub": "జాతీయ అత్యవసర లైన్",
        "ec_fire_label": "అగ్నిమాపక దళం",
        "ec_fire_sub": "అగ్నిమాపక & రెస్క్యూ సేవలు",

        # AI Assistant
        "label_ai_mode": "AI మోడ్ ఎంచుకోండి",
        "label_api_key": "OpenAI API కీని నమోదు చేయండి",
        "label_question": "అత్యవసర ప్రశ్న అడగండి",
        "placeholder_question": "ఉదాహరణ: గుండె నొప్పి కోసం ఆసుపత్రికి చేరుకునే ముందు నేను ఏమి చేయాలి?",
        "btn_get_advice": "AI సలహా పొందండి",
        "ai_response_header": "### AI సమాధానం",
        "warn_no_question": "దయచేసి ఒక ప్రశ్న నమోదు చేయండి.",
        "err_ai": "లోపం",
        "spinner_ai": "AI సలహా పొందుతున్నారు...",

        # AI language instruction
        "ai_lang_instruction": "దయచేసి కేవలం తెలుగులో మాత్రమే సమాధానం ఇవ్వండి.",

        # Errors / warnings
        "err_location_not_found": "స్థానం కనుగొనబడలేదు",
        "msg_selected": "ఎంచుకున్నారు",

        # Footer
        "footer_tagline": "స్మార్ట్ అత్యవసర మార్గ అన్వేషకుడు",
        "footer_credit": "సురక్షిత నగరాల కోసం ❤️ తో నిర్మించబడింది - రచయితలు: M.అనిల, P.శివాని",

        # Language screen
        "lang_screen_title": "మీ భాషను ఎంచుకోండి",
        "lang_select_label": "భాష ఎంచుకోండి",
        "btn_continue": "కొనసాగించు",
    },

    "Hindi": {
        # Hero
        "hero_title": "रैपिडएड — जल्दी सहायता पाएं।",
        "hero_subtitle": "रियल-टाइम अस्पताल रूटिंग, लाइव ट्रैफिक इंटेलिजेंस, और आपातकालीन सेवाओं तक वन-टैप एक्सेस।",
        "hero_badge": "AI आपातकालीन नेविगेटर · लाइव",

        # Section headings
        "section_location": "📍 आपका स्थान",
        "section_hospitals": "🏥 पास के अस्पताल",
        "section_hospital_list": "📋 अस्पताल सूची",
        "section_map": "🗺️ लाइव मैप",
        "section_contacts": "🚨 आपातकालीन संपर्क",
        "section_assistant": "🤖 AI आपातकालीन सहायक",

        # Location inputs
        "label_city": "शहर या क्षेत्र",
        "btn_use_location": "📍  वर्तमान स्थान उपयोग करें",
        "btn_find_help": "🔍  नजदीकी सहायता खोजें",

        # Hospital table columns
        "col_hospital": "अस्पताल",
        "col_distance": "दूरी",
        "col_eta": "समय",
        "col_traffic": "ट्रैफिक",
        "btn_directions": "दिशाएं",
        "label_top_hospital": "शीर्ष अस्पताल",

        # Map
        "map_destination": "🏥 गंतव्य",

        # Emergency contacts
        "ec_ambulance_label": "एम्बुलेंस",
        "ec_ambulance_sub": "24/7 चिकित्सा आपातकाल",
        "ec_police_label": "पुलिस",
        "ec_police_sub": "राष्ट्रीय आपातकालीन लाइन",
        "ec_fire_label": "अग्निशमन दल",
        "ec_fire_sub": "अग्निशमन और बचाव सेवाएं",

        # AI Assistant
        "label_ai_mode": "AI मोड चुनें",
        "label_api_key": "OpenAI API कुंजी दर्ज करें",
        "label_question": "आपातकालीन प्रश्न पूछें",
        "placeholder_question": "उदाहरण: सीने में दर्द के लिए अस्पताल पहुंचने से पहले मुझे क्या करना चाहिए?",
        "btn_get_advice": "AI सलाह प्राप्त करें",
        "ai_response_header": "### AI प्रतिक्रिया",
        "warn_no_question": "कृपया एक प्रश्न दर्ज करें।",
        "err_ai": "त्रुटि",
        "spinner_ai": "AI सलाह प्राप्त की जा रही है...",

        # AI language instruction
        "ai_lang_instruction": "कृपया केवल हिंदी में उत्तर दें।",

        # Errors / warnings
        "err_location_not_found": "स्थान नहीं मिला",
        "msg_selected": "चुना गया",

        # Footer
        "footer_tagline": "स्मार्ट आपातकालीन मार्ग खोजक",
        "footer_credit": "सुरक्षित शहरों के लिए ❤️ के साथ बनाया गया - द्वारा: M.अनिला, P.शिवानी",

        # Language screen
        "lang_screen_title": "अपनी भाषा चुनें",
        "lang_select_label": "भाषा चुनें",
        "btn_continue": "जारी रखें",
    },
}


# -----------------------------------
# HELPER FUNCTION
# -----------------------------------
def t(key: str) -> str:
    """Look up a translation key for the active language, falling back to English."""
    lang = st.session_state.get("language", "English")
    return LANGUAGES.get(lang, LANGUAGES["English"]).get(key, LANGUAGES["English"].get(key, key))


# -----------------------------------
# PAGE CONFIG (must be first Streamlit call)
# -----------------------------------
st.set_page_config(
    page_title="RapidAid — AI Emergency Navigator",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------
# LANGUAGE SELECTION SCREEN
# -----------------------------------
if "language" not in st.session_state:
    st.title("Choose Your Language")
    st.subheader("భాష ఎంచుకోండి")
    st.subheader("भाषा चुनें")

    selected_language = st.selectbox(
        "Select Language",
        ["English", "Telugu", "Hindi"]
    )

    if st.button("Continue"):
        st.session_state.language = selected_language
        st.rerun()

    st.stop()

# -----------------------------------
# PREMIUM CUSTOM CSS (unchanged)
# -----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ---------- GLOBAL ---------- */
html, body, [class*="css"], .stApp, .stMarkdown, p, span, div, label {
    font-family: 'Inter', sans-serif !important;
    color: #e6edf7 !important;
}

h1, h2, h3, h4, h5 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.02em !important;
    color: #ffffff !important;
}

/* ---------- BACKGROUND ---------- */
.stApp {
    background:
        radial-gradient(1200px 600px at 10% -10%, rgba(99,102,241,0.25), transparent 60%),
        radial-gradient(900px 500px at 110% 10%, rgba(236,72,153,0.18), transparent 60%),
        radial-gradient(800px 600px at 50% 120%, rgba(34,211,238,0.18), transparent 60%),
        linear-gradient(160deg, #050816 0%, #0b1023 45%, #0a0f1f 100%);
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
    z-index: 0;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1280px !important;
    position: relative;
    z-index: 1;
}

#MainMenu, footer, header [data-testid="stToolbar"] { visibility: hidden; }

/* ---------- HERO ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 38px 40px;
    border-radius: 24px;
    margin-bottom: 28px;
    background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(236,72,153,0.18) 60%, rgba(34,211,238,0.22));
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow:
        0 20px 60px -20px rgba(99,102,241,0.45),
        inset 0 1px 0 rgba(255,255,255,0.08);
}
.hero::after {
    content: "";
    position: absolute;
    top: -50%; right: -20%;
    width: 480px; height: 480px;
    background: radial-gradient(circle, rgba(236,72,153,0.35), transparent 60%);
    filter: blur(40px);
    animation: float 9s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0) translateX(0); }
    50% { transform: translateY(-20px) translateX(15px); }
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a5f3fc !important;
    margin-bottom: 14px;
}
.hero-badge .dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #22d3ee;
    box-shadow: 0 0 0 0 rgba(34,211,238,0.7);
    animation: pulse 1.8s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(34,211,238,0.7); }
    70% { box-shadow: 0 0 0 12px rgba(34,211,238,0); }
    100% { box-shadow: 0 0 0 0 rgba(34,211,238,0); }
}

.hero h1 {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    margin: 0 0 8px 0 !important;
    background: linear-gradient(120deg, #ffffff 0%, #c7d2fe 50%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: rgba(230,237,247,0.75) !important;
    font-size: 1.05rem !important;
    max-width: 620px;
    margin: 0 !important;
}

/* ---------- SECTION HEADERS ---------- */
.section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 18px 0;
    font-size: 1.35rem;
    font-weight: 600;
    color: #fff;
}
.section-title .bar {
    width: 4px; height: 22px;
    border-radius: 4px;
    background: linear-gradient(180deg, #6366f1, #ec4899);
}

/* ---------- GLASS CARDS ---------- */
.glass {
    background: rgba(17, 24, 39, 0.55);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.6);
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
}
.glass:hover {
    transform: translateY(-3px);
    border-color: rgba(99,102,241,0.45);
    box-shadow: 0 18px 50px -12px rgba(99,102,241,0.35);
}

/* ---------- INPUTS ---------- */
[data-testid="stTextInput"] label, [data-testid="stSelectbox"] label {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}
[data-testid="stTextInput"] input {
    background: rgba(15, 23, 42, 0.7) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    transition: all .2s ease !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
}
[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.18) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #64748b !important; }

/* ---------- BUTTONS ---------- */
.stButton > button {
    width: 100%;
    height: 3.2rem;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    letter-spacing: 0.01em;
    color: #fff !important;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%) !important;
    background-size: 200% 200% !important;
    border: none !important;
    box-shadow: 0 10px 30px -10px rgba(99,102,241,0.65), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    transition: all .3s ease !important;
}
.stButton > button:hover {
    background-position: 100% 0 !important;
    transform: translateY(-2px);
    box-shadow: 0 16px 40px -10px rgba(236,72,153,0.6), inset 0 1px 0 rgba(255,255,255,0.25) !important;
}
.stButton > button:active { transform: translateY(0); }

/* ---------- KPI / METRIC CARDS ---------- */
[data-testid="stMetric"] {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px 22px !important;
    backdrop-filter: blur(14px);
    transition: all .25s ease;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #6366f1, #22d3ee, #ec4899);
    opacity: 0.85;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(99,102,241,0.45);
    box-shadow: 0 18px 50px -12px rgba(99,102,241,0.35);
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
}

/* ---------- DATAFRAME ---------- */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(17,24,39,0.6);
    backdrop-filter: blur(12px);
}

/* ---------- ALERTS / INFO ---------- */
[data-testid="stAlert"] {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(12px);
    background: rgba(30,41,59,0.6) !important;
    color: #e2e8f0 !important;
}

/* ---------- EMERGENCY CONTACT CARDS ---------- */
.emergency-card {
    position: relative;
    padding: 26px 22px;
    border-radius: 20px;
    text-align: left;
    color: #fff;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(14px);
    transition: all .3s ease;
    cursor: pointer;
}
.emergency-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 25px 60px -15px rgba(0,0,0,0.6);
}
.emergency-card .ec-icon {
    font-size: 28px;
    width: 52px; height: 52px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 14px;
    background: rgba(255,255,255,0.15);
    margin-bottom: 14px;
}
.emergency-card .ec-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.85;
    margin-bottom: 6px;
}
.emergency-card .ec-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.emergency-card .ec-sub {
    font-size: 0.85rem;
    opacity: 0.85;
}
.ec-ambulance { background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%); box-shadow: 0 14px 40px -12px rgba(239,68,68,0.55); }
.ec-police    { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); box-shadow: 0 14px 40px -12px rgba(59,130,246,0.55); }
.ec-fire      { background: linear-gradient(135deg, #f59e0b 0%, #c2410c 100%); box-shadow: 0 14px 40px -12px rgba(245,158,11,0.55); }

/* ---------- STATUS PILL ---------- */
.status-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.35);
    color: #86efac !important;
    padding: 6px 12px; border-radius: 999px;
    font-size: 12px; font-weight: 600;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.status-pill .live {
    width: 8px; height: 8px; border-radius: 50%;
    background: #22c55e; animation: pulse-green 1.6s infinite;
}
@keyframes pulse-green {
    0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.7); }
    70% { box-shadow: 0 0 0 10px rgba(34,197,94,0); }
    100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
}

/* ---------- DIVIDER ---------- */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent) !important;
    margin: 32px 0 !important;
}

/* ---------- FOOTER ---------- */
.footer-bar {
    margin-top: 40px;
    padding: 18px 22px;
    border-radius: 16px;
    background: rgba(17,24,39,0.5);
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(10px);
    display: flex; justify-content: space-between; align-items: center;
    color: #94a3b8;
    font-size: 13px;
}
.footer-bar strong { color: #e2e8f0; }

/* ---------- ANIMATIONS ---------- */
.fade-in { animation: fadeIn .6s ease both; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px);} to { opacity:1; transform:none;} }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HERO
# -----------------------------------
st.markdown(f"""
<div class="hero fade-in">
    <div class="hero-badge"><span class="dot"></span> {t("hero_badge")}</div>
    <h1>{t("hero_title")}</h1>
    <p>{t("hero_subtitle")}</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# LOCATION INPUT
# -----------------------------------
st.markdown(f'<div class="section-title"><span class="bar"></span>{t("section_location")}</div>', unsafe_allow_html=True)

with st.container():
    city = st.selectbox(
        t("label_city"),
        [
            "Hyderabad",
            "Hyderabad, Banjara Hills",
            "Hyderabad, Miyapur",
            "Hyderabad, Uppal",
        ]
    )
    col1, col2 = st.columns(2)
    with col1:
        current_location = st.button(t("btn_use_location"))
    with col2:
        search = st.button(t("btn_find_help"))

    if search and city:
        demo_locations = {
            "Hyderabad": (17.3850, 78.4867),
            "Hyderabad, Banjara Hills": (17.4126, 78.4482),
            "Hyderabad, Miyapur": (17.4967, 78.3567),
            "Hyderabad, Uppal": (17.4058, 78.5591),
        }
        coords = demo_locations.get(city)
        if coords:
            lat, lon = coords
            hospitals = get_nearby_hospitals(lat, lon)
            st.session_state["user_lat"] = lat
            st.session_state["user_lon"] = lon
            st.session_state["hospitals"] = hospitals
            st.session_state["searched"] = True
        else:
            st.error(t("err_location_not_found"))

# -----------------------------------
# RESULTS
# -----------------------------------
if st.session_state.get("searched", False):
    st.markdown(
        f'<div class="section-title"><span class="bar"></span>{t("section_hospitals")} '
        f'<span class="status-pill" style="margin-left:10px;"><span class="live"></span>Live</span></div>',
        unsafe_allow_html=True,
    )

    hospital_list = st.session_state.get("hospitals", [])
    if hospital_list:
        first_hospital = hospital_list[0]
        distance, eta = get_route(
            st.session_state["user_lat"],
            st.session_state["user_lon"],
            first_hospital["lat"],
            first_hospital["lon"],
        )
        traffic = traffic_status(eta)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(t("label_top_hospital"), first_hospital["name"])
        with c2:
            st.metric(t("col_distance"), f"{distance} km")
        with c3:
            st.metric(t("col_eta"), f"{eta} min")
        with c4:
            st.metric(t("col_traffic"), traffic)

    st.markdown(
        f'<div class="section-title" style="margin-top:28px;"><span class="bar"></span>{t("section_hospital_list")}</div>',
        unsafe_allow_html=True,
    )

    hospital_list = st.session_state.get("hospitals", [])
    for hospital in hospital_list[:10]:
        try:
            distance, eta = get_route(
                st.session_state["user_lat"],
                st.session_state["user_lon"],
                hospital["lat"],
                hospital["lon"],
            )
            traffic = traffic_status(eta)
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])
            with col1:
                st.write(f"🏥 {hospital['name']}")
            with col2:
                st.write(f"{distance} km")
            with col3:
                st.write(f"{eta} min")
            with col4:
                st.write(traffic)
            with col5:
                if st.button(t("btn_directions"), key=hospital["name"]):
                    st.session_state["selected_hospital"] = hospital
                    st.success(f"{t('msg_selected')}: {hospital['name']}")
                    st.rerun()
        except Exception:
            pass

# -----------------------------------
# MAP
# -----------------------------------
if st.session_state.get("searched", False):
    st.markdown(
        f'<div class="section-title"><span class="bar"></span>{t("section_map")}</div>',
        unsafe_allow_html=True,
    )

    user_lat = st.session_state.get("user_lat")
    user_lon = st.session_state.get("user_lon")
    selected = st.session_state.get("selected_hospital")

    if user_lat is not None and user_lon is not None:
        if selected:
            m = folium.Map(location=[selected["lat"], selected["lon"]], zoom_start=15)
        else:
            m = folium.Map(location=[user_lat, user_lon], zoom_start=13)

        folium.Marker(
            [user_lat, user_lon],
            popup="Your Location",
            tooltip="You",
            icon=folium.Icon(color="blue"),
        ).add_to(m)

        for hospital in st.session_state.get("hospitals", []):
            folium.Marker(
                [hospital["lat"], hospital["lon"]],
                popup=hospital["name"],
                tooltip=hospital["name"],
                icon=folium.Icon(color="red"),
            ).add_to(m)

        if selected:
            st.success(f"{t('map_destination')}: {selected['name']}")

            folium.Marker(
                [selected["lat"], selected["lon"]],
                popup=selected["name"],
                tooltip=selected["name"],
                icon=folium.Icon(color="green", icon="plus-sign"),
            ).add_to(m)

            folium.PolyLine(
                [[user_lat, user_lon], [selected["lat"], selected["lon"]]],
                color="blue",
                weight=6,
                opacity=0.8,
            ).add_to(m)

        st_folium(m, width=None, height=500)

# -----------------------------------
# EMERGENCY CONTACTS
# -----------------------------------
st.markdown(
    f'<div class="section-title"><span class="bar"></span>{t("section_contacts")}</div>',
    unsafe_allow_html=True,
)

e1, e2, e3 = st.columns(3)
with e1:
    st.markdown(f"""
    <div class="emergency-card ec-ambulance">
        <div class="ec-icon">🚑</div>
        <div class="ec-label">{t("ec_ambulance_label")}</div>
        <div class="ec-number">108</div>
        <div class="ec-sub">{t("ec_ambulance_sub")}</div>
    </div>""", unsafe_allow_html=True)
with e2:
    st.markdown(f"""
    <div class="emergency-card ec-police">
        <div class="ec-icon">👮</div>
        <div class="ec-label">{t("ec_police_label")}</div>
        <div class="ec-number">112</div>
        <div class="ec-sub">{t("ec_police_sub")}</div>
    </div>""", unsafe_allow_html=True)
with e3:
    st.markdown(f"""
    <div class="emergency-card ec-fire">
        <div class="ec-icon">🔥</div>
        <div class="ec-label">{t("ec_fire_label")}</div>
        <div class="ec-number">101</div>
        <div class="ec-sub">{t("ec_fire_sub")}</div>
    </div>""", unsafe_allow_html=True)

# -----------------------------------
# AI ASSISTANT
# -----------------------------------
st.markdown(
    f'<div class="section-title"><span class="bar"></span>{t("section_assistant")}</div>',
    unsafe_allow_html=True,
)

model_type = st.selectbox(
    t("label_ai_mode"),
    ["Local Ollama", "BYOK OpenAI"]
)

api_key = ""
if model_type == "BYOK OpenAI":
    api_key = st.text_input(t("label_api_key"), type="password")

question = st.text_area(
    t("label_question"),
    placeholder=t("placeholder_question"),
)

if st.button(t("btn_get_advice")):
    if not question:
        st.warning(t("warn_no_question"))
    else:
        with st.spinner(t("spinner_ai")):
            try:
                # Prepend language instruction so the model responds in the right language
                lang_instruction = t("ai_lang_instruction")
                localized_question = f"{lang_instruction}\n\n{question}"

                answer = ask_ollama(localized_question)

                st.markdown(t("ai_response_header"))
                st.write(answer)
            except Exception as e:
                st.error(f"{t('err_ai')}: {e}")

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown(f"""
<div class="footer-bar">
    <div><strong>RapidAid</strong> · {t("footer_tagline")}</div>
    <div>{t("footer_credit")}</div>
</div>
""", unsafe_allow_html=True)