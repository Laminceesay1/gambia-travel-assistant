"""
✈️ TGTA - The Gambia Travel Assistant
Your AI-Powered Gambia Travel Guide
Plan your trip to Africa's Smiling Coast
https://gambia-travel-guide.com
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from datetime import datetime
import requests
import base64
import random
import urllib.parse

# Path setup
ASSETS_PATH = Path(__file__).parent / "assets"

# Import Knowledge Base
try:
    from knowledge_base import QUICK_ANSWERS, get_smart_answer, get_suggestions
    KB_LOADED = True
except ImportError:
    KB_LOADED = False
    QUICK_ANSWERS = {}
    def get_smart_answer(q): return {"answer": None, "confidence": 0}
    def get_suggestions(q): return []

# Page config
st.set_page_config(
    page_title="TGTA | The Gambia Travel Guide - Visit, Explore & Plan Your Trip",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colors - Gambian Flag
RED = "#CE1126"
BLUE = "#0C1C8C"
GREEN = "#3A7728"

# ============== GOOGLE ANALYTICS ==============
# Replace 'G-XXXXXXXXXX' with your actual Google Analytics 4 Measurement ID
GA_TRACKING_ID = "G-XXXXXXXXXX"  # Get this from analytics.google.com

def inject_ga():
    """Inject Google Analytics tracking code."""
    ga_code = f"""
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_TRACKING_ID}');
    </script>
    """
    st.markdown(ga_code, unsafe_allow_html=True)

# Inject GA on every page load
inject_ga()

# ============== SEO META TAGS ==============
def inject_seo():
    """Inject SEO meta tags for better search engine ranking."""
    seo_tags = """
    <!-- SEO Meta Tags -->
    <meta name="description" content="Plan your Gambia trip with TGTA - The Gambia Travel Assistant. Your complete travel guide with hotels, flights, tours & local tips for visiting The Gambia.">
    <meta name="keywords" content="Gambia, The Gambia, travel, tourism, Africa, West Africa, Banjul, beach, safari, Kunta Kinteh, bird watching, hotels, tours, travel guide, visit Gambia, tourist guide">
    <meta name="author" content="TGTA - The Gambia Travel Assistant">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://gambia-travel-guide.com/">
    <meta property="og:title" content="TGTA | The Gambia Travel Guide - Visit, Explore & Plan Your Trip">
    <meta property="og:description" content="Plan your Gambia trip with TGTA. Your complete travel guide with hotels, flights, tours & local tips for visiting The Gambia.">
    <meta property="og:image" content="https://gambia-travel-guide.com/og-image.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://gambia-travel-guide.com/">
    <meta property="twitter:title" content="TGTA | The Gambia Travel Guide">
    <meta property="twitter:description" content="Your AI-Powered Gambia Travel Guide - Hotels, flights, tours & local tips">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://gambia-travel-guide.com/">
    """
    st.markdown(seo_tags, unsafe_allow_html=True)

# Inject SEO tags
inject_seo()

# ============== SOCIAL SHARING FUNCTION ==============
def social_share_buttons(title, url="https://gambia-travel-guide.com"):
    """Generate social sharing buttons using Streamlit columns."""
    pass  # Now using Streamlit buttons instead

def render_social_buttons(title, url="https://gambia-travel-guide.com"):
    """Render social sharing buttons using Streamlit."""
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(url)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button("📘 Facebook", f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}", use_container_width=True)
    with col2:
        st.link_button("🐦 Twitter/X", f"https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}", use_container_width=True)
    with col3:
        st.link_button("💬 WhatsApp", f"https://wa.me/?text={encoded_title}%20{encoded_url}", use_container_width=True)
    with col4:
        st.link_button("✉️ Email", f"mailto:?subject={encoded_title}&body=Check%20this%20out:%20{encoded_url}", use_container_width=True)

# Custom CSS
st.markdown("""
<style>
#MainMenu, footer, [data-testid="stDecoration"], 
[data-testid="stStatusWidget"], .stDeployButton {display: none !important; visibility: hidden !important;}

[data-testid="stSidebarCollapsedControl"] {
    display: block !important;
    visibility: visible !important;
}

header[data-testid="stHeader"] {background: transparent !important;}
.main .block-container {padding: 2rem 3rem; max-width: 900px;}

