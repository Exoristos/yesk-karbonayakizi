"""
app.py — Carbon Footprint Calculator & Analytics Dashboard (v3)
Green Economy and Sustainability Club | Boğaziçi University Demo
"""

import streamlit as st
import pandas as pd
import numpy as np
import json, os
import plotly.graph_objects as go
import plotly.express as px

# ─────────────────────── config ───────────────────────
st.set_page_config(page_title="Carbon Footprint Dashboard", page_icon="🌍",
                   layout="wide", initial_sidebar_state="expanded")

BASE = os.path.dirname(__file__)

@st.cache_data
def load_factors():
    with open(os.path.join(BASE, "data", "complex_factors.json"), "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_db():
    return pd.read_csv(os.path.join(BASE, "data", "complex_emissions.csv"))

F  = load_factors()
df = load_db()

# ═══════════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════════
LANG = {
  "en": {
    "page_title": "🌍 Carbon Footprint Dashboard",
    "page_subtitle": "Green Economy & Sustainability Club — Marmara University",
    "badge": "📊 DATASET: 1,500 SYNTHETIC PROFILES · 5 CATEGORIES · 22 FEATURES",
    "sidebar_title": "🌿 Lifestyle Inputs",
    "sidebar_caption": "Adjust the parameters below to estimate your daily carbon footprint.",
    "lang_label": "🌐 Language / Dil",
    # Expander titles
    "exp_transport": "🚗 Transportation",
    "exp_tech": "💻 Tech & Energy",
    "exp_lifestyle": "🛍️ Lifestyle & Hobbies",
    "exp_fashion": "👗 Fashion & Shopping",
    "exp_diet": "🥗 Diet & Health",
    # Transport
    "lbl_route": "Commute route",
    "lbl_km": "Daily distance (km)",
    "lbl_flights": "Flights per year (short/med)",
    # Tech
    "lbl_pc": "Primary computer",
    "lbl_gaming": "Heavy gaming (h/day)",
    "lbl_study": "Study / light use (h/day)",
    "lbl_phone": "Phone type",
    "lbl_charges": "Phone charges per day",
    "lbl_heating": "Home heating type",
    # Lifestyle
    "lbl_dj": "DJ / music production (h/day)",
    "lbl_board": "New board games / month",
    "lbl_stream": "Streaming / YouTube (h/day)",
    "lbl_recycle": "Recycling habits",
    "lbl_shower": "Average shower (minutes)",
    # Fashion
    "lbl_clothes": "Clothing items bought / month",
    "lbl_style": "Fashion style",
    "lbl_perfume": "Cosmetics / perfume shipping",
    # Diet
    "lbl_diet": "Diet type",
    "lbl_coffee": "Coffee cups / day",
    "lbl_smoke": "I am a smoker",
    # Cards
    "card_transport": "Transport",
    "card_tech": "Tech",
    "card_lifestyle": "Lifestyle",
    "card_fashion": "Fashion",
    "card_diet": "Diet",
    "card_total": "Total Daily",
    "card_unit": "kg CO₂ / day",
    # Charts
    "gauge_title": "Total Daily Footprint",
    "treemap_title": "Emission Breakdown (Treemap)",
    "radar_title": "You vs. Average Student",
    "bar_title": "Category Comparison",
    "legend_you": "You",
    "legend_avg": "Avg Student",
    "xaxis_label": "kg CO₂ / day",
    # Dataset explorer
    "explorer_title": "📂 Explore Raw Dataset (1,500 profiles)",
    "footer": "Synthetic dataset · Built with Streamlit · Plotly · Pandas | YESK – Green Economy & Sustainability Club",
    # Treemap sub-items
    "sub_commute": "Commute",
    "sub_flight": "Flights",
    "sub_pc": "PC / Laptop",
    "sub_phone": "Phone Charging",
    "sub_heating": "Home Heating",
    "sub_dj": "DJ / Music",
    "sub_board": "Board Games",
    "sub_streaming": "Streaming",
    "sub_recycle": "Recycling",
    "sub_shower": "Hot Showers",
    "sub_clothing": "Clothing",
    "sub_perfume": "Perfume Ship.",
    "sub_food": "Food",
    "sub_coffee": "Coffee",
    "sub_smoking": "Smoking",
    # Enhancements
    "msg_success": "Awesome! Your carbon footprint is below average. 🌿",
    "msg_motivate": "You're slightly above average. Small steps can make a big difference! 💪",
    "rec_title": "💡 Personalized Tip",
    "rec_transport": "Your transport emissions are high. Consider using public transit, carpooling, or cycling more often.",
    "rec_tech": "Your tech/energy usage is high. Try unplugging devices and reducing screen time.",
    "rec_lifestyle": "Your lifestyle emissions stand out. Consider more sustainable hobbies.",
    "rec_fashion": "Your fashion footprint is high. Try thrifting, buying less, or choosing sustainable brands.",
    "rec_diet": "Diet makes up most of your footprint. Shifting to plant-based meals even a few times a week helps immensely.",
    "cta_title": "🌱 Join YESK!",
    "cta_text": "Did you like this app? Follow Green Economy & Sustainability Club on Instagram and join our events!",
    "cta_button": "Follow @marmarayesk",
  },
  "tr": {
    "page_title": "🌍 Karbon Ayak İzi Panosu",
    "page_subtitle": "Yeşil Ekonomi ve Sürdürülebilirlik Kulübü — Marmara Üniversitesi",
    "badge": "📊 VERİ: 1.500 SENTETİK PROFİL · 5 KATEGORİ · 22 ÖZELLİK",
    "sidebar_title": "🌿 Yaşam Tarzı Girdileri",
    "sidebar_caption": "Günlük karbon ayak izinizi hesaplamak için parametreleri ayarlayın.",
    "lang_label": "🌐 Language / Dil",
    # Expander titles
    "exp_transport": "🚗 Ulaşım",
    "exp_tech": "💻 Teknoloji ve Enerji",
    "exp_lifestyle": "🛍️ Yaşam Tarzı ve Hobiler",
    "exp_fashion": "👗 Moda ve Alışveriş",
    "exp_diet": "🥗 Beslenme ve Sağlık",
    # Transport
    "lbl_route": "Ulaşım güzergahı",
    "lbl_km": "Günlük mesafe (km)",
    "lbl_flights": "Yıllık uçuş sayısı (kısa/orta)",
    # Tech
    "lbl_pc": "Birincil bilgisayar",
    "lbl_gaming": "Yoğun oyun (saat/gün)",
    "lbl_study": "Ders / hafif kullanım (saat/gün)",
    "lbl_phone": "Telefon tipi",
    "lbl_charges": "Günlük telefon şarj sayısı",
    "lbl_heating": "Ev ısınma tipi",
    # Lifestyle
    "lbl_dj": "DJ / müzik prodüksiyonu (saat/gün)",
    "lbl_board": "Aylık yeni kutu oyun sayısı",
    "lbl_stream": "Dizi / YouTube izleme (saat/gün)",
    "lbl_recycle": "Geri dönüşüm alışkanlığı",
    "lbl_shower": "Ortalama duş süresi (dk)",
    # Fashion
    "lbl_clothes": "Aylık satın alınan kıyafet",
    "lbl_style": "Moda tarzı",
    "lbl_perfume": "Kozmetik / parfüm kargosu",
    # Diet
    "lbl_diet": "Diyet tipi",
    "lbl_coffee": "Günlük kahve (fincan)",
    "lbl_smoke": "Sigara içiyorum",
    # Cards
    "card_transport": "Ulaşım",
    "card_tech": "Teknoloji",
    "card_lifestyle": "Yaşam",
    "card_fashion": "Moda",
    "card_diet": "Beslenme",
    "card_total": "Günlük Toplam",
    "card_unit": "kg CO₂ / gün",
    # Charts
    "gauge_title": "Günlük Toplam Ayak İzi",
    "treemap_title": "Emisyon Dağılımı (Ağaç Harita)",
    "radar_title": "Sen vs. Ortalama Öğrenci",
    "bar_title": "Kategori Karşılaştırması",
    "legend_you": "Sen",
    "legend_avg": "Ort. Öğrenci",
    "xaxis_label": "kg CO₂ / gün",
    # Dataset explorer
    "explorer_title": "📂 Ham Veri Seti (1.500 profil)",
    "footer": "Sentetik veri · Streamlit · Plotly · Pandas ile yapıldı | YESK – Yeşil Ekonomi ve Sürdürülebilirlik Kulübü",
    # Treemap sub-items
    "sub_commute": "Ulaşım",
    "sub_flight": "Uçuşlar",
    "sub_pc": "PC / Laptop",
    "sub_phone": "Telefon Şarjı",
    "sub_heating": "Ev Isıtma",
    "sub_dj": "DJ / Müzik",
    "sub_board": "Kutu Oyun",
    "sub_streaming": "Dizi İzleme",
    "sub_recycle": "Geri Dönüşüm",
    "sub_shower": "Sıcak Duş",
    "sub_clothing": "Kıyafet",
    "sub_perfume": "Parfüm Kargosu",
    "sub_food": "Yemek",
    "sub_coffee": "Kahve",
    "sub_smoking": "Sigara",
    # Enhancements
    "msg_success": "Harika! Karbon ayak izin ortalama bir öğrencinin altında. Böyle devam et! 🌿",
    "msg_motivate": "Ayak izin ortalamanın biraz üzerinde. Ufak adımlarla büyük farklar yaratabilirsin! 💪",
    "rec_title": "💡 Sana Özel Tavsiyemiz",
    "rec_transport": "En yüksek emisyonun ulaşımdan geliyor. Toplu taşıma, yürüyüş veya bisikleti daha sık tercih edebilirsin.",
    "rec_tech": "Teknoloji tüketimin yüksek. Cihazları fişten çekmek veya ekran süresini azaltmak harika bir başlangıç olabilir.",
    "rec_lifestyle": "Yaşam tarzı ve hobi emisyonların dikkat çekiyor. Daha sürdürülebilir alternatiflere yönelebilirsin.",
    "rec_fashion": "Moda kaynaklı ayak izin yüksek. İkinci el kıyafetlere şans verebilir veya daya yavaş moda tercih edebilirsin.",
    "rec_diet": "Beslenme alışkanlıkların emisyonunu artırıyor. Haftada birkaç gün etsiz beslenmek bile devasa etki yaratır.",
    "cta_title": "🌱 YESK'e Katıl!",
    "cta_text": "Bu uygulamayı sevdin mi? Yeşil Ekonomi ve Sürdürülebilirlik Kulübü'nü (YESK) Instagram'da takip et ve etkinliklerimize katıl!",
    "cta_button": "@marmarayesk Takip Et",
  },
}

# Translated dropdown options (key = factors JSON key, value shown in UI)
DROPDOWN_TR = {
    # Commute routes
    "Marmaray + Metro (cross-city)": "Marmaray + Metro (şehirler arası)",
    "Ferry + Bus": "Vapur + Otobüs",
    "Metrobüs": "Metrobüs",
    "Bus Only": "Sadece Otobüs",
    "Personal Car (Gasoline)": "Özel Araç (Benzinli)",
    "Personal Car (Diesel)": "Özel Araç (Dizel)",
    "Personal Car (Hybrid)": "Özel Araç (Hibrit)",
    "Electric Scooter / E-Bike": "Elektrikli Scooter / E-Bisiklet",
    "Walking / Cycling": "Yürüyüş / Bisiklet",
    # PC types
    "High-End Gaming Laptop": "Üst Seviye Oyun Laptopı",
    "Mid-Range Gaming Laptop": "Orta Seviye Oyun Laptopı",
    "Standard Office Laptop": "Standart Ofis Laptopı",
    "Ultrabook / Thin Laptop": "İnce / Ultrabook Laptop",
    "Desktop Gaming PC": "Masaüstü Oyun Bilgisayarı",
    "Desktop Office PC": "Masaüstü Ofis Bilgisayarı",
    "Tablet Only": "Sadece Tablet",
    # Phone
    "Flagship Phone (5000 mAh)": "Amiral Gemisi Telefon (5000 mAh)",
    "Mid-Range Phone (4500 mAh)": "Orta Segment Telefon (4500 mAh)",
    "Budget Phone (4000 mAh)": "Bütçe Dostu Telefon (4000 mAh)",
    # Heating
    "Dormitory (Shared)": "KYK / Paylaşımlı Yurt",
    "Apartment (Natural Gas)": "Öğrenci Evi (Doğalgaz)",
    "Apartment (Electric)": "Öğrenci Evi (Elektrikli Isıtıcı)",
    "Family Home (High Usage)": "Aile Evi (Yoğun Isıtma)",
    # Recycling
    "Strict Recycler": "Her zaman (Kağıt, Plastik, Pil)",
    "Sometimes": "Bazen (Aklıma geldikçe)",
    "Never": "Hiçbir zaman",
    # Diet
    "Heavy Meat Eater": "Yoğun Et Tüketimi",
    "Moderate Meat": "Orta Düzey Et",
    "Pescatarian": "Pesketaryen",
    "Vegetarian": "Vejetaryen",
    "Vegan": "Vegan",
    # Style
    "Streetwear / Heavy Denim": "Sokak Modası / Ağır Denim",
    "Fast Fashion": "Hızlı Moda",
    "Vintage / Thrift": "Vintage / İkinci El",
    "Designer / Luxury": "Tasarım / Lüks",
    "Minimal / Capsule": "Minimal / Kapsül",
    # Perfume shipping
    "Never": "Hiçbir zaman",
    "Rarely (1-2/yr)": "Nadiren (yılda 1-2)",
    "Sometimes (3-6/yr)": "Bazen (yılda 3-6)",
    "Frequently (monthly)": "Sık sık (ayda 1)",
}

# ─────────────────────── CSS ───────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}

.hero{background:linear-gradient(135deg,#0d3b1e 0%,#1b5e20 40%,#2e7d32 70%,#43a047 100%);
      border-radius:18px;padding:36px 28px 30px;text-align:center;color:#fff;margin-bottom:26px;
      box-shadow:0 8px 32px rgba(0,0,0,.25)}
.hero h1{font-size:2.3rem;font-weight:800;margin:0;letter-spacing:-.6px}
.hero p{opacity:.82;margin-top:6px;font-size:.95rem}
.hero .badge{display:inline-block;background:rgba(255,255,255,.18);padding:4px 14px;
             border-radius:20px;font-size:.75rem;margin-top:10px;letter-spacing:.4px}

.cards{display:flex;gap:14px;margin-bottom:26px;flex-wrap:wrap}
.card{flex:1;min-width:150px;background:var(--background-color);border:1px solid var(--secondary-background-color);border-radius:14px;
      padding:20px 14px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,.15);
      transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,.25)}
