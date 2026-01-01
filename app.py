"""
✈️ The Gambia Travel Assistant (TGTA)
Professional Travel Guide - Smiling Coast of Africa
Expert conversational Q&A with smart knowledge base
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
    page_title="The Gambia Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colors - Gambian Flag
RED = "#CE1126"
BLUE = "#0C1C8C"
GREEN = "#3A7728"

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

HOTELS = [
    {"name": "Coco Ocean Resort & Spa", "area": "Bijilo", "stars": 5, "price": "$120-200", "feat": "Beach, Pool, Spa", "url": "https://www.booking.com/hotel/gm/coco-ocean-resort-spa.html"},
    {"name": "Senegambia Beach Hotel", "area": "Kololi", "stars": 4, "price": "$80-150", "feat": "Beach, Pool", "url": "https://www.booking.com/hotel/gm/senegambia-beach.html"},
    {"name": "Sunset Beach Hotel", "area": "Kotu", "stars": 4, "price": "$70-120", "feat": "Beach, Family", "url": "https://www.booking.com/hotel/gm/sunset-beach.html"},
    {"name": "Kombo Beach Hotel", "area": "Kotu", "stars": 3, "price": "$50-90", "feat": "Pool, Garden", "url": "https://www.booking.com/hotel/gm/kombo-beach.html"},
    {"name": "Luigi's Guesthouse", "area": "Kololi", "stars": 2, "price": "$25-50", "feat": "Budget", "url": "https://www.booking.com/hotel/gm/luigis-guesthouse.html"},
    {"name": "Ngala Lodge", "area": "Fajara", "stars": 4, "price": "$90-140", "feat": "Boutique, Garden", "url": "https://www.booking.com/hotel/gm/ngala-lodge.html"},
    {"name": "Bakotu Hotel", "area": "Kotu", "stars": 3, "price": "$45-80", "feat": "Pool, Birding", "url": "https://www.booking.com/hotel/gm/bakotu.html"},
    {"name": "Ocean Bay Hotel", "area": "Cape Point", "stars": 4, "price": "$75-130", "feat": "Beach, Pool", "url": "https://www.booking.com/hotel/gm/ocean-bay.html"},
    {"name": "Mandina Lodges", "area": "Makasutu", "stars": 5, "price": "$150-250", "feat": "Eco-Lodge, River", "url": "https://www.booking.com/hotel/gm/mandina-lodges.html"},
    {"name": "Lemon Creek Hotel", "area": "Bijilo", "stars": 3, "price": "$55-95", "feat": "Pool, Restaurant", "url": "https://www.booking.com/hotel/gm/lemon-creek.html"},
]

TOURS = [
    {"name": "Kunta Kinteh Island Day Trip", "type": "Heritage", "price": "$45-65", "duration": "Full Day", "url": "https://www.getyourguide.com"},
    {"name": "Makasutu Culture Forest", "type": "Eco-Tour", "price": "$55-75", "duration": "Half Day", "url": "https://www.viator.com"},
    {"name": "River Gambia Cruise", "type": "Nature", "price": "$35-50", "duration": "3-4 hours", "url": "https://www.getyourguide.com"},
    {"name": "Abuko Nature Reserve", "type": "Wildlife", "price": "$20-30", "duration": "Half Day", "url": "https://www.viator.com"},
    {"name": "Banjul City Tour", "type": "Culture", "price": "$25-40", "duration": "3-4 hours", "url": "https://www.getyourguide.com"},
    {"name": "Tanji Fishing Village", "type": "Local Life", "price": "$20-35", "duration": "Half Day", "url": "https://www.viator.com"},
]

ATTRACTIONS = [
    {"name": "Kunta Kinteh Island", "type": "UNESCO Heritage", "desc": "Historic slave trade site from the novel 'Roots'", "cost": "$15-25"},
    {"name": "Abuko Nature Reserve", "type": "Wildlife", "desc": "Forest with monkeys, birds, crocodiles", "cost": "$5-10"},
    {"name": "Makasutu Culture Forest", "type": "Eco-tourism", "desc": "Sacred forest, boat rides, village life", "cost": "$40-60"},
    {"name": "Kololi Beach", "type": "Beach", "desc": "Main tourist beach with restaurants and bars", "cost": "Free"},
    {"name": "Albert Market", "type": "Culture", "desc": "Banjul's largest market for crafts and goods", "cost": "Free"},
    {"name": "Bijilo Forest Park", "type": "Wildlife", "desc": "Family-friendly monkey walk near the coast", "cost": "$3-5"},
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
    st.markdown("### ✈️ The Gambia")
    st.markdown("*Smiling Coast of Africa*")
    st.markdown("---")
    
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    if st.button("📖 Travel Guides", key="nav_guides", use_container_width=True):
        st.session_state.page = "guides"
        st.rerun()
    
    if st.button("🏨 Hotels", key="nav_hotels", use_container_width=True):
        st.session_state.page = "hotels"
        st.rerun()
    
    if st.button("⭐ Attractions", key="nav_attractions", use_container_width=True):
        st.session_state.page = "attractions"
        st.rerun()
    
    if st.button("🎫 Book Tours", key="nav_tours", use_container_width=True):
        st.session_state.page = "tours"
        st.rerun()
    
    st.markdown("---")
    
    w = get_live_weather()
    r = get_exchange_rates()
    icon = get_weather_icon(w.get("weather_code", 0))
    
    st.markdown(f"**{icon} {w.get('temperature', 28)}°C** Banjul")
    st.markdown(f"**💵 {r['USD']['rate']:.0f} GMD** per $1")
    
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
    
    st.markdown("<h1 style='text-align:center; font-size:2.25rem; font-weight:500; color:#333;'>I'm your Gambia Travel Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.5rem; color:#666; margin-bottom:2rem;'>How can I help you today?</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        query = st.text_input("Search", key="home_search", placeholder="Ask about places, history, culture, travel...", label_visibility="collapsed")
        
        if st.button("🔍 Search", use_container_width=True, type="primary"):
            if query:
                st.session_state.search_query = query
                st.session_state.page = "results"
                st.rerun()
    
    ALL_TOP_QUERIES = [
        ("Is Gambia safe?", "safety"), ("Do I need visa?", "visa"), ("Best time to visit?", "weather"),
        ("Day trip ideas", "day_trip"), ("How far is Basse?", "distances"), ("Coming from Senegal", "distances"),
        ("Best beaches", "beaches"), ("Best hotels", "hotels"), ("Where to stay?", "accommodation"),
        ("Kunta Kinteh Island", "Kunta Kinteh"), ("Things to do", "attractions"), ("What to see?", "tourism"),
        ("Currency & money", "money"), ("Getting around", "transport"), ("Local food", "food"),
        ("History of Gambia", "history"), ("Culture & people", "culture"),
        ("Serekunda", "Serekunda"), ("Banjul", "Banjul"), ("Kololi", "Kololi"),
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
                <a href="{h['url']}" target="_blank" class="book-btn">📅 Book Now</a>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**More options:** [Booking.com](https://booking.com/country/gm.html) • [Airbnb](https://airbnb.com/s/Gambia) • [TripAdvisor](https://tripadvisor.com/Hotels-g293786)")

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
    
    for a in ATTRACTIONS:
        with st.expander(f"**{a['name']}** - {a['type']}"):
            st.markdown(f"**Description:** {a['desc']}")
            st.markdown(f"**Cost:** {a['cost']}")
            
            if st.button(f"📖 Learn more about {a['name']}", key=f"attr_{a['name']}"):
                st.session_state.search_query = a['name']
                st.session_state.page = "results"
                st.rerun()

# ============== FOOTER ==============
st.markdown("---")
st.markdown('<div class="flag-bar"></div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; font-size:0.85rem;'>✈️ The Gambia Travel Assistant | <a href='https://visitthegambia.gm'>Official Tourism Board</a></p>", unsafe_allow_html=True)