.flag-bar {
    height: 5px;
    background: linear-gradient(to right, #CE1126 0%, #CE1126 20%, #FFF 20%, #FFF 35%, 
        #0C1C8C 35%, #0C1C8C 65%, #FFF 65%, #FFF 80%, #3A7728 80%, #3A7728 100%);
    border-radius: 3px;
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] {background: linear-gradient(180deg, #f8f9fa 0%, #fff 100%);}
[data-testid="stSidebar"] .stButton > button {
    width: 100%; text-align: left; padding: 0.75rem 1rem; margin: 0.25rem 0;
    border-radius: 8px; background: transparent; border: none; font-size: 0.95rem;
}
[data-testid="stSidebar"] .stButton > button:hover {background: #e8f5e9;}

.hotel-card {
    background: white; border-radius: 10px; padding: 1.25rem; margin: 0.75rem 0;
    border: 1px solid #eee; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.book-btn {
    display: inline-block; background: #3A7728; color: white !important;
    padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none;
    font-size: 0.9rem; margin-top: 0.5rem;
}

.stButton > button {border-radius: 24px; font-weight: 500;}

.stTextInput > div > div > input {
    border-radius: 24px; padding: 0.75rem 1.25rem; font-size: 1rem;
    border: 1px solid #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stTextInput > div > div > input:focus {
    border-color: #3A7728; box-shadow: 0 2px 12px rgba(58,119,40,0.15);
}
</style>
""", unsafe_allow_html=True)

# ============== API FUNCTIONS ==============

@st.cache_data(ttl=1800)
def get_live_weather():
    """Get live weather for Banjul."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": 13.4549, "longitude": -16.5790,
                  "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m", "timezone": "GMT"}
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            c = r.json().get("current", {})
            return {"temperature": c.get("temperature_2m", 28), "humidity": c.get("relative_humidity_2m", 70),
                    "wind_speed": c.get("wind_speed_10m", 15), "weather_code": c.get("weather_code", 0), "success": True}
    except: pass
    return {"success": False, "temperature": 28, "humidity": 70, "wind_speed": 15, "weather_code": 0}

@st.cache_data(ttl=3600)
def get_exchange_rates():
    """Get exchange rates."""
    try:
        r = requests.get("https://api.frankfurter.app/latest?from=EUR&to=USD,GBP", timeout=10)
        if r.status_code == 200:
            rates = r.json().get("rates", {})
            gmd = 70.0
            return {"EUR": {"rate": gmd, "symbol": "€"}, "USD": {"rate": gmd/rates.get("USD", 1.1), "symbol": "$"},
                    "GBP": {"rate": gmd/rates.get("GBP", 0.85), "symbol": "£"}, "success": True}
    except: pass
    return {"EUR": {"rate": 70, "symbol": "€"}, "USD": {"rate": 65, "symbol": "$"}, "GBP": {"rate": 82, "symbol": "£"}, "success": False}

@st.cache_data(ttl=86400)
def search_gambia_wikipedia(query: str):
    """Search Wikipedia for Gambia-related topics."""
    GAMBIA_WIKI_MAP = {
        "serekunda": "Serekunda", "bakau": "Bakau", "brikama": "Brikama",
        "banjul": "Banjul", "kololi": "Kololi", "kotu": "Kotu_Stream",
        "bijilo": "Bijilo", "brufut": "Brufut", "gunjur": "Gunjur", "sanyang": "Sanyang",
        "soma": "Soma,_Gambia", "farafenni": "Farafenni", "basse": "Basse_Santa_Su",
        "janjanbureh": "Janjanbureh", "kunta kinteh": "Kunta_Kinte", "kunta kinte": "Kunta_Kinte",
        "kunta kinteh island": "Kunta_Kinteh_Island", "james island": "Kunta_Kinteh_Island",
        "gambia river": "Gambia_River", "history": "History_of_the_Gambia",
        "mandinka": "Mandinka_people", "wolof": "Wolof_people", "fula": "Fula_people",
        "tourism": "Tourism_in_the_Gambia", "culture": "Culture_of_the_Gambia",
        "abuko": "Abuko_Nature_Reserve", "makasutu": "Makasutu_Culture_Forest",
        "stone circles": "Stone_Circles_of_Senegambia", "wassu": "Wassu_Stone_Circles",
        "gambia": "The_Gambia", "the gambia": "The_Gambia",
    }
    q_lower = query.lower().strip()
    
    for key, article in GAMBIA_WIKI_MAP.items():
        if key in q_lower or q_lower in key:
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article}"
                r = requests.get(url, headers={"User-Agent": "GambiaTravelAssistant/1.0"}, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    return {
                        "title": data.get("title", article.replace("_", " ")),
                        "summary": data.get("extract", ""),
                        "url": data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{article}"),
                        "image": data.get("thumbnail", {}).get("source", ""),
                        "success": True
                    }
            except: pass
    
    return {"success": False, "title": query, "summary": "", "url": "", "image": ""}

def get_weather_icon(code: int) -> str:
    icons = {0: "☀️", 1: "⛅", 2: "⛅", 3: "⛅", 45: "🌫️", 48: "🌫️", 51: "🌧️", 53: "🌧️", 55: "🌧️",
             61: "🌧️", 63: "🌧️", 65: "🌧️", 80: "🌧️", 81: "🌧️", 82: "🌧️", 95: "⛈️", 96: "⛈️", 99: "⛈️"}
    return icons.get(code, "🌤️")

# ============== DATA ==============

# NOTE: Replace YOUR_AFFILIATE_ID with your actual affiliate IDs when you sign up
# Booking.com: https://www.booking.com/affiliate-program/v2/index.html
# Airbnb: No longer has affiliate program, use direct links
# Skyscanner: https://www.partners.skyscanner.net/

HOTELS = [
    {"name": "Coco Ocean Resort & Spa", "area": "Bijilo", "stars": 5, "price": "$120-200", "feat": "Beach, Pool, Spa", "url": "https://www.booking.com/searchresults.html?ss=Coco+Ocean+Resort+Gambia&dest_type=hotel"},
    {"name": "Senegambia Beach Hotel", "area": "Kololi", "stars": 4, "price": "$80-150", "feat": "Beach, Pool", "url": "https://www.booking.com/searchresults.html?ss=Senegambia+Beach+Hotel+Gambia"},
    {"name": "Sunset Beach Hotel", "area": "Kotu", "stars": 4, "price": "$70-120", "feat": "Beach, Family", "url": "https://www.booking.com/searchresults.html?ss=Sunset+Beach+Hotel+Gambia"},
    {"name": "Kombo Beach Hotel", "area": "Kotu", "stars": 3, "price": "$50-90", "feat": "Pool, Garden", "url": "https://www.booking.com/searchresults.html?ss=Kombo+Beach+Hotel+Gambia"},
    {"name": "Luigi's Guesthouse", "area": "Kololi", "stars": 2, "price": "$25-50", "feat": "Budget", "url": "https://www.booking.com/searchresults.html?ss=Kololi+Gambia&nflt=class%3D1"},
    {"name": "Ngala Lodge", "area": "Fajara", "stars": 4, "price": "$90-140", "feat": "Boutique, Garden", "url": "https://www.booking.com/searchresults.html?ss=Ngala+Lodge+Gambia"},
    {"name": "Bakotu Hotel", "area": "Kotu", "stars": 3, "price": "$45-80", "feat": "Pool, Birding", "url": "https://www.booking.com/searchresults.html?ss=Bakotu+Hotel+Gambia"},
    {"name": "Ocean Bay Hotel", "area": "Cape Point", "stars": 4, "price": "$75-130", "feat": "Beach, Pool", "url": "https://www.booking.com/searchresults.html?ss=Ocean+Bay+Hotel+Gambia"},
    {"name": "Mandina Lodges", "area": "Makasutu", "stars": 5, "price": "$150-250", "feat": "Eco-Lodge, River", "url": "https://www.booking.com/searchresults.html?ss=Mandina+Lodges+Gambia"},
    {"name": "Lemon Creek Hotel", "area": "Bijilo", "stars": 3, "price": "$55-95", "feat": "Pool, Restaurant", "url": "https://www.booking.com/searchresults.html?ss=Lemon+Creek+Hotel+Gambia"},
]

TOURS = [
    {"name": "Kunta Kinteh Island Day Trip", "type": "Heritage", "price": "$45-65", "duration": "Full Day", "url": "https://www.getyourguide.com"},
    {"name": "Makasutu Culture Forest", "type": "Eco-Tour", "price": "$55-75", "duration": "Half Day", "url": "https://www.viator.com"},
    {"name": "River Gambia Cruise", "type": "Nature", "price": "$35-50", "duration": "3-4 hours", "url": "https://www.getyourguide.com"},
    {"name": "Abuko Nature Reserve", "type": "Wildlife", "price": "$20-30", "duration": "Half Day", "url": "https://www.viator.com"},
    {"name": "Banjul City Tour", "type": "Culture", "price": "$25-40", "duration": "3-4 hours", "url": "https://www.getyourguide.com"},
    {"name": "Tanji Fishing Village", "type": "Local Life", "price": "$20-35", "duration": "Half Day", "url": "https://www.viator.com"},
]

# ============== FLIGHTS DATA ==============
AIRLINES = [
    {"name": "Royal Air Maroc", "from": "Casablanca (CMN)", "freq": "Daily", "flight": "~3h via CMN", "price": "$350-700", "logo": "🇲🇦", "url": "https://www.royalairmaroc.com/"},
    {"name": "Lufthansa", "from": "Frankfurt (FRA)", "freq": "Via partners", "flight": "~7h via hub", "price": "$500-900", "logo": "🇩🇪", "url": "https://www.lufthansa.com/"},
    {"name": "Swiss International Air Lines", "from": "Zurich (ZRH)", "freq": "Via partners", "flight": "~7h via hub", "price": "$550-950", "logo": "🇨🇭", "url": "https://www.swiss.com/"},
    {"name": "Brussels Airlines", "from": "Brussels (BRU)", "freq": "3x weekly", "flight": "~6h direct", "price": "$400-800", "logo": "🇧🇪", "url": "https://www.brusselsairlines.com/"},
    {"name": "Turkish Airlines", "from": "Istanbul (IST)", "freq": "3x weekly", "flight": "~8h via IST", "price": "$450-900", "logo": "🇹🇷", "url": "https://www.turkishairlines.com/"},
    {"name": "TAP Portugal", "from": "Lisbon (LIS)", "freq": "Via partners", "flight": "~5h via LIS", "price": "$400-800", "logo": "🇵🇹", "url": "https://www.flytap.com/"},
    {"name": "Vueling Airlines", "from": "Barcelona (BCN)", "freq": "2x weekly", "flight": "~5h direct", "price": "$250-500", "logo": "🇪🇸", "url": "https://www.vueling.com/"},
    {"name": "TUI Airways", "from": "London Gatwick (LGW)", "freq": "Seasonal (Nov-Apr)", "flight": "~6h direct", "price": "$300-600", "logo": "🇬🇧", "url": "https://www.tui.co.uk/"},
    {"name": "Air Senegal", "from": "Dakar (DSS)", "freq": "Daily", "flight": "~30min", "price": "$80-200", "logo": "🇸🇳", "url": "https://www.airsenegal.com/"},
    {"name": "ASKY Airlines", "from": "West Africa hubs", "freq": "Multiple", "flight": "Regional", "price": "$150-400", "logo": "🇹🇬", "url": "https://www.flyasky.com/"},
]

FLIGHT_SEARCH_LINKS = {
    "skyscanner": "https://www.skyscanner.com/transport/flights/YOURLOCATION/bjl/",
    "kayak": "https://www.kayak.com/flights/NYC-BJL",
    "google_flights": "https://www.google.com/travel/flights?q=flights%20to%20banjul",
    "expedia": "https://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:,to:BJL",
}

ATTRACTIONS = [
    {"name": "Kunta Kinteh Island", "type": "UNESCO Heritage", "desc": "Historic slave trade site from the novel 'Roots' - UNESCO World Heritage Site", "cost": "$15-25"},
    {"name": "Abuko Nature Reserve", "type": "Wildlife", "desc": "Forest with monkeys, birds, crocodiles - oldest wildlife reserve in the country", "cost": "$5-10"},
    {"name": "Makasutu Culture Forest", "type": "Eco-tourism", "desc": "Sacred forest, boat rides, village life - unique eco-experience", "cost": "$40-60"},
    {"name": "Kololi Beach", "type": "Beach", "desc": "Main tourist beach with restaurants, bars and water sports", "cost": "Free"},
    {"name": "Albert Market", "type": "Culture", "desc": "Banjul's largest and oldest market for crafts, fabrics, spices and food", "cost": "Free"},
    {"name": "Bijilo Forest Park", "type": "Wildlife", "desc": "Family-friendly monkey walk near the coast - great for kids!", "cost": "$3-5"},
    {"name": "Arch 22", "type": "Monument", "desc": "Iconic 35-meter triumphal arch in Banjul with panoramic city views", "cost": "$1-2"},
    {"name": "Tanji Fishing Village", "type": "Culture", "desc": "Authentic fishing village - watch colorful boats return at sunset", "cost": "Free"},
    {"name": "Kachikally Crocodile Pool", "type": "Wildlife", "desc": "Sacred pool with over 80 friendly crocodiles - touch them!", "cost": "$3-5"},
    {"name": "Sanyang Beach", "type": "Beach", "desc": "Paradise beach less crowded than Kololi - fresh grilled fish!", "cost": "Free"},
    {"name": "River Gambia National Park", "type": "Wildlife", "desc": "Home to chimps, hippos and diverse birdlife - boat safaris available", "cost": "$20-50"},
    {"name": "Wassu Stone Circles", "type": "UNESCO Heritage", "desc": "Ancient megalithic site - mysterious stone circles over 1000 years old", "cost": "$5-10"},
]

# ============== FOOD DATA ==============
FOOD_DATA = {
    "dishes": [
        {"name": "Benachin", "aka": "Jollof Rice", "desc": "One-pot rice dish - national dish! Tomato-based with meat or fish.", "try": "Must try", "price": "D50-150"},
        {"name": "Domoda", "aka": "Groundnut Stew", "desc": "Rich, creamy peanut butter stew with meat - comfort food!", "try": "Must try", "price": "D60-150"},
        {"name": "Superkanja", "aka": "Okra Soup", "desc": "Slimy okra-based stew - traditional Mandinka dish.", "try": "Adventurous", "price": "D50-120"},
        {"name": "Afra", "aka": "Grilled Meat", "desc": "Street food skewers with spicy sauce - best at night markets!", "try": "Must try", "price": "D30-80"},
        {"name": "Tapalapa", "aka": "Gambian Bread", "desc": "Baguette-style bread, crispy outside, soft inside.", "try": "Daily staple", "price": "D5-15"},
        {"name": "Yassa", "aka": "Onion Sauce", "desc": "Chicken or fish in tangy lemon-onion sauce.", "try": "Must try", "price": "D80-180"},
    ],
    "drinks": [
        {"name": "Attaya", "aka": "Green Tea", "desc": "3-round tea ceremony - symbol of hospitality. Never refuse!", "price": "Often free"},
        {"name": "Wonjo", "aka": "Hibiscus Juice", "desc": "Sweet red drink from hibiscus flowers - refreshing!", "price": "D15-30"},
        {"name": "Baobab Juice", "aka": "Bouye", "desc": "Nutritious drink from baobab fruit - energy booster.", "price": "D20-40"},
        {"name": "Ginger Juice", "aka": "Ginger Drink", "desc": "Fresh ginger with lemon - warming and medicinal.", "price": "D15-30"},
    ],
    "markets": [
        {"name": "Albert Market, Banjul", "desc": "The largest and oldest market in The Gambia - fish, produce, fabrics, crafts and street food. Best to visit early morning before the heat!"},
        {"name": "Serekunda Market", "desc": "The biggest market in the entire country - you can find absolutely everything here! Can be overwhelming but an authentic experience. Bargain hard!"},
        {"name": "Kololi Night Market", "desc": "Afra (grilled meat) heaven - best visited after 7pm when the smoke rises and the skewers sizzle. Friendly atmosphere with locals and tourists."},
    ]
}

# ============== PHRASES DATA ==============
PHRASES = {
    "mandinka": [
        {"english": "Hello", "local": "I be di", "pronun": "ee-bay-dee"},
        {"english": "How are you?", "local": "Here be di?", "pronun": "hay-ray-bay-dee"},
        {"english": "I'm fine", "local": "Mbee jaata", "pronun": "em-bay-jah-tah"},
        {"english": "Thank you", "local": "Abaraka", "pronun": "ah-bah-rah-kah"},
        {"english": "Please", "local": "Dukare", "pronun": "doo-kah-ray"},
        {"english": "Yes", "local": "Haa", "pronun": "haa"},
        {"english": "No", "local": "Hani", "pronun": "hah-nee"},
        {"english": "Goodbye", "local": "Fo tuma doo", "pronun": "foh-too-mah-doh"},
        {"english": "How much?", "local": "Jelu le?", "pronun": "jeh-loo-lay"},
        {"english": "Too expensive", "local": "A songo jata", "pronun": "ah-song-oh-jah-tah"},
    ],
    "wolof": [
        {"english": "Hello", "local": "Salaam aleekum", "pronun": "sah-lahm-ah-lay-koom"},
        {"english": "How are you?", "local": "Nanga def?", "pronun": "nahn-gah-def"},
        {"english": "I'm fine", "local": "Mangi fi rekk", "pronun": "mahn-gee-fee-rek"},
        {"english": "Thank you", "local": "Jërëjëf", "pronun": "jeh-reh-jef"},
        {"english": "Please", "local": "Bu la neexee", "pronun": "boo-lah-neh-hay"},
        {"english": "Yes", "local": "Waaw", "pronun": "wow"},
        {"english": "No", "local": "Déedéet", "pronun": "day-dayt"},
        {"english": "Goodbye", "local": "Maa ngi dem", "pronun": "mah-ngee-dem"},
        {"english": "How much?", "local": "Ñaata la?", "pronun": "nyah-tah-lah"},
        {"english": "Too expensive", "local": "Dafa seer", "pronun": "dah-fah-seer"},
    ],
}

# ============== ITALIAN TOURIST PHRASES ==============
# Common phrases Italian tourists might need (English to use in Gambia)
ITALIAN_PHRASES = [
    {"italian": "Ciao", "english": "Hello", "mandinka": "I be di"},
    {"italian": "Come stai?", "english": "How are you?", "mandinka": "Here be di?"},
    {"italian": "Grazie", "english": "Thank you", "mandinka": "Abaraka"},
    {"italian": "Per favore", "english": "Please", "mandinka": "Dukare"},
    {"italian": "Sì", "english": "Yes", "mandinka": "Haa"},
    {"italian": "No", "english": "No", "mandinka": "Hani"},
    {"italian": "Arrivederci", "english": "Goodbye", "mandinka": "Fo tuma doo"},
    {"italian": "Quanto costa?", "english": "How much?", "mandinka": "Jelu le?"},
    {"italian": "Troppo caro", "english": "Too expensive", "mandinka": "A songo jata"},
    {"italian": "Acqua", "english": "Water", "mandinka": "Jio"},
    {"italian": "Aiuto!", "english": "Help!", "mandinka": "N dema!"},
    {"italian": "Dov'è...?", "english": "Where is...?", "mandinka": "...be mintolu?"},
]

# ============== FAQ DATA ==============
FAQ_DATA = [
    {"q": "Do I need a visa to visit The Gambia?", "a": "Most nationalities get visa on arrival (free or small fee). UK, EU, US citizens don't need advance visa. Check with your embassy for specifics.", "cat": "Entry"},
    {"q": "What is the Tourism Development Levy?", "a": "A €20 fee payable on arrival AND departure (€40 total). Cash only - Euros, USD, or GBP accepted. Keep your receipt!", "cat": "Entry"},
    {"q": "Is The Gambia safe for tourists?", "a": "Yes! The Gambia is one of Africa's safest destinations. Petty theft can occur (like anywhere), so take normal precautions. Violent crime against tourists is very rare.", "cat": "Safety"},
    {"q": "What currency is used?", "a": "Gambian Dalasi (GMD). Euros and USD are widely accepted at hotels and tourist areas. ATMs available in main towns. Bring some cash as backup.", "cat": "Money"},
    {"q": "Do I need malaria tablets?", "a": "YES - strongly recommended. Consult your doctor 4-6 weeks before travel. Also use DEET repellent and sleep under mosquito nets.", "cat": "Health"},
    {"q": "What's the best time to visit?", "a": "November to May (dry season). Peak season is Nov-Feb with perfect weather. Avoid July-October (heavy rains, some hotels close).", "cat": "Planning"},
    {"q": "What should I pack?", "a": "Light cotton clothes, modest dress for villages, sun protection, insect repellent, malaria tablets, UK-style adapter (Type G), and cash for the Tourism Levy.", "cat": "Planning"},
    {"q": "Is English spoken?", "a": "Yes! English is the official language. You'll have no problems communicating. Local languages include Mandinka, Wolof, and Fula.", "cat": "Culture"},
    {"q": "Can I drink tap water?", "a": "No - stick to bottled water, which is cheap and widely available. Ice in tourist hotels is usually safe.", "cat": "Health"},
    {"q": "How do I get from the airport?", "a": "Taxis are available at Banjul International Airport. Agree on price BEFORE getting in (expect 500-800 GMD to tourist areas). Many hotels offer airport transfers.", "cat": "Transport"},
    {"q": "Is bargaining expected?", "a": "Yes, at markets and with taxis! Start at 50% of asking price and negotiate. Fixed prices only at supermarkets and upscale shops.", "cat": "Culture"},
    {"q": "What about tipping?", "a": "Tips appreciated but not mandatory. 10% at restaurants if service charge not included. Small tips for guides and hotel staff are welcomed.", "cat": "Money"},
]

# ============== BLOG/TIPS DATA ==============
BLOG_TIPS = [
    {"title": "First Time in The Gambia? Read This!", "excerpt": "Essential tips for first-time visitors - what to expect, what to pack, and how to make the most of your trip.", "cat": "Planning", "read_time": "5 min"},
    {"title": "Best Beaches in The Gambia Ranked", "excerpt": "From busy Kololi to serene Sanyang - we rank the top beaches and tell you which one suits your style.", "cat": "Beaches", "read_time": "4 min"},
    {"title": "Gambian Food You Must Try", "excerpt": "Don't leave without trying Benachin, Domoda, and Yassa. Here's your complete food guide.", "cat": "Food", "read_time": "6 min"},
    {"title": "How to Bargain at Albert Market", "excerpt": "Master the art of friendly negotiation and get the best deals on crafts, clothes, and souvenirs.", "cat": "Shopping", "read_time": "3 min"},
    {"title": "Day Trip: Kunta Kinteh Island", "excerpt": "A moving journey to the UNESCO site - what to expect, how to book, and why it matters.", "cat": "Heritage", "read_time": "5 min"},
    {"title": "Birding Paradise: 540+ Species Guide", "excerpt": "The Gambia has more bird species per square km than anywhere in Africa. Here's where to spot them.", "cat": "Nature", "read_time": "7 min"},
    {"title": "Solo Female Travel in The Gambia", "excerpt": "Is it safe? What to wear? Real advice from women who've traveled independently.", "cat": "Safety", "read_time": "5 min"},
    {"title": "Budget Travel: £30/Day Itinerary", "excerpt": "Yes, you can visit The Gambia on a budget! Here's how to see everything without breaking the bank.", "cat": "Budget", "read_time": "6 min"},
]

# ============== PACKING LIST ==============
PACKING_LIST = {
    "essentials": [
        "✈️ Passport (6+ months valid)",
        "💵 Cash (EUR/USD) for Tourism Levy",
        "📱 Phone + charger (UK plugs work)",
        "💳 Backup debit/credit card",
        "📄 Travel insurance docs",
        "📷 Camera",
    ],
    "clothing": [
        "👕 Light cotton clothes",
        "🩳 Shorts/light pants",
        "👗 Modest dress for villages/mosques",
        "🩴 Sandals + comfortable walking shoes",
        "🧢 Sun hat",
        "🕶️ Sunglasses",
        "🏊 Swimwear",
        "🧥 Light jacket (Dec-Feb evenings)",
    ],
    "health": [
        "💊 Malaria tablets (start before!)",
        "🦟 DEET insect repellent",
        "🧴 SPF 30+ sunscreen",
        "💧 Rehydration sachets",
        "🩹 Basic first aid kit",
        "💊 Any prescription meds",
    ],
    "useful": [
        "🔦 Flashlight (power cuts happen)",
        "🎒 Day backpack",
        "📖 Guidebook/offline maps",
        "🧻 Tissues/wet wipes",
        "🔌 Power adapter (UK Type G)",
        "🎁 Small gifts for locals (pens, sweets)",
    ],
}

# ============== EVENTS CALENDAR ==============
EVENTS = [
    {"month": "January", "event": "New Year Celebrations", "desc": "Beach parties, hotel events, fireworks", "type": "Festival"},
    {"month": "February", "event": "Independence Day (18th)", "desc": "National holiday - parades, cultural shows in Banjul", "type": "National"},
    {"month": "February", "event": "Roots Homecoming Festival", "desc": "African diaspora celebration - music, culture, heritage tours", "type": "Cultural"},
    {"month": "March-April", "event": "Easter Weekend", "desc": "Beach activities, church services", "type": "Religious"},
    {"month": "April", "event": "Eid al-Fitr", "desc": "End of Ramadan - family gatherings, feasts, new clothes", "type": "Religious"},
    {"month": "May", "event": "International Roots Festival", "desc": "Bi-annual heritage festival - Kunta Kinteh focus", "type": "Cultural"},
    {"month": "June", "event": "Eid al-Adha", "desc": "Feast of Sacrifice - major Islamic holiday", "type": "Religious"},
    {"month": "July", "event": "Kartong Festival", "desc": "Arts & culture festival in Kartong village", "type": "Cultural"},
    {"month": "November", "event": "Tourism Season Opens", "desc": "Hotels reopen, flights resume, perfect weather begins", "type": "Tourism"},
    {"month": "December", "event": "Christmas & New Year", "desc": "Peak tourism - book early! Beach parties, hotel events", "type": "Festival"},
    {"month": "Year-round", "event": "Bird Watching Season", "desc": "Best Nov-Apr when migratory birds arrive", "type": "Nature"},
    {"month": "Year-round", "event": "Fishing Competitions", "desc": "Sport fishing events, especially Nov-May", "type": "Sports"},
]

# ============== LOCAL BUSINESSES ==============
LOCAL_BUSINESSES = [
    # Restaurants
    {"name": "Butcher's Shop", "cat": "Restaurant", "area": "Kololi", "desc": "Best steaks in Gambia, expat favorite", "website": "https://www.google.com/search?q=Butcher's+Shop+Kololi+Gambia", "featured": True},
    {"name": "Calypso Restaurant", "cat": "Restaurant", "area": "Kololi", "desc": "Beachfront dining, seafood specialties", "website": "https://www.google.com/search?q=Calypso+Restaurant+Kololi+Gambia", "featured": True},
    {"name": "Ali Baba's", "cat": "Restaurant", "area": "Fajara", "desc": "Lebanese cuisine, shisha lounge", "website": "https://www.google.com/search?q=Ali+Baba+Restaurant+Fajara+Gambia", "featured": False},
    {"name": "Mama's Kitchen", "cat": "Restaurant", "area": "Bakau", "desc": "Authentic Gambian food, local prices", "website": "https://www.google.com/search?q=Mama's+Kitchen+Bakau+Gambia", "featured": False},
    {"name": "Solomon's Beach Bar", "cat": "Restaurant", "area": "Cape Point", "desc": "Beach bar, fresh fish, sunset views", "website": "https://www.google.com/search?q=Solomon's+Beach+Bar+Cape+Point+Gambia", "featured": False},
    # Car Rentals
    {"name": "AB Rent-A-Car", "cat": "Car Rental", "area": "Kololi", "desc": "SUVs, sedans, airport pickup", "website": "https://www.google.com/search?q=AB+Rent+A+Car+Kololi+Gambia", "featured": True},
    {"name": "Gambia Car Hire", "cat": "Car Rental", "area": "Banjul", "desc": "Budget to luxury vehicles", "website": "https://www.google.com/search?q=Gambia+Car+Hire+Banjul", "featured": False},
    # Shops
    {"name": "Timbooktoo", "cat": "Shop", "area": "Fajara", "desc": "Bookshop, crafts, souvenirs, cafe", "website": "https://www.timbooktoo.com", "featured": True},
    {"name": "Kerewan Craft Market", "cat": "Shop", "area": "Kololi", "desc": "Authentic crafts, fair prices", "website": "https://www.google.com/search?q=Kerewan+Craft+Market+Kololi+Gambia", "featured": False},
    # Services
    {"name": "Gambia Tours", "cat": "Travel Agency", "area": "Kololi", "desc": "Full service tour operator", "website": "https://www.gambiatours.gm", "featured": True},
    {"name": "Hidden Gambia", "cat": "Travel Agency", "area": "Brufut", "desc": "Eco-tours, community tourism", "website": "https://www.hiddengambia.com", "featured": False},
    {"name": "MedGambia Clinic", "cat": "Medical", "area": "Fajara", "desc": "Private clinic, English-speaking doctors", "website": "https://www.google.com/search?q=MedGambia+Clinic+Fajara", "featured": True},
    # Spas & Wellness
    {"name": "Coco Ocean Spa", "cat": "Spa", "area": "Bijilo", "desc": "Luxury spa, massage, treatments", "website": "https://www.cocoocean.com", "featured": True},
    {"name": "African Living Spa", "cat": "Spa", "area": "Kololi", "desc": "Traditional treatments, affordable", "website": "https://www.google.com/search?q=African+Living+Spa+Kololi+Gambia", "featured": False},
]

# ============== TOUR GUIDES ==============
TOUR_GUIDES = [
    {"name": "Lamin Touray", "specialty": "Cultural & Heritage", "langs": "English, Mandinka, Wolof", "exp": "15 years", "area": "All Gambia", "price": "$40/day", "featured": True, "bio": "Expert in Roots history, Kunta Kinteh Island specialist"},
    {"name": "Fatou Jallow", "specialty": "Birdwatching", "langs": "English, French, Fula", "exp": "10 years", "area": "Coastal & River", "price": "$50/day", "featured": True, "bio": "Certified birding guide, knows 300+ species"},
    {"name": "Ousman Ceesay", "specialty": "Photography Tours", "langs": "English, Mandinka", "exp": "8 years", "area": "All Gambia", "price": "$60/day", "featured": True, "bio": "Professional photographer, knows best spots"},
    {"name": "Mariama Sowe", "specialty": "Women's Tours", "langs": "English, Wolof", "exp": "5 years", "area": "TDA & Upcountry", "price": "$35/day", "featured": False, "bio": "Solo female travel expert, cultural immersion"},
    {"name": "Ebrima Sanyang", "specialty": "Adventure & Nature", "langs": "English, German, Mandinka", "exp": "12 years", "area": "River & Upcountry", "price": "$45/day", "featured": False, "bio": "Kayaking, hiking, wildlife expert"},
    {"name": "Modou Faal", "specialty": "City & Market Tours", "langs": "English, Arabic, Wolof", "exp": "7 years", "area": "Banjul & TDA", "price": "$30/day", "featured": False, "bio": "Banjul expert, bargaining specialist"},
]

# ============== YOUTUBE VIDEOS ==============
YOUTUBE_VIDEOS = [
    {"title": "The Gambia - Smiling Coast of Africa", "id": "6KZWzrPwjcU", "channel": "Visit The Gambia", "cat": "Overview", "desc": "Official tourism video showcasing The Gambia's beauty"},
    {"title": "The Gambia Travel Guide 2024", "id": "wZG3xKxELGc", "channel": "Touropia", "cat": "Overview", "desc": "Complete travel guide - beaches, culture, wildlife"},
    {"title": "Kunta Kinteh Island - Roots Heritage", "id": "TvQviLLgkzc", "channel": "UNESCO", "cat": "Heritage", "desc": "UNESCO World Heritage site, slave trade history"},
    {"title": "Gambian Street Food Tour", "id": "qVcj_HdDX-I", "channel": "Best Ever Food Review", "cat": "Food", "desc": "Trying Benachin, Domoda, and local delicacies"},
    {"title": "Birding in The Gambia", "id": "_0ZrKgVj5j4", "channel": "BirdLife", "cat": "Nature", "desc": "540+ bird species - Africa's best birding destination"},
    {"title": "Beach Hotels & Resorts Review", "id": "H7FML8X8dPc", "channel": "Travel Guide", "cat": "Hotels", "desc": "Tour of Kololi, Kotu, and Cape Point beach resorts"},
    {"title": "Abuko Nature Reserve Wildlife", "id": "Z8g1XnMu-Ag", "channel": "Wildlife TV", "cat": "Nature", "desc": "Monkeys, crocodiles, and exotic birds"},
    {"title": "River Gambia Cruise Adventure", "id": "Zy5m4QYLfss", "channel": "Adventure Travel", "cat": "Adventure", "desc": "Journey up the River Gambia - hippos, chimps, villages"},
    {"title": "Banjul City Walking Tour", "id": "bFv9HDjYCM8", "channel": "Walk The World", "cat": "Cities", "desc": "Exploring Albert Market, Arch 22, and local life"},
    {"title": "Gambia Nightlife & Culture", "id": "pGmL9WgKO2c", "channel": "Africa Travel", "cat": "Culture", "desc": "Music, dance, and entertainment scene"},
]

# ============== REVIEWS ==============
REVIEWS = [
    # Hotel reviews
    {"type": "hotel", "item": "Coco Ocean Resort & Spa", "rating": 5, "author": "Sarah M.", "date": "Dec 2025", "text": "Absolutely stunning resort! The spa was incredible and staff couldn't be more helpful. Beach was pristine.", "verified": True},
    {"type": "hotel", "item": "Coco Ocean Resort & Spa", "rating": 4, "author": "James T.", "date": "Nov 2025", "text": "Great location and facilities. Food was excellent. Only minor issue was slow WiFi.", "verified": True},
    {"type": "hotel", "item": "Senegambia Beach Hotel", "rating": 5, "author": "Emma K.", "date": "Jan 2026", "text": "Perfect for families! Kids loved the pool and the craft market right outside is amazing.", "verified": True},
    {"type": "hotel", "item": "Senegambia Beach Hotel", "rating": 4, "author": "Michael B.", "date": "Dec 2025", "text": "Classic Gambian hotel experience. Great atmosphere, friendly staff, central location.", "verified": False},
    {"type": "hotel", "item": "Ngala Lodge", "rating": 5, "author": "Linda P.", "date": "Nov 2025", "text": "Boutique gem! Quiet, romantic, incredible attention to detail. Will definitely return.", "verified": True},
    # Guide reviews
    {"type": "guide", "item": "Lamin Touray", "rating": 5, "author": "Robert H.", "date": "Dec 2025", "text": "Lamin made our Roots tour unforgettable. His knowledge of history is encyclopedic!", "verified": True},
    {"type": "guide", "item": "Fatou Jallow", "rating": 5, "author": "Carol W.", "date": "Jan 2026", "text": "Best birding guide ever! Spotted over 80 species in one day. Patient and knowledgeable.", "verified": True},
    {"type": "guide", "item": "Ousman Ceesay", "rating": 5, "author": "David L.", "date": "Nov 2025", "text": "Amazing photography spots I never would have found alone. Worth every penny!", "verified": True},
    # Restaurant reviews
    {"type": "business", "item": "Butcher's Shop", "rating": 5, "author": "Tom R.", "date": "Dec 2025", "text": "Best steaks in West Africa, no exaggeration. Great wine selection too.", "verified": True},
    {"type": "business", "item": "Calypso Restaurant", "rating": 4, "author": "Anna S.", "date": "Jan 2026", "text": "Beautiful beachfront setting. Seafood was fresh and delicious. Bit pricey but worth it.", "verified": False},
    # Attraction reviews
    {"type": "attraction", "item": "Kunta Kinteh Island", "rating": 5, "author": "Michelle D.", "date": "Dec 2025", "text": "Deeply moving experience. The boat ride and tour guide made it special. Must-visit!", "verified": True},
    {"type": "attraction", "item": "Abuko Nature Reserve", "rating": 5, "author": "Peter K.", "date": "Nov 2025", "text": "So many animals! Saw crocodiles, monkeys, and countless birds. Great for families.", "verified": True},
]

# ============== SESSION STATE ==============
if "page" not in st.session_state: st.session_state.page = "home"

# ============== SIDEBAR ==============
with st.sidebar:
    logo_path = ASSETS_PATH / "tgta_logo.png"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:1rem; background:linear-gradient(135deg, #CE1126, #0C1C8C, #3A7728); border-radius:10px; margin-bottom:1rem;">
            <span style="font-size:2.5rem;">🦅</span>
            <h2 style="color:white; margin:0.5rem 0 0 0; font-size:1.2rem;">TGTA</h2>
            <p style="color:#ddd; margin:0; font-size:0.75rem;">The Gambia Travel Assistant</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="flag-bar"></div>', unsafe_allow_html=True)
    st.markdown("### ✈️ TGTA")
    st.markdown("*Your AI-Powered Gambia Travel Guide*")
    st.markdown("---")
    
    # ===== MAIN NAVIGATION =====
    st.markdown("**🏠 Main**")
    
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    if st.button("📖 Travel Guides", key="nav_guides", use_container_width=True):
        st.session_state.page = "guides"
        st.rerun()
    
    st.markdown("---")
    st.markdown("**✈️ Plan Your Trip**")
    
    if st.button("✈️ Flights", key="nav_flights", use_container_width=True):
        st.session_state.page = "flights"
        st.rerun()
    
    if st.button("🏨 Hotels & Stays", key="nav_hotels", use_container_width=True):
        st.session_state.page = "hotels"
        st.rerun()
    
    if st.button("🎫 Book Tours", key="nav_tours", use_container_width=True):
        st.session_state.page = "tours"
        st.rerun()
    
    if st.button("🧭 Tour Guides", key="nav_guides_list", use_container_width=True):
        st.session_state.page = "tour_guides"
        st.rerun()
    
    st.markdown("---")
    st.markdown("**🌟 Explore**")
    
    if st.button("⭐ Attractions", key="nav_attractions", use_container_width=True):
        st.session_state.page = "attractions"
        st.rerun()
    
    if st.button("🍛 Food & Cuisine", key="nav_food", use_container_width=True):
        st.session_state.page = "food"
        st.rerun()
    
    if st.button("📹 Videos", key="nav_videos", use_container_width=True):
        st.session_state.page = "videos"
        st.rerun()
    
    if st.button("📅 Events Calendar", key="nav_events", use_container_width=True):
        st.session_state.page = "events"
        st.rerun()
    
    if st.button("📝 Blog & Tips", key="nav_blog", use_container_width=True):
        st.session_state.page = "blog"
        st.rerun()
    
    st.markdown("---")
    st.markdown("**🛠️ Travel Tools**")
    
    if st.button("🗣️ Phrases", key="nav_phrases", use_container_width=True):
        st.session_state.page = "phrases"
        st.rerun()
    
    if st.button("💱 Currency", key="nav_currency", use_container_width=True):
        st.session_state.page = "currency"
        st.rerun()
    
    if st.button("🎒 Packing List", key="nav_packing", use_container_width=True):
        st.session_state.page = "packing"
        st.rerun()
    
    if st.button("🗺️ Maps", key="nav_maps", use_container_width=True):
        st.session_state.page = "maps"
        st.rerun()
    
    if st.button("🌤️ Weather Forecast", key="nav_weather", use_container_width=True):
        st.session_state.page = "weather"
        st.rerun()
    
    st.markdown("---")
    st.markdown("**❓ Help**")
    
    if st.button("❓ FAQ", key="nav_faq", use_container_width=True):
        st.session_state.page = "faq"
        st.rerun()
    
    if st.button("🔒 Privacy Policy", key="nav_privacy", use_container_width=True):
        st.session_state.page = "privacy"
        st.rerun()
    
    st.markdown("---")
    st.markdown("**🏢 Directory**")
    
    if st.button("🏪 Local Businesses", key="nav_directory", use_container_width=True):
        st.session_state.page = "directory"
        st.rerun()
    
    if st.button("⭐ Reviews", key="nav_reviews", use_container_width=True):
        st.session_state.page = "reviews"
        st.rerun()
    
    if st.button("📧 Contact Us", key="nav_contact", use_container_width=True):
        st.session_state.page = "contact"
        st.rerun()
    
    st.markdown("---")
    
    # Weather with loading indicator
    with st.spinner("🌤️"):
        w = get_live_weather()
    icon = get_weather_icon(w.get("weather_code", 0))
    if w.get("success"):
        st.markdown(f"**{icon} {w.get('temperature', 28)}°C** Banjul")
    else:
        st.markdown(f"**{icon} ~28°C** Banjul _(offline)_")
    
    # Exchange rates with loading indicator
    with st.spinner("💵"):
        r = get_exchange_rates()
    if r.get("success"):
        st.markdown(f"**💵 {r['USD']['rate']:.0f} GMD** per $1")
    else:
        st.markdown(f"**💵 ~65 GMD** per $1 _(offline)_")
    
    st.markdown("---")
    st.markdown("**🚨 Emergency**")
    st.markdown("🚔 Police: **117**")
    st.markdown("🚑 Ambulance: **116**")
    st.markdown("🚒 Fire: **118**")

# ============== MAIN CONTENT ==============
page = st.session_state.page

# ============== HOME PAGE ==============
if page == "home":
    st.markdown("")
    st.markdown("")
    
    st.markdown("<h1 style='text-align:center; font-size:2.25rem; font-weight:500; color:#333;'>Welcome to TGTA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.25rem; color:#666; margin-bottom:0.5rem;'>The Gambia Travel Assistant</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1rem; color:#888; margin-bottom:2rem;'>🌟 Your AI-Powered Gambia Travel Guide 🌟</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        query = st.text_input("Search", key="home_search", placeholder="Ask about places, history, culture, travel...", label_visibility="collapsed")
        
        if st.button("🔍 Search", use_container_width=True, type="primary"):
            if query:
                st.session_state.search_query = query
                st.session_state.page = "results"
                st.rerun()
    
    ALL_TOP_QUERIES = [
        ("Is Gambia safe?", "is gambia safe"), ("Do I need visa?", "visa"), ("Best time to visit?", "best time to visit"),
        ("Day trip ideas", "day trip"), ("How far is Basse?", "how far"), ("Coming from Senegal", "from senegal"),
        ("Best beaches", "best beach"), ("Best hotels", "best hotel"), ("Where to stay?", "where to stay"),
        ("Kunta Kinteh Island", "kunta kinteh"), ("Things to do", "things to do"), ("What to see?", "things to do"),
        ("Currency & money", "money"), ("Getting around", "getting around"), ("Local food", "food"),
        ("History of Gambia", "history"), ("Culture & people", "culture"),
        ("Serekunda", "serekunda"), ("Banjul", "banjul"), ("Kololi", "kololi"),
    ]
    
    st.markdown("")
    st.markdown("<p style='text-align:center; color:#888; margin-bottom:1rem;'>🔥 Popular questions tourists ask:</p>", unsafe_allow_html=True)
    
    random.seed(datetime.now().minute // 5)
    random_suggestions = random.sample(ALL_TOP_QUERIES, 5)
    random.seed()
    
    cols = st.columns([0.3, 1, 1, 1, 1, 1, 0.3])
    
    for idx, (label, search_term) in enumerate(random_suggestions):
        with cols[idx + 1]:
            if st.button(label, key=f"suggest_{idx}", use_container_width=True):
                st.session_state.search_query = search_term
                st.session_state.page = "results"
                st.rerun()

# ============== SEARCH RESULTS PAGE ==============
elif page == "results":
    query = st.session_state.get("search_query", "The Gambia")
    
    col_back, col_home, col_space = st.columns([1, 1, 3])
    with col_back:
        if st.button("← Back", key="back_btn", use_container_width=True):
            st.session_state.page = "home"
            if "search_query" in st.session_state:
                del st.session_state.search_query
            st.rerun()
    with col_home:
        if st.button("🏠 Home", key="home_btn_results", use_container_width=True):
            st.session_state.page = "home"
            if "search_query" in st.session_state:
                del st.session_state.search_query
            st.rerun()
    
    st.markdown("---")
    
    # Try Knowledge Base first
    kb_result = None
    if KB_LOADED:
        kb_result = get_smart_answer(query)
    
    if kb_result and kb_result.get("answer") and kb_result.get("confidence", 0) >= 0.5:
        title = query.title() if len(query) < 50 else kb_result.get("matched", query).replace("_", " ").title()
        
        st.markdown(f"## {title}")
        st.markdown(kb_result["answer"])
        
        suggestions = get_suggestions(query) if KB_LOADED else []
        if suggestions:
            st.markdown("---")
            st.markdown("**Related questions:**")
            sugg_cols = st.columns(len(suggestions))
            for i, sugg in enumerate(suggestions):
                with sugg_cols[i]:
                    if st.button(sugg.replace("_", " ").title(), key=f"sugg_{i}", use_container_width=True):
                        st.session_state.search_query = sugg
                        st.rerun()
        
        st.markdown("---")
        share_cols = st.columns(3)
        with share_cols[0]:
            if st.button("📱 WhatsApp", key="share_wa", use_container_width=True):
                wa_text = urllib.parse.quote(f"{title} - The Gambia Travel Assistant")
                st.markdown(f'<meta http-equiv="refresh" content="0;url=https://wa.me/?text={wa_text}">', unsafe_allow_html=True)
        with share_cols[1]:
            if st.button("🐦 Twitter", key="share_tw", use_container_width=True):
                tw_text = urllib.parse.quote(f"{title} - The Gambia Travel Assistant")
                st.markdown(f'<meta http-equiv="refresh" content="0;url=https://twitter.com/intent/tweet?text={tw_text}">', unsafe_allow_html=True)
        with share_cols[2]:
            if st.button("📋 Copy Text", key="copy_text", use_container_width=True):
                st.code(f"{title}\n\n{kb_result['answer'][:200]}...\n\n- The Gambia Travel Assistant", language=None)
    
    else:
        # Fall back to Wikipedia
        with st.spinner(f"Searching for '{query}'..."):
            wiki = search_gambia_wikipedia(query)
        
        if wiki.get("success"):
            st.markdown(f"## {wiki['title']}")
            if wiki.get("image"):
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    st.markdown(wiki.get("summary", ""))
                with col_img:
                    st.image(wiki["image"], use_container_width=True)
            else:
                st.markdown(wiki.get("summary", ""))
            
            st.markdown(f"\n\n*Source: [Wikipedia]({wiki.get('url', '')})*")
        else:
            st.warning(f"I couldn't find specific information about '{query}'.")
            st.markdown("**Try asking about:**")
            st.markdown("- Visa requirements, safety, best time to visit")
            st.markdown("- Beaches, hotels, things to do")

# ============== TRAVEL GUIDES PAGE ==============
elif page == "guides":
    st.markdown("# 📖 Travel Guides")
    st.markdown("Essential information for your trip to The Gambia")
    st.markdown("---")
    
    tabs = st.tabs(["🛂 Visa", "💰 Money", "☀️ Weather", "🛡️ Safety", "🚕 Transport", "🏖️ Beaches", "🍛 Food", "💉 Health"])
    keys = ["visa", "money", "weather", "is gambia safe", "getting around", "best beach", "food", "vaccines"]
    
    for i, tab in enumerate(tabs):
        with tab:
            if KB_LOADED and keys[i] in QUICK_ANSWERS:
                st.markdown(QUICK_ANSWERS[keys[i]])
            else:
                st.info("Guide coming soon!")

# ============== HOTELS PAGE ==============
elif page == "hotels":
    st.markdown("# 🏨 Hotels & Accommodation")
    st.markdown("Find the perfect place to stay in The Gambia")
    st.markdown("---")
    
    # Accommodation type tabs
    acc_tabs = st.tabs(["🏨 Hotels", "🏠 Airbnb & Rentals", "🔍 Search All"])
    
    with acc_tabs[0]:
        filt = st.selectbox("Filter by:", ["All Hotels", "5 Star Luxury", "4 Star", "3 Star", "Budget"])
        
        for h in HOTELS:
            show = filt == "All Hotels" or \
                   (filt == "5 Star Luxury" and h["stars"] == 5) or \
                   (filt == "4 Star" and h["stars"] == 4) or \
                   (filt == "3 Star" and h["stars"] == 3) or \
                   (filt == "Budget" and h["stars"] <= 2)
            
            if show:
                st.markdown(f"""<div class="hotel-card">
                    <h3 style="margin:0;">{h['name']} {"⭐" * h['stars']}</h3>
                    <p style="margin:0.5rem 0; color:#666;">📍 {h['area']} &nbsp;|&nbsp; 💵 {h['price']}/night</p>
                    <p style="margin:0.5rem 0;">✨ {h['feat']}</p>
                    <a href="{h['url']}" target="_blank" class="book-btn">📅 Book on Booking.com</a>
                </div>""", unsafe_allow_html=True)
    
    with acc_tabs[1]:
        st.markdown("### 🏠 Vacation Rentals & Airbnb")
        st.markdown("Perfect for longer stays, families, or those wanting a local experience!")
        
        st.markdown("""
        <div class="hotel-card">
            <h3 style="margin:0;">🏠 Airbnb in The Gambia</h3>
            <p style="margin:0.5rem 0;">Find apartments, villas, and unique stays across The Gambia</p>
            <p style="margin:0.5rem 0; color:#666;">
                ✨ Full kitchens • 🏊 Private pools • 👨‍👩‍👧 Family friendly • 💰 Often cheaper for groups
            </p>
            <a href="https://www.airbnb.com/s/Gambia/homes" target="_blank" class="book-btn" style="background:#FF5A5F;">🏠 Browse Airbnb</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📍 Popular Areas for Rentals")
        
        areas = [
            {"area": "Kololi", "desc": "Tourist hub, restaurants, nightlife", "best": "First-timers"},
            {"area": "Fajara", "desc": "Upscale, quieter, expat area", "best": "Long stays"},
            {"area": "Bijilo", "desc": "Beach access, modern, growing", "best": "Families"},
            {"area": "Brufut", "desc": "Local feel, authentic, cheaper", "best": "Budget travelers"},
            {"area": "Sanyang", "desc": "Beach village, peaceful, surfing", "best": "Beach lovers"},
        ]
        
        for a in areas:
            st.markdown(f"**📍 {a['area']}** - {a['desc']} | Best for: *{a['best']}*")
        
        st.markdown("---")
        st.link_button("🏠 Search Airbnb Gambia", "https://www.airbnb.com/s/Gambia/homes", use_container_width=True, type="primary")
    
    with acc_tabs[2]:
        st.markdown("### 🔍 Compare All Booking Sites")
        st.markdown("Find the best deals across multiple platforms:")
        
        search_cols = st.columns(2)
        with search_cols[0]:
            st.link_button("🔵 Booking.com", "https://www.booking.com/country/gm.html", use_container_width=True)
            st.link_button("🏠 Airbnb", "https://www.airbnb.com/s/Gambia/homes", use_container_width=True)
            st.link_button("🟢 TripAdvisor", "https://www.tripadvisor.com/SmartDeals-g293794-Gambia-Hotel-Deals.html", use_container_width=True)
        with search_cols[1]:
            st.link_button("🟠 Agoda", "https://www.agoda.com/country/gambia.html", use_container_width=True)
            st.link_button("🔴 Hotels.com", "https://www.hoteles.com/en/co10233059/hotels-in-gambia/", use_container_width=True)
            st.link_button("🟡 Expedia", "https://www.expedia.com/Destinations-In-Gambia.d63.Hotel-Destinations", use_container_width=True)
        
        search_cols2 = st.columns(2)
        with search_cols2[0]:
            st.link_button("🌴 Lastminute", "https://www.lastminute.com/holidays/gm_gambia", use_container_width=True)
        
        st.markdown("---")
        st.markdown("**💡 Pro Tip:** Check Booking.com for hotels, Airbnb for apartments & villas!")

# ============== TOURS PAGE ==============
elif page == "tours":
    st.markdown("# 🎫 Book Tours & Excursions")
    st.markdown("Experience the best of The Gambia with guided tours")
    st.markdown("---")
    
    for t in TOURS:
        st.markdown(f"""<div class="hotel-card">
            <h3 style="margin:0;">🎫 {t['name']}</h3>
            <p style="margin:0.5rem 0; color:#666;">🏷️ {t['type']} &nbsp;|&nbsp; ⏱️ {t['duration']} &nbsp;|&nbsp; 💵 {t['price']}</p>
            <a href="{t['url']}" target="_blank" class="book-btn">📅 Book Now</a>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**More tours:** [GetYourGuide](https://getyourguide.com/gambia) • [Viator](https://viator.com/Gambia)")

# ============== ATTRACTIONS PAGE ==============
elif page == "attractions":
    st.markdown("# ⭐ Must-See Attractions")
    st.markdown("Discover the best of The Gambia")
    st.markdown("---")
    
    # Social sharing - clickable buttons
    st.markdown("**📤 Share this page:**")
    render_social_buttons("Must-See Attractions in The Gambia - Travel Guide")
    st.markdown("---")
    
    for a in ATTRACTIONS:
        with st.expander(f"**{a['name']}** - {a['type']}"):
            st.markdown(f"**📝 Description:** {a['desc']}")
            st.markdown(f"**💵 Cost:** {a['cost']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📖 Learn more about {a['name']}", key=f"attr_{a['name']}"):
                    st.session_state.search_query = a['name']
                    st.session_state.page = "results"
                    st.rerun()
            with col2:
                st.link_button(f"📍 View on Map", f"https://www.google.com/maps/search/{urllib.parse.quote(a['name'] + ' Gambia')}")

# ============== FLIGHTS PAGE ==============
elif page == "flights":
    st.markdown("# ✈️ Flights to The Gambia")
    st.markdown("Find the best flights to Banjul International Airport (BJL)")
    st.markdown("---")
    
    # Flight search box
    st.markdown("### 🔍 Search Flights")
    search_cols = st.columns([2, 2, 1])
    with search_cols[0]:
        origin = st.text_input("From", placeholder="London, New York, Paris...")
    with search_cols[1]:
        travel_date = st.date_input("Travel Date")
    with search_cols[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if search_clicked and origin:
        st.markdown("### Search on these sites:")
        link_cols = st.columns(4)
        with link_cols[0]:
            st.markdown(f"[🔵 **Skyscanner**](https://www.skyscanner.com/transport/flights/{origin.lower()[:3]}/bjl/{travel_date.strftime('%y%m%d')}/)")
        with link_cols[1]:
            st.markdown(f"[🟠 **Kayak**](https://www.kayak.com/flights/{origin[:3].upper()}-BJL/{travel_date})")
        with link_cols[2]:
            st.markdown(f"[🔴 **Google Flights**](https://www.google.com/travel/flights?q=flights%20from%20{origin}%20to%20banjul)")
        with link_cols[3]:
            st.markdown(f"[🟡 **Expedia**](https://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:{origin},to:BJL)")
    
    st.markdown("---")
    st.markdown("### 🛫 Airlines Flying to Banjul")
    
    for airline in AIRLINES:
        st.markdown(f"""<div class="hotel-card">
            <h3 style="margin:0;">{airline['logo']} {airline['name']}</h3>
            <p style="margin:0.5rem 0; color:#666;">
                📍 From: <strong>{airline['from']}</strong> &nbsp;|&nbsp;
                📅 {airline['freq']} &nbsp;|&nbsp;
                ⏱️ {airline['flight']}
            </p>
            <p style="margin:0.5rem 0;">💵 Typical price: <strong>{airline['price']}</strong></p>
            <a href="{airline['url']}" target="_blank" class="book-btn">🔗 Visit Airline</a>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Booking Tips")
    
    tip_cols = st.columns(2)
    with tip_cols[0]:
        st.markdown("""
        **✈️ Best Routes:**
        - 🇬🇧 **UK:** Direct from Gatwick (TUI, seasonal)
        - 🇪🇺 **Europe:** Via Brussels or Casablanca
        - 🇺🇸 **USA:** Via Brussels, Istanbul, or Casablanca
        - 🇸🇳 **Senegal:** 30min flight from Dakar
        """)
    with tip_cols[1]:
        st.markdown("""
        **💰 Save Money:**
        - Book **2-3 months** in advance
        - **Tuesday/Wednesday** flights cheapest
        - **Nov-Apr** is peak season (pricier)
        - Use **Skyscanner** for best comparison
        """)
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Flight Search")
    quick_cols = st.columns(4)
    with quick_cols[0]:
        st.link_button("🔵 Skyscanner", "https://www.skyscanner.com/transport/flights/-/bjl/", use_container_width=True)
    with quick_cols[1]:
        st.link_button("🟠 Kayak", "https://www.kayak.com/explore/BJL", use_container_width=True)
    with quick_cols[2]:
        st.link_button("🔴 Google Flights", "https://www.google.com/travel/flights?q=flights%20to%20banjul", use_container_width=True)
    with quick_cols[3]:
        st.link_button("🟡 Expedia", "https://www.expedia.com/Destinations-In-Gambia.d63.Flight-Destinations", use_container_width=True)
    
    st.markdown("---")
    
    hotel_col1, hotel_col2 = st.columns([3, 1])
    with hotel_col1:
        st.info("**🏠 Need accommodation too?** Check our Hotels page for the best places to stay!")
    with hotel_col2:
        if st.button("🏨 Go to Hotels", key="go_hotels_flights", use_container_width=True):
            st.session_state.page = "hotels"
            st.rerun()

# ============== FOOD & CUISINE PAGE ==============
elif page == "food":
    st.markdown("# 🍛 Food & Cuisine")
    st.markdown("Taste the flavors of The Gambia!")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🍽️ Must-Try Dishes", "🥤 Drinks", "🏪 Where to Eat"])
    
    with tab1:
        for dish in FOOD_DATA["dishes"]:
            st.markdown(f"""<div class="hotel-card">
                <h3 style="margin:0;">{dish['name']} <span style="color:#888; font-weight:normal;">({dish['aka']})</span></h3>
                <p style="margin:0.5rem 0;">{dish['desc']}</p>
                <p style="margin:0; color:#666;">💵 {dish['price']} &nbsp;|&nbsp; 🏷️ {dish['try']}</p>
            </div>""", unsafe_allow_html=True)
    
    with tab2:
        for drink in FOOD_DATA["drinks"]:
            st.markdown(f"""<div class="hotel-card">
                <h3 style="margin:0;">{drink['name']} <span style="color:#888; font-weight:normal;">({drink['aka']})</span></h3>
                <p style="margin:0.5rem 0;">{drink['desc']}</p>
                <p style="margin:0; color:#666;">💵 {drink['price']}</p>
            </div>""", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🏪 Best Places to Try Local Food")
        for market in FOOD_DATA["markets"]:
            st.markdown(f"**📍 {market['name']}** - {market['desc']}")
        
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        st.markdown("- Always try **Benachin** - it's the national dish!")
        st.markdown("- Accept **Attaya** tea if offered - it's rude to refuse")
        st.markdown("- Street food is safe at busy stalls")
        st.markdown("- Wash hands before eating (often communal dishes)")

# ============== CURRENCY CONVERTER PAGE ==============
elif page == "currency":
    st.markdown("# 💱 Currency Converter")
    st.markdown("Gambian Dalasi (GMD) exchange rates")
    st.markdown("---")
    
    rates = get_exchange_rates()
    
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount", min_value=0.0, value=100.0, step=10.0)
        from_curr = st.selectbox("From", ["USD", "EUR", "GBP", "GMD"])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        to_curr = st.selectbox("To", ["GMD", "USD", "EUR", "GBP"])
    
    if from_curr != to_curr:
        if from_curr == "GMD":
            result = amount / rates.get(to_curr, {}).get("rate", 65)
        elif to_curr == "GMD":
            result = amount * rates.get(from_curr, {}).get("rate", 65)
        else:
            gmd_amount = amount * rates.get(from_curr, {}).get("rate", 65)
            result = gmd_amount / rates.get(to_curr, {}).get("rate", 65)
        
        st.markdown(f"### {amount:,.2f} {from_curr} = **{result:,.2f} {to_curr}**")
    
    st.markdown("---")
    st.markdown("### Current Rates (approximate)")
    
    rate_cols = st.columns(3)
    with rate_cols[0]:
        st.metric("🇺🇸 USD", f"{rates['USD']['rate']:.0f} GMD")
    with rate_cols[1]:
        st.metric("🇪🇺 EUR", f"{rates['EUR']['rate']:.0f} GMD")
    with rate_cols[2]:
        st.metric("🇬🇧 GBP", f"{rates['GBP']['rate']:.0f} GMD")
    
    st.markdown("---")
    st.markdown("**💡 Money Tips:**")
    st.markdown("- 💵 **Bring cash** (USD/EUR/GBP) - ATMs unreliable")
    st.markdown("- 🏦 Change money at banks or authorized bureaus")
    st.markdown("- 💳 Cards only work at large hotels/restaurants")
    st.markdown("- 🚫 Don't change money on the street")
    st.markdown("- 💰 Budget: $50-100/day comfortable")

# ============== PHRASES PAGE ==============
elif page == "phrases":
    st.markdown("# 🗣️ Useful Phrases")
    st.markdown("Learn some local language - locals will love it!")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🇬🇲 Mandinka", "🇬🇲 Wolof", "🇮🇹 Italian Visitors"])
    
    with tab1:
        st.markdown("### Essential Mandinka Phrases")
        for p in PHRASES["mandinka"]:
            st.markdown(f"""<div class="hotel-card">
                <h4 style="margin:0; color:#333;">🇬🇧 English: {p['english']}</h4>
                <p style="margin:0.25rem 0; font-size:1.25rem; color:#3A7728;"><strong>🇬🇲 Mandinka: {p['local']}</strong></p>
                <p style="margin:0; color:#888; font-style:italic;">Pronunciation: "{p['pronun']}"</p>
            </div>""", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Essential Wolof Phrases")
        for p in PHRASES["wolof"]:
            st.markdown(f"""<div class="hotel-card">
                <h4 style="margin:0; color:#333;">🇬🇧 English: {p['english']}</h4>
                <p style="margin:0.25rem 0; font-size:1.25rem; color:#3A7728;"><strong>🇬🇲 Wolof: {p['local']}</strong></p>
                <p style="margin:0; color:#888; font-style:italic;">Pronunciation: "{p['pronun']}"</p>
            </div>""", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🇮🇹 Per i Turisti Italiani")
        st.markdown("*Frasi utili - Italian to English to Mandinka*")
        st.markdown("")
        for p in ITALIAN_PHRASES:
            st.markdown(f"""<div class="hotel-card">
                <h4 style="margin:0; color:#333;">🇮🇹 Italiano: {p['italian']}</h4>
                <p style="margin:0.25rem 0;">🇬🇧 English: <strong>{p['english']}</strong></p>
                <p style="margin:0; font-size:1.1rem; color:#3A7728;">🇬🇲 Mandinka: <strong>{p['mandinka']}</strong></p>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Language Tips")
    st.markdown("- **English** is the official language - you'll be fine everywhere!")
    st.markdown("- Saying **'Abaraka'** (thank you in Mandinka) will make everyone smile")
    st.markdown("- **'Toubab'** means foreigner - it's not offensive, just descriptive")
    st.markdown("- Learning greetings shows respect and opens doors to authentic experiences")
    st.markdown("")
    st.info("🎯 **Pro Tip:** Book a Tour Guide who speaks your language for deeper cultural immersion!")
    if st.button("🧭 Browse Tour Guides", key="phrases_to_guides"):
        st.session_state.page = "tour_guides"
        st.rerun()

# ============== PACKING LIST PAGE ==============
elif page == "packing":
    st.markdown("# 🎒 Packing Checklist")
    st.markdown("Everything you need for The Gambia")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✈️ Essentials")
        for item in PACKING_LIST["essentials"]:
            st.checkbox(item, key=f"pack_{item}")
        
        st.markdown("### 👕 Clothing")
        for item in PACKING_LIST["clothing"]:
            st.checkbox(item, key=f"pack_{item}")
    
    with col2:
        st.markdown("### 💊 Health")
        for item in PACKING_LIST["health"]:
            st.checkbox(item, key=f"pack_{item}")
        
        st.markdown("### 🔧 Useful Items")
        for item in PACKING_LIST["useful"]:
            st.checkbox(item, key=f"pack_{item}")
    
    st.markdown("---")
    st.markdown("**💡 Don't Forget:**")
    st.markdown("- 🔌 **UK-style plugs** (Type G) are used")
    st.markdown("- 💵 **€40 cash** for Tourism Levy (€20 in + €20 out)")
    st.markdown("- 💊 **Start malaria tablets** before you leave!")
    st.markdown("- 📱 **Download offline maps** - internet can be spotty")

# ============== EVENTS CALENDAR PAGE ==============
elif page == "events":
    st.markdown("# 📅 Events & Festivals")
    st.markdown("Plan your trip around The Gambia's best events!")
    st.markdown("---")
    
    filter_type = st.selectbox("Filter by type:", ["All Events", "Festival", "Cultural", "Religious", "National", "Tourism", "Nature", "Sports"])
    
    for event in EVENTS:
        show = filter_type == "All Events" or event["type"] == filter_type
        if show:
            type_emoji = {"Festival": "🎉", "Cultural": "🎭", "Religious": "🕌", "National": "🇬🇲", "Tourism": "✈️", "Nature": "🦜", "Sports": "🎣"}.get(event["type"], "📅")
            st.markdown(f"""<div class="hotel-card">
                <h3 style="margin:0;">{type_emoji} {event['event']}</h3>
                <p style="margin:0.25rem 0; color:#3A7728; font-weight:500;">📅 {event['month']}</p>
                <p style="margin:0.5rem 0;">{event['desc']}</p>
                <span style="background:#e8f5e9; padding:0.25rem 0.5rem; border-radius:4px; font-size:0.8rem;">{event['type']}</span>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**💡 Tips:**")
    st.markdown("- 🕌 **Ramadan dates change** yearly - check Islamic calendar")
    st.markdown("- 🎉 **Book early** for Independence Day & Roots Festival")
    st.markdown("- 🦜 **Best birding:** November to April")
    st.markdown("- 🏖️ **Peak season:** November to February")

# ============== LOCAL DIRECTORY PAGE ==============
elif page == "directory":
    st.markdown("# 🏪 Local Business Directory")
    st.markdown("Discover trusted local businesses in The Gambia")
    st.markdown("---")
    
    # Category filter
    categories = list(set([b["cat"] for b in LOCAL_BUSINESSES]))
    categories.insert(0, "All Categories")
    
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        selected_cat = st.selectbox("Filter by Category", categories)
    with filter_col2:
        show_featured = st.checkbox("⭐ Featured Only", value=False)
    
    st.markdown("---")
    
    # Filter businesses
    filtered_businesses = LOCAL_BUSINESSES
    if selected_cat != "All Categories":
        filtered_businesses = [b for b in filtered_businesses if b["cat"] == selected_cat]
    if show_featured:
        filtered_businesses = [b for b in filtered_businesses if b["featured"]]
    
    # Display businesses
    if filtered_businesses:
        # Featured businesses first
        featured = [b for b in filtered_businesses if b["featured"]]
        regular = [b for b in filtered_businesses if not b["featured"]]
        
        if featured:
            st.markdown("### ⭐ Featured Businesses")
            for biz in featured:
                st.markdown(f"""<div class="hotel-card" style="border-left:4px solid gold;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <h3 style="margin:0;">⭐ {biz['name']}</h3>
                            <span style="background:#e8f4ea; color:#2e7d32; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem;">
                                {biz['cat']}
                            </span>
                        </div>
                    </div>
                    <p style="margin:0.5rem 0; color:#666;">{biz['desc']}</p>
                    <p style="margin:0.25rem 0;">📍 <strong>{biz['area']}</strong></p>
                    <a href="{biz['website']}" target="_blank" class="book-btn">🔍 Find Contact Info</a>
                </div>""", unsafe_allow_html=True)
            st.markdown("---")
        
        if regular:
            st.markdown("### 📋 All Businesses")
            for biz in regular:
                st.markdown(f"""<div class="hotel-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <h3 style="margin:0;">{biz['name']}</h3>
                            <span style="background:#f0f0f0; color:#666; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem;">
                                {biz['cat']}
                            </span>
                        </div>
                    </div>
                    <p style="margin:0.5rem 0; color:#666;">{biz['desc']}</p>
                    <p style="margin:0.25rem 0;">📍 <strong>{biz['area']}</strong></p>
                    <a href="{biz['website']}" target="_blank" class="book-btn">🔍 Find Contact Info</a>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No businesses found matching your criteria.")
    
    # List your business CTA
    st.markdown("---")
    st.markdown("""<div style="background:linear-gradient(135deg, #1a472a 0%, #2d5016 100%); color:white; padding:2rem; border-radius:12px; text-align:center;">
        <h2 style="margin:0 0 1rem 0; color:white;">🏢 List Your Business</h2>
        <p style="margin:0 0 1rem 0; font-size:1.1rem;">
            Get your business in front of thousands of travelers visiting The Gambia!
        </p>
        <p style="margin:0 0 1rem 0;">
            ⭐ <strong>Featured Listing:</strong> Top placement + golden badge<br>
            📋 <strong>Standard Listing:</strong> Free basic listing
        </p>
    </div>""", unsafe_allow_html=True)
    
    if st.button("📝 Contact Us to List Your Business", type="primary", use_container_width=True):
        st.session_state.page = "contact"
        st.rerun()

# ============== TOUR GUIDES PAGE ==============
elif page == "tour_guides":
    st.markdown("# 🧭 Tour Guides Directory")
    st.markdown("Connect with experienced local guides for authentic Gambian experiences")
    st.markdown("---")
    
    # Filter options
    specialties = list(set([g["specialty"] for g in TOUR_GUIDES]))
    specialties.insert(0, "All Specialties")
    
    filter_cols = st.columns([2, 2, 1])
    with filter_cols[0]:
        selected_specialty = st.selectbox("Specialty", specialties)
    with filter_cols[1]:
        selected_area = st.selectbox("Area", ["All Areas", "Banjul", "Coastal", "Upcountry", "Nationwide"])
    with filter_cols[2]:
        verified_only = st.checkbox("✅ Verified", value=False)
    
    st.markdown("---")
    
    # Filter guides
    filtered_guides = TOUR_GUIDES
    if selected_specialty != "All Specialties":
        filtered_guides = [g for g in filtered_guides if g["specialty"] == selected_specialty]
    if selected_area != "All Areas":
        filtered_guides = [g for g in filtered_guides if selected_area.lower() in g["area"].lower()]
    if verified_only:
        filtered_guides = [g for g in filtered_guides if g["featured"]]
    
    # Display guides
    if filtered_guides:
        # Featured guides first
        featured = [g for g in filtered_guides if g["featured"]]
        regular = [g for g in filtered_guides if not g["featured"]]
        
        if featured:
            st.markdown("### ⭐ Featured Guides")
            for guide in featured:
                lang_badges = " ".join([f"<span style='background:#e3f2fd; color:#1565c0; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem; margin-right:0.25rem;'>{lang.strip()}</span>" for lang in guide["langs"].split(",")])
                
                st.markdown(f"""<div class="hotel-card" style="border-left:4px solid gold;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <h3 style="margin:0;">⭐ {guide['name']}</h3>
                            <span style="background:#e8f4ea; color:#2e7d32; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem;">
                                {guide['specialty']}
                            </span>
                            <span style="background:#fff3e0; color:#e65100; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem; margin-left:0.5rem;">
                                {guide['exp']}
                            </span>
                        </div>
                        <div style="text-align:right;">
                            <strong style="color:#2e7d32; font-size:1.2rem;">{guide['price']}</strong>
                        </div>
                    </div>
                    <p style="margin:0.75rem 0 0.5rem 0; color:#666;">{guide['bio']}</p>
                    <p style="margin:0.25rem 0;">📍 Area: <strong>{guide['area']}</strong></p>
                    <p style="margin:0.25rem 0;">🗣️ Languages: {lang_badges}</p>
                    <button class="book-btn" style="margin-top:0.75rem;">📧 Contact Guide</button>
                </div>""", unsafe_allow_html=True)
            st.markdown("---")
        
        if regular:
            st.markdown("### 🗺️ All Tour Guides")
            for guide in regular:
                lang_badges = " ".join([f"<span style='background:#e3f2fd; color:#1565c0; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem; margin-right:0.25rem;'>{lang.strip()}</span>" for lang in guide["langs"].split(",")])
                
                st.markdown(f"""<div class="hotel-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <h3 style="margin:0;">{guide['name']}</h3>
                            <span style="background:#f0f0f0; color:#666; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem;">
                                {guide['specialty']}
                            </span>
                            <span style="background:#fff3e0; color:#e65100; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.8rem; margin-left:0.5rem;">
                                {guide['exp']}
                            </span>
                        </div>
                        <div style="text-align:right;">
                            <strong style="color:#2e7d32; font-size:1.2rem;">{guide['price']}</strong>
                        </div>
                    </div>
                    <p style="margin:0.75rem 0 0.5rem 0; color:#666;">{guide['bio']}</p>
                    <p style="margin:0.25rem 0;">📍 Area: <strong>{guide['area']}</strong></p>
                    <p style="margin:0.25rem 0;">🗣️ Languages: {lang_badges}</p>
                    <button class="book-btn" style="margin-top:0.75rem;">📧 Contact Guide</button>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No guides found matching your criteria.")
    
    # Become a guide CTA
    st.markdown("---")
    st.markdown("""<div style="background:linear-gradient(135deg, #1a472a 0%, #2d5016 100%); color:white; padding:2rem; border-radius:12px; text-align:center;">
        <h2 style="margin:0 0 1rem 0; color:white;">🧭 Become a Listed Guide</h2>
        <p style="margin:0 0 1rem 0; font-size:1.1rem;">
            Are you a licensed tour guide in The Gambia? Join our directory!
        </p>
        <p style="margin:0 0 1rem 0;">
            ⭐ <strong>Premium Profile:</strong> Featured placement + verified badge<br>
            📋 <strong>Basic Profile:</strong> Free listing in our directory
        </p>
    </div>""", unsafe_allow_html=True)
    
    if st.button("📝 Apply to Join", type="primary", use_container_width=True):
        st.session_state.page = "contact"
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Hiring a Guide Tips")
    tips_cols = st.columns(2)
    with tips_cols[0]:
        st.markdown("""
        **✅ What to expect:**
        - Local knowledge & history
        - Language translation help
        - Safety & navigation
        - Restaurant/shop recommendations
        - Photography spots
        """)
    with tips_cols[1]:
        st.markdown("""
        **💰 Typical costs:**
        - Half-day tour: $20-40
        - Full-day tour: $40-80
        - Multi-day upcountry: $50-100/day
        - Specialized (birding): $60-100/day
        - Prices include guide only (not transport)
        """)

# ============== VIDEOS PAGE ==============
elif page == "videos":
    st.markdown("# 📹 Videos & Travel Guides")
    st.markdown("Watch videos to plan your perfect Gambia trip!")
    st.markdown("---")
    
    # Category filter
    video_cats = ["All Videos"] + list(set([v["cat"] for v in YOUTUBE_VIDEOS]))
    selected_vid_cat = st.selectbox("Filter by Topic", video_cats)
    
    # Filter videos
    filtered_vids = YOUTUBE_VIDEOS
    if selected_vid_cat != "All Videos":
        filtered_vids = [v for v in YOUTUBE_VIDEOS if v["cat"] == selected_vid_cat]
    
    st.markdown("---")
    
    # Display videos in grid
    for i in range(0, len(filtered_vids), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(filtered_vids):
                vid = filtered_vids[i + j]
                with col:
                    st.markdown(f"""<div class="hotel-card">
                        <h4 style="margin:0 0 0.5rem 0;">{vid['title']}</h4>
                        <p style="margin:0; color:#666; font-size:0.85rem;">📺 {vid['channel']} | 🏷️ {vid['cat']}</p>
                        <p style="margin:0.5rem 0; font-size:0.9rem;">{vid['desc']}</p>
                    </div>""", unsafe_allow_html=True)
                    # YouTube embed
                    st.video(f"https://www.youtube.com/watch?v={vid['id']}")
    
    st.markdown("---")
    st.markdown("### 🎬 More Gambia Content")
    st.markdown("""<div style="background:#f8f9fa; padding:1.5rem; border-radius:10px;">
        <p style="margin:0 0 1rem 0;">Subscribe to these channels for more Gambia travel content:</p>
        <p style="margin:0.25rem 0;">▶️ <strong>Visit The Gambia</strong> - Official tourism channel</p>
        <p style="margin:0.25rem 0;">▶️ <strong>Gambia Tourism Board</strong> - Travel guides & events</p>
        <p style="margin:0.25rem 0;">▶️ <strong>Travel Gambia</strong> - Independent travel vlogs</p>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("**💡 Tip:** Planning a trip? Watch our destination videos to see exactly what to expect!")

# ============== REVIEWS PAGE ==============
elif page == "reviews":
    st.markdown("# ⭐ Traveler Reviews")
    st.markdown("Real experiences from visitors to The Gambia")
    st.markdown("---")
    
    # Review filters
    filter_cols = st.columns([2, 2, 1])
    with filter_cols[0]:
        review_type = st.selectbox("Category", ["All Reviews", "Hotels", "Tour Guides", "Restaurants", "Attractions"])
    with filter_cols[1]:
        rating_filter = st.selectbox("Rating", ["All Ratings", "5 Stars", "4+ Stars", "3+ Stars"])
    with filter_cols[2]:
        verified_only = st.checkbox("Verified", value=False, key="verified_reviews")
    
    # Map filter to type
    type_map = {"Hotels": "hotel", "Tour Guides": "guide", "Restaurants": "business", "Attractions": "attraction"}
    
    # Filter reviews
    filtered_reviews = REVIEWS
    if review_type != "All Reviews":
        filtered_reviews = [r for r in filtered_reviews if r["type"] == type_map.get(review_type, "")]
    if rating_filter == "5 Stars":
        filtered_reviews = [r for r in filtered_reviews if r["rating"] == 5]
    elif rating_filter == "4+ Stars":
        filtered_reviews = [r for r in filtered_reviews if r["rating"] >= 4]
    elif rating_filter == "3+ Stars":
        filtered_reviews = [r for r in filtered_reviews if r["rating"] >= 3]
    if verified_only:
        filtered_reviews = [r for r in filtered_reviews if r["verified"]]
    
    st.markdown("---")
    
    # Summary stats
    if filtered_reviews:
        avg_rating = sum([r["rating"] for r in filtered_reviews]) / len(filtered_reviews)
        stat_cols = st.columns(4)
        with stat_cols[0]:
            st.metric("Total Reviews", len(filtered_reviews))
        with stat_cols[1]:
            st.metric("Average Rating", f"{avg_rating:.1f} ⭐")
        with stat_cols[2]:
            five_star = len([r for r in filtered_reviews if r["rating"] == 5])
            st.metric("5-Star Reviews", five_star)
        with stat_cols[3]:
            verified = len([r for r in filtered_reviews if r["verified"]])
            st.metric("Verified", f"{verified} ✓")
        
        st.markdown("---")
        
        # Display reviews
        for review in filtered_reviews:
            stars = "⭐" * review["rating"]
            verified_badge = ' <span style="background:#e8f5e9; color:#2e7d32; padding:0.1rem 0.4rem; border-radius:3px; font-size:0.75rem;">✓ Verified</span>' if review["verified"] else ""
            type_badge = review["type"].capitalize()
            
            st.markdown(f"""<div class="hotel-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <h4 style="margin:0;">{review['item']}</h4>
                        <span style="background:#f0f0f0; color:#666; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.75rem;">{type_badge}</span>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:1.1rem;">{stars}</span>
                    </div>
                </div>
                <p style="margin:0.75rem 0; font-style:italic; color:#333;">"{review['text']}"</p>
                <p style="margin:0; color:#888; font-size:0.85rem;">
                    — <strong>{review['author']}</strong>{verified_badge} • {review['date']}
                </p>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No reviews found matching your criteria.")
    
    # Write a review CTA
    st.markdown("---")
    st.markdown("### ✍️ Write a Review")
    st.markdown("""<div style="background:linear-gradient(135deg, #1a472a 0%, #2d5016 100%); color:white; padding:2rem; border-radius:12px;">
        <h3 style="margin:0 0 1rem 0; color:white;">Share Your Experience!</h3>
        <p style="margin:0 0 1rem 0;">Been to The Gambia? Help other travelers by sharing your honest review of hotels, guides, restaurants, or attractions.</p>
        <p style="margin:0;">📧 Email your review to <strong>reviews@gambia-travel-guide.com</strong> or use our contact form!</p>
    </div>""", unsafe_allow_html=True)
    
    if st.button("📝 Submit a Review", type="primary", use_container_width=True):
        st.session_state.page = "contact"
        st.rerun()

# ============== CONTACT PAGE ==============
elif page == "contact":
    st.markdown("# 📧 Contact Us")
    st.markdown("Get in touch for custom trips, questions, or partnerships")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Send us a message")
        
        name = st.text_input("Your Name *", placeholder="John Smith")
        email = st.text_input("Email Address *", placeholder="john@example.com")
        subject = st.selectbox("Subject", [
            "General Inquiry",
            "Custom Trip Planning", 
            "Hotel/Tour Booking Help",
            "Business Partnership",
            "List My Business",
            "Report an Issue",
            "Other"
        ])
        message = st.text_area("Your Message *", placeholder="Tell us how we can help you...", height=150)
        
        if st.button("📤 Send Message", type="primary", use_container_width=True):
            if name and email and message:
                # In production, this would send to email/database
                st.success("✅ Message sent! We'll get back to you within 24 hours.")
                st.balloons()
            else:
                st.error("Please fill in all required fields (*)")
        
        st.markdown("---")
        st.markdown("### 📬 Subscribe to Newsletter")
        st.markdown("Get travel tips, deals, and updates about The Gambia")
        
        news_cols = st.columns([3, 1])
        with news_cols[0]:
            newsletter_email = st.text_input("Email", placeholder="your@email.com", label_visibility="collapsed", key="newsletter")
        with news_cols[1]:
            if st.button("Subscribe", use_container_width=True):
                if newsletter_email and "@" in newsletter_email:
                    st.success("✅ Subscribed!")
                else:
                    st.error("Enter valid email")
    
    with col2:
        st.markdown("### Quick Contact")
        st.markdown("""
        **� Email:**  
        info@gambia-travel-guide.com
        
        **🌐 Social Media:**
        """)
        st.link_button("📘 Facebook", "https://www.facebook.com/visitthegambia", use_container_width=True)
        st.link_button("📸 Instagram", "https://www.instagram.com/visitthegambia", use_container_width=True)
        st.link_button("🐦 Twitter/X", "https://twitter.com/visitthegambia", use_container_width=True)
        
        st.markdown("---")
        st.markdown("""
        **🏢 For Businesses:**  
        Want to list your hotel, tour, or service?  
        Contact us for partnership opportunities!
        
        ---
        
        **⏰ Response Time:**  
        Usually within 24 hours
        """)

# ============== FAQ PAGE ==============
elif page == "faq":
    st.markdown("# ❓ Frequently Asked Questions")
    st.markdown("Everything you need to know before visiting The Gambia")
    st.markdown("---")
    
    # Category filter
    faq_cats = ["All Questions"] + list(set([f["cat"] for f in FAQ_DATA]))
    selected_faq_cat = st.selectbox("Filter by topic:", faq_cats)
    
    filtered_faqs = FAQ_DATA if selected_faq_cat == "All Questions" else [f for f in FAQ_DATA if f["cat"] == selected_faq_cat]
    
    st.markdown("---")
    
    for faq in filtered_faqs:
        with st.expander(f"**{faq['q']}**"):
            st.markdown(faq['a'])
            st.markdown(f"<span style='background:#e8f4ea; color:#2e7d32; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem;'>{faq['cat']}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🤔 Still have questions?")
    if st.button("📧 Contact Us", key="faq_contact"):
        st.session_state.page = "contact"
        st.rerun()

# ============== BLOG/TIPS PAGE ==============
elif page == "blog":
    st.markdown("# 📝 Travel Tips & Blog")
    st.markdown("Expert advice for your Gambia adventure")
    st.markdown("---")
    
    # Category filter
    blog_cats = ["All Articles"] + list(set([b["cat"] for b in BLOG_TIPS]))
    selected_blog_cat = st.selectbox("Filter by topic:", blog_cats)
    
    filtered_blogs = BLOG_TIPS if selected_blog_cat == "All Articles" else [b for b in BLOG_TIPS if b["cat"] == selected_blog_cat]
    
    st.markdown("---")
    
    for blog in filtered_blogs:
        st.markdown(f"""<div class="hotel-card">
            <span style="background:#e3f2fd; color:#1565c0; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem;">{blog['cat']}</span>
            <span style="color:#888; font-size:0.8rem; margin-left:0.5rem;">⏱️ {blog['read_time']} read</span>
            <h3 style="margin:0.5rem 0;">{blog['title']}</h3>
            <p style="margin:0; color:#666;">{blog['excerpt']}</p>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("📚 **More content coming soon!** Subscribe to our newsletter to get new articles delivered to your inbox.")
    if st.button("📬 Subscribe to Newsletter", key="blog_newsletter"):
        st.session_state.page = "contact"
        st.rerun()

# ============== MAPS PAGE ==============
elif page == "maps":
    st.markdown("# 🗺️ Maps & Locations")
    st.markdown("Find your way around The Gambia")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📍 Interactive Map", "🏨 Hotels Map", "⭐ Attractions Map"])
    
    with tab1:
        st.markdown("### The Gambia Overview")
        st.markdown("""
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d496485.0507823066!2d-16.80191895!3d13.4549273!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xec29cf48e35b6ef%3A0x5a4b4e4a85b70b8a!2sThe%20Gambia!5e0!3m2!1sen!2s!4v1704200000000!5m2!1sen!2s" width="100%" height="450" style="border:0; border-radius:10px;" allowfullscreen="" loading="lazy"></iframe>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.markdown("**📍 Key Areas:**")
        cols = st.columns(3)
        with cols[0]:
            st.markdown("🏛️ **Banjul** - Capital city")
            st.markdown("🏖️ **Kololi** - Tourist area")
            st.markdown("🌴 **Kotu** - Beach resort area")
        with cols[1]:
            st.markdown("🏘️ **Serrekunda** - Largest city")
            st.markdown("🎨 **Fajara** - Upscale area")
            st.markdown("🏝️ **Cape Point** - Quiet beach")
        with cols[2]:
            st.markdown("🌿 **Bijilo** - Nature reserve")
            st.markdown("🎣 **Brufut** - Fishing village")
            st.markdown("🏞️ **Upcountry** - River region")
    
    with tab2:
        st.markdown("### Hotel Areas")
        st.markdown("""
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d62058.80461832578!2d-16.7438!3d13.4348!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xec2a9ab0e15d51d%3A0x3c0b2a7c9e0b2e8d!2sKololi%2C%20The%20Gambia!5e0!3m2!1sen!2s!4v1704200000000!5m2!1sen!2s" width="100%" height="400" style="border:0; border-radius:10px;" allowfullscreen="" loading="lazy"></iframe>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("🏨 Browse All Hotels", key="maps_hotels"):
            st.session_state.page = "hotels"
            st.rerun()
    
    with tab3:
        st.markdown("### Major Attractions")
        st.markdown("""
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d248242.5253911533!2d-16.9!3d13.4!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xec29cf48e35b6ef%3A0x5a4b4e4a85b70b8a!2sThe%20Gambia!5e0!3m2!1sen!2s!4v1704200000000!5m2!1sen!2s" width="100%" height="400" style="border:0; border-radius:10px;" allowfullscreen="" loading="lazy"></iframe>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("⭐ View All Attractions", key="maps_attractions"):
            st.session_state.page = "attractions"
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📱 Offline Maps")
    st.markdown("Download maps for offline use:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("📍 Google Maps", "https://maps.google.com/maps?q=the+gambia", use_container_width=True)
    with col2:
        st.link_button("🗺️ Maps.me", "https://maps.me/", use_container_width=True)
    with col3:
        st.link_button("🧭 OpenStreetMap", "https://www.openstreetmap.org/#map=9/13.4/-16.6", use_container_width=True)

# ============== WEATHER PAGE ==============
elif page == "weather":
    st.markdown("# 🌤️ Weather Forecast")
    st.markdown("Plan your activities with the 7-day forecast")
    st.markdown("---")
    
    # Current weather
    w = get_live_weather()
    icon = get_weather_icon(w.get("weather_code", 0))
    
    st.markdown("### 📍 Current Weather in Banjul")
    wcols = st.columns(4)
    with wcols[0]:
        st.metric("Temperature", f"{w.get('temperature', 28)}°C")
    with wcols[1]:
        st.metric("Humidity", f"{w.get('humidity', 70)}%")
    with wcols[2]:
        st.metric("Wind", f"{w.get('wind_speed', 15)} km/h")
    with wcols[3]:
        st.metric("Conditions", icon)
    
    st.markdown("---")
    st.markdown("### 📅 7-Day Forecast")
    
    # Fetch 7-day forecast
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 13.4549, "longitude": -16.5790,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
            "timezone": "GMT", "forecast_days": 7
        }
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json().get("daily", {})
            dates = data.get("time", [])
            max_temps = data.get("temperature_2m_max", [])
            min_temps = data.get("temperature_2m_min", [])
            rain_probs = data.get("precipitation_probability_max", [])
            codes = data.get("weather_code", [])
            
            fcols = st.columns(7)
            for i, col in enumerate(fcols):
                if i < len(dates):
                    day_name = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%a")
                    with col:
                        st.markdown(f"**{day_name}**")
                        st.markdown(f"{get_weather_icon(codes[i] if i < len(codes) else 0)}")
                        st.markdown(f"🔺 {max_temps[i]:.0f}°")
                        st.markdown(f"🔻 {min_temps[i]:.0f}°")
                        st.markdown(f"💧 {rain_probs[i]:.0f}%")
        else:
            st.warning("Could not load forecast data")
    except:
        st.warning("Weather forecast temporarily unavailable")
    
    st.markdown("---")
    st.markdown("### 🌴 Seasonal Guide")
    
    scols = st.columns(2)
    with scols[0]:
        st.markdown("""
        **☀️ Dry Season (Nov-May)**
        - Best time to visit!
        - Sunny, 25-35°C daily
        - Very little rain
        - Peak tourism: Dec-Feb
        - Perfect beach weather
        """)
    with scols[1]:
        st.markdown("""
        **🌧️ Rainy Season (Jun-Oct)**
        - Afternoon thunderstorms
        - Lush, green landscapes
        - Fewer tourists
        - Some hotels close
        - Great for photography
        """)
    
    st.info("💡 **Best months:** November to February for perfect weather. March-April still excellent but hotter.")

# ============== PRIVACY POLICY PAGE ==============
elif page == "privacy":
    st.markdown("# 🔒 Privacy Policy")
    st.markdown("*Last updated: January 2026*")
    st.markdown("---")
    
    st.markdown("""
    ### 1. Information We Collect
    
    **The Gambia Travel Assistant** respects your privacy. We collect minimal information:
    
    - **Contact Form Data:** Name, email, and message content when you contact us
    - **Newsletter Subscriptions:** Email addresses for those who subscribe
    - **Analytics:** Anonymous usage data via Google Analytics (page views, device type, location country)
    
    We do **NOT** collect:
    - Payment information (all bookings are through third-party sites)
    - Personal identification beyond what you provide
    - Cookies beyond essential site functionality
    
    ---
    
    ### 2. How We Use Your Information
    
    - Respond to your inquiries
    - Send newsletter updates (only if subscribed)
    - Improve our website and content
    - Understand which content is most helpful
    
    ---
    
    ### 3. Third-Party Services
    
    Our site contains links to:
    - **Booking.com, Skyscanner, GetYourGuide** - for hotel/flight/tour bookings
    - **Google Maps** - for location services
    - **YouTube** - for video content
    
    These services have their own privacy policies. We are not responsible for their practices.
    
    ---
    
    ### 4. Data Security
    
    We implement reasonable security measures to protect your information. However, no internet transmission is 100% secure.
    
    ---
    
    ### 5. Your Rights
    
    You can:
    - Request deletion of your data
    - Unsubscribe from newsletters at any time
    - Contact us with privacy concerns
    
    ---
    
    ### 6. Contact
    
    For privacy questions, contact us at: **privacy@gambia-travel-guide.com**
    """)
    
    st.markdown("---")
    if st.button("📧 Contact Us About Privacy", key="privacy_contact"):
        st.session_state.page = "contact"
        st.rerun()

# ============== FOOTER ==============
st.markdown("---")

# Newsletter signup section
st.markdown("### 📬 Stay Updated")
st.markdown("Get travel tips, deals, and updates about The Gambia")
news_col1, news_col2, news_col3 = st.columns([1, 2, 1])
with news_col2:
    footer_news_cols = st.columns([3, 1])
    with footer_news_cols[0]:
        footer_newsletter = st.text_input("Email for newsletter", placeholder="your@email.com", label_visibility="collapsed", key="footer_newsletter")
    with footer_news_cols[1]:
        if st.button("📧 Subscribe", key="footer_sub", use_container_width=True):
            if footer_newsletter and "@" in footer_newsletter:
                st.success("✅ Subscribed! Check your email.")
            else:
                st.error("Enter valid email")

st.markdown("---")

# Quick feedback
feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 2, 1])
with feedback_col2:
    with st.expander("💬 Quick Feedback - Help us improve!"):
        feedback_rating = st.select_slider("How useful is this app?", options=["😞 Not useful", "😐 Okay", "🙂 Good", "😊 Very Good", "🤩 Excellent"], value="🙂 Good")
        feedback_text = st.text_area("Any suggestions?", placeholder="Tell us what you'd like to see...", height=80, key="feedback_text")
        if st.button("📤 Send Feedback", key="send_feedback", use_container_width=True):
            if feedback_text:
                st.success("✅ Thank you for your feedback!")
            else:
                st.info("Thanks for rating us!")

st.markdown('<div class="flag-bar"></div>', unsafe_allow_html=True)

# Social media and footer
footer_cols = st.columns([1, 2, 1])
with footer_cols[1]:
    st.markdown("**🌐 Follow The Gambia Tourism:**")
    social_cols = st.columns(4)
    with social_cols[0]:
        st.link_button("📘 Facebook", "https://www.facebook.com/visitthegambia", use_container_width=True)
    with social_cols[1]:
        st.link_button("📸 Instagram", "https://www.instagram.com/visitthegambia", use_container_width=True)
    with social_cols[2]:
        st.link_button("🐦 Twitter/X", "https://twitter.com/visitthegambia", use_container_width=True)
    with social_cols[3]:
        st.link_button("▶️ YouTube", "https://www.youtube.com/@visitthegambia", use_container_width=True)
    
    st.markdown("""
    <div style="text-align:center; padding:0.5rem 0;">
        <p style="color:#888; font-size:0.85rem; margin:0;">
            ✈️ TGTA - The Gambia Travel Assistant | <a href='https://gambia-travel-guide.com'>gambia-travel-guide.com</a>
        </p>
        <p style="color:#aaa; font-size:0.75rem; margin-top:0.25rem;">
            © 2026 TGTA | Your AI-Powered Gambia Travel Guide | <a href='https://visitthegambia.gm'>Official Tourism Board</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