.card .icon{font-size:1.5rem;margin-bottom:2px}
.card .lbl{font-size:.72rem;text-transform:uppercase;letter-spacing:.6px;opacity:0.8}
.card .val{font-size:1.65rem;font-weight:700;color:#2e7d32;margin:2px 0}
.card .unit{font-size:.7rem;opacity:0.6}
.card.total{border:2px solid #2e7d32;background:rgba(46,125,50,.1)}

.cta-box{background:rgba(46,125,50,.1);border:2px solid rgba(46,125,50,.3);border-radius:12px;padding:24px;text-align:center;margin:30px 0 20px}
.cta-box h3{color:#2e7d32;margin-top:0;font-weight:800;font-size:1.6rem}
.cta-box p{font-size:1.05rem;opacity:0.9}
.cta-btn{display:inline-block;background:#2e7d32;color:#fff !important;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:700;margin-top:10px;transition:.2s;box-shadow:0 4px 12px rgba(46,125,50,.3)}
.cta-btn:hover{background:#1b5e20;transform:translateY(-2px);box-shadow:0 6px 16px rgba(46,125,50,.4)}
.recommendation{background:rgba(255,193,7,.15);border-left:5px solid #ffca28;padding:16px 20px;border-radius:6px;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.recommendation strong{color:#ff8f00;font-size:1.1rem;display:inline-block;margin-bottom:6px}

@media (max-width: 768px){
    .cards{flex-direction:column;gap:10px}
    .card{min-width:100%}
    .hero{padding:24px 16px 20px}
    .hero h1{font-size:1.7rem}
}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# LANGUAGE SELECTOR (top of sidebar)
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    lang_choice = st.radio("🌐 Language / Dil", ["English", "Türkçe"],
                           horizontal=True, label_visibility="visible")
    lang = "tr" if lang_choice == "Türkçe" else "en"
    T = LANG[lang]

# Helper: translate dropdown option
def tr_opt(key):
    """Return translated label if lang=tr, else original key."""
    return DROPDOWN_TR.get(key, key) if lang == "tr" else key

# Build display→key maps for dropdowns
def make_select(options_keys):
    """Return (display_labels, display_to_key_map)"""
    labels = [tr_opt(k) for k in options_keys]
    return labels, dict(zip(labels, options_keys))

# ═══════════════════════════════════════════════════════════
# SIDEBAR — 5 expander groups
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"## {T['sidebar_title']}")
    st.caption(T["sidebar_caption"])

    # ── 1. Transportation ──
    with st.expander(T["exp_transport"], expanded=True):
        route_labels, route_map = make_select(F["commute_co2_per_km"].keys())
        sel_route_label = st.selectbox(T["lbl_route"], route_labels)
        sel_route = route_map[sel_route_label]
        sel_km = st.slider(T["lbl_km"], 0, 150, 18, step=1)
        sel_flight = st.slider(T["lbl_flights"], 0, 20, 1)

    # ── 2. Tech & Energy ──
    with st.expander(T["exp_tech"], expanded=False):
        pc_labels, pc_map = make_select(F["pc_watt"].keys())
        sel_pc_label = st.selectbox(T["lbl_pc"], pc_labels)
        sel_pc = pc_map[sel_pc_label]
        sel_gaming = st.slider(T["lbl_gaming"], 0.0, 14.0, 2.5, step=0.5)
        sel_study  = st.slider(T["lbl_study"], 0.0, 12.0, 4.0, step=0.5)
        phone_labels, phone_map = make_select(F["phone_charge_kwh"].keys())
        sel_phone_label = st.selectbox(T["lbl_phone"], phone_labels)
        sel_phone = phone_map[sel_phone_label]
        sel_charges = st.slider(T["lbl_charges"], 1, 4, 1)
        heat_labels, heat_map = make_select(F["heating_co2_kg_day"].keys())
        sel_heat_label = st.selectbox(T["lbl_heating"], heat_labels)
        sel_heat = heat_map[sel_heat_label]

    # ── 3. Lifestyle & Hobbies ──
    with st.expander(T["exp_lifestyle"], expanded=False):
        sel_dj     = st.slider(T["lbl_dj"], 0.0, 6.0, 0.0, step=0.5)
        sel_board  = st.slider(T["lbl_board"], 0, 8, 1)
        sel_stream = st.slider(T["lbl_stream"], 0.0, 10.0, 3.0, step=0.5)
        rec_labels, rec_map = make_select(F["recycling_offset_kg"].keys())
        sel_rec_label = st.selectbox(T["lbl_recycle"], rec_labels)
        sel_rec = rec_map[sel_rec_label]
        sel_shower = st.slider(T["lbl_shower"], 3, 40, 12)

    # ── 4. Fashion & Shopping ──
    with st.expander(T["exp_fashion"], expanded=False):
        sel_clothes = st.slider(T["lbl_clothes"], 0, 15, 3)
        style_labels, style_map = make_select(F["style_multiplier"].keys())
        sel_style_label = st.selectbox(T["lbl_style"], style_labels)
        sel_style = style_map[sel_style_label]
        perf_labels, perf_map = make_select(F["perfume_shipping_kg_day"].keys())
        sel_perf_label = st.selectbox(T["lbl_perfume"], perf_labels)
        sel_perf = perf_map[sel_perf_label]

    # ── 5. Diet & Health ──
    with st.expander(T["exp_diet"], expanded=False):
        diet_labels, diet_map = make_select(F["diet_base_kg_per_day"].keys())
        sel_diet_label = st.selectbox(T["lbl_diet"], diet_labels)
        sel_diet = diet_map[sel_diet_label]
        sel_coffee = st.slider(T["lbl_coffee"], 0, 8, 2)
        sel_smoke  = st.checkbox(T["lbl_smoke"])

# ═══════════════════════════════════════════════════════════
# CALCULATIONS
# ═══════════════════════════════════════════════════════════
GRID = F["grid_co2_kg_per_kwh"]

transport_co2 = F["commute_co2_per_km"][sel_route] * sel_km / 1000 + (sel_flight * 250) / 365
tech_co2      = ((F["pc_watt"][sel_pc] / 1000) * (sel_gaming + sel_study) * GRID
                + F["phone_charge_kwh"][sel_phone] * sel_charges * GRID
                + F["heating_co2_kg_day"][sel_heat])
lifestyle_co2 = (sel_dj * 0.050 * GRID
                + sel_board / 30 * 5.0
                + sel_stream * 0.055
                + F["recycling_offset_kg"][sel_rec]
                + sel_shower * 0.1)
fashion_co2   = ((sel_clothes / 30) * 15 * F["style_multiplier"][sel_style]
                + F["perfume_shipping_kg_day"][sel_perf])
diet_co2      = (F["diet_base_kg_per_day"][sel_diet]
                + sel_coffee * 0.06
                + (0.3 if sel_smoke else -0.3))

total_co2 = transport_co2 + tech_co2 + lifestyle_co2 + fashion_co2 + diet_co2
avg = F["averages"]

# ═══════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <h1>{T["page_title"]}</h1>
    <p>{T["page_subtitle"]}</p>
    <div class="badge">{T["badge"]}</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# GAMIFICATION & RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════
if total_co2 < avg["total"]:
    if not st.session_state.get("balloons_shown", False):
        st.balloons()
        st.session_state["balloons_shown"] = True
    st.success(T["msg_success"], icon="🎈")
else:
    st.session_state["balloons_shown"] = False
    st.info(T["msg_motivate"], icon="💡")

# Smart Recommendation based on highest category
cat_values = {
    "transport": transport_co2,
    "tech": tech_co2,
    "lifestyle": lifestyle_co2,
    "fashion": fashion_co2,
    "diet": diet_co2
}
max_cat = max(cat_values, key=cat_values.get)
rec_text = T[f"rec_{max_cat}"]

st.markdown(f'''
<div class="recommendation">
    <strong>{T["rec_title"]}</strong><br>
    {rec_text}
</div>
''', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# METRIC CARDS (6 cards)
# ═══════════════════════════════════════════════════════════
cats = [
    ("🚗", T["card_transport"],  transport_co2),
    ("💻", T["card_tech"],       tech_co2),
    ("🎧", T["card_lifestyle"],  lifestyle_co2),
    ("👗", T["card_fashion"],    fashion_co2),
    ("🥗", T["card_diet"],       diet_co2),
]
cards_html = ""
for icon, label, val in cats:
    cards_html += f"""
    <div class="card">
        <div class="icon">{icon}</div>
        <div class="lbl">{label}</div>
        <div class="val">{val:.2f}</div>
        <div class="unit">{T["card_unit"]}</div>
    </div>"""

cards_html += f"""
    <div class="card total">
        <div class="icon">🌍</div>
        <div class="lbl">{T["card_total"]}</div>
        <div class="val">{total_co2:.2f}</div>
        <div class="unit">{T["card_unit"]}</div>
    </div>"""

st.markdown(f'<div class="cards">{cards_html}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# ROW 1 — Gauge + Treemap
# ═══════════════════════════════════════════════════════════
c1, c2 = st.columns(2)

with c1:
    ceiling = max(25, total_co2 * 1.4)
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total_co2,
        number={"suffix": " kg", "font": {"size": 36, "color": "#1b5e20"}},
        delta={"reference": avg["total"], "increasing": {"color": "#c62828"},
               "decreasing": {"color": "#2e7d32"}, "suffix": " kg"},
        title={"text": T["gauge_title"], "font": {"size": 17}},
        gauge={
            "axis": {"range": [0, ceiling], "tickwidth": 1},
            "bar": {"color": "#2e7d32", "thickness": 0.22},
            "bgcolor": "rgba(200,200,200,0.1)", "borderwidth": 1, "bordercolor": "rgba(100,100,100,0.2)",
            "steps": [
                {"range": [0, avg["total"] * 0.6], "color": "rgba(165, 214, 167, 0.4)"},
                {"range": [avg["total"] * 0.6, avg["total"]], "color": "rgba(255, 245, 157, 0.4)"},
                {"range": [avg["total"], ceiling], "color": "rgba(239, 154, 154, 0.4)"},
            ],
            "threshold": {"line": {"color": "#b71c1c", "width": 3},
                          "thickness": 0.8, "value": avg["total"]},
        },
    ))
    fig_g.update_layout(height=380, margin=dict(l=30, r=30, t=60, b=20),
                        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_g, use_container_width=True)

with c2:
    tree_data = []
    sub_items = {
        f"🚗 {T['card_transport']}": [(T["sub_commute"], F["commute_co2_per_km"][sel_route] * sel_km / 1000),
                                       (T["sub_flight"], (sel_flight * 250) / 365)],
        f"💻 {T['card_tech']}":      [(T["sub_pc"], (F["pc_watt"][sel_pc]/1000)*(sel_gaming+sel_study)*GRID),
                                       (T["sub_phone"], F["phone_charge_kwh"][sel_phone]*sel_charges*GRID),
                                       (T["sub_heating"], F["heating_co2_kg_day"][sel_heat])],
        f"🎧 {T['card_lifestyle']}": [(T["sub_dj"], sel_dj*0.050*GRID),
                                       (T["sub_board"], sel_board/30*5.0),
                                       (T["sub_streaming"], sel_stream*0.055),
                                       (T["sub_recycle"], max(0, F["recycling_offset_kg"][sel_rec])), # can't be negative in treemap
                                       (T["sub_shower"], sel_shower * 0.1)],
        f"👗 {T['card_fashion']}":   [(T["sub_clothing"], (sel_clothes/30)*15*F["style_multiplier"][sel_style]),
                                       (T["sub_perfume"], F["perfume_shipping_kg_day"][sel_perf])],
        f"🥗 {T['card_diet']}":      [(T["sub_food"], F["diet_base_kg_per_day"][sel_diet]),
                                       (T["sub_coffee"], sel_coffee*0.06),
                                       (T["sub_smoking"], 0.3 if sel_smoke else 0.0)],
    }
    for cat, subs in sub_items.items():
        for name, v in subs:
            tree_data.append({"category": cat, "source": name, "co2": max(v, 0.001)})

    df_tree = pd.DataFrame(tree_data)
    fig_tree = px.treemap(
        df_tree, path=["category", "source"], values="co2",
        color="co2",
        color_continuous_scale=["#c8e6c9", "#66bb6a", "#2e7d32", "#1b5e20"],
    )
    fig_tree.update_traces(
        textinfo="label+value+percent parent",
        texttemplate="<b>%{label}</b><br>%{value:.3f} kg",
        hovertemplate="<b>%{label}</b><br>%{value:.3f} kg CO₂<br>%{percentParent:.1%}<extra></extra>",
    )
    fig_tree.update_layout(
        title=dict(text=T["treemap_title"], font=dict(size=17), x=0.5),
        height=380, margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# ROW 2 — Radar + Bar
# ═══════════════════════════════════════════════════════════
c3, c4 = st.columns(2)

with c3:
    radar_cats = [T["card_transport"], T["card_tech"], T["card_lifestyle"],
                  T["card_fashion"], T["card_diet"]]
    user_vals  = [transport_co2, tech_co2, lifestyle_co2, fashion_co2, diet_co2]
    avg_vals   = [avg["transport"], avg["tech"], avg["lifestyle"], avg["fashion"], avg["diet"]]

    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(
        r=user_vals + [user_vals[0]],
        theta=radar_cats + [radar_cats[0]],
        fill="toself", name=T["legend_you"],
        fillcolor="rgba(46,125,50,0.25)",
        line=dict(color="#1b5e20", width=2),
        marker=dict(size=6),
    ))
    fig_r.add_trace(go.Scatterpolar(
        r=avg_vals + [avg_vals[0]],
        theta=radar_cats + [radar_cats[0]],
        fill="toself", name=T["legend_avg"],
        fillcolor="rgba(189,189,189,0.2)",
        line=dict(color="#9e9e9e", width=2, dash="dot"),
        marker=dict(size=5),
    ))
    fig_r.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(max(user_vals), max(avg_vals))*1.3],
                                   gridcolor="#e0e0e0"),
                   angularaxis=dict(gridcolor="#e0e0e0")),
        title=dict(text=T["radar_title"], font=dict(size=17), x=0.5),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
        height=400, margin=dict(l=60, r=60, t=55, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_r, use_container_width=True)

with c4:
    fig_b = go.Figure()
    fig_b.add_trace(go.Bar(
        name=T["legend_you"], y=radar_cats, x=user_vals, orientation="h",
        marker=dict(color="#2e7d32"),
        text=[f"{v:.2f}" for v in user_vals], textposition="auto",
        textfont=dict(color="white", size=13),
    ))
    fig_b.add_trace(go.Bar(
        name=T["legend_avg"], y=radar_cats, x=avg_vals, orientation="h",
        marker=dict(color="#bdbdbd"),
        text=[f"{v:.2f}" for v in avg_vals], textposition="auto",
        textfont=dict(color="white", size=13),
    ))
    fig_b.update_layout(
        barmode="group",
        title=dict(text=T["bar_title"], font=dict(size=17), x=0.5),
        xaxis_title=T["xaxis_label"],
        yaxis=dict(autorange="reversed"),
        height=400, margin=dict(l=20, r=20, t=55, b=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e0e0e0"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig_b, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# Dataset explorer
# ═══════════════════════════════════════════════════════════
with st.expander(T["explorer_title"]):
    st.dataframe(df.head(100), use_container_width=True, height=320)

st.markdown(f'''
<div class="cta-box">
    <h3>{T["cta_title"]}</h3>
    <p>{T["cta_text"]}</p>
    <a href="https://www.instagram.com/marmarayesk" target="_blank" class="cta-btn">{T["cta_button"]}</a>
</div>
''', unsafe_allow_html=True)

st.markdown(
    f"<p style='text-align:center;color:#9e9e9e;font-size:.75rem;margin-top:28px'>"
    f"{T['footer']}</p>",
    unsafe_allow_html=True)
