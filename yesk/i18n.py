"""Çok dilli arayüz metinleri ve Türkçe seçenek eşlemesi."""

from typing import Any

LANG: dict[str, dict[str, Any]] = {
  "en": {
    "page_title": "🌍 Carbon Footprint Dashboard",
    "page_title_browser": "Carbon Footprint · YESK",
    "page_subtitle": (
        "Green Economy & Sustainability Club — Marmara University. "
        "Free, illustrative estimate for typical student habits—not a certified carbon audit."
    ),
    "dashboard_howto": (
        "**How to use**\n\n"
        "1. Open the **sidebar** on the left and expand each category (transport through diet).\n"
        "2. Choose values that match a **typical day** for you.\n"
        "3. Use **Dashboard** for totals and **Analytics** for breakdowns. "
        "Your percentile ranks you against the **synthetic cohort dataset** only."
    ),
    "badge_fmt": "📊 DATASET: {:,} PROFILES",
    "sidebar_title": "🌿 Lifestyle Inputs",
    "sidebar_caption": "All categories below are editable—expand each section and set your habits to build your estimate.",
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
    "lbl_pets": "Pet ownership",
    "lbl_housework": "Laundry/Dishwasher (cycles/week)",
    # Fashion
    "lbl_clothes": "Clothing items bought / month",
    "lbl_style": "Fashion style",
    "lbl_perfume": "Cosmetics / perfume shipping",
    # Diet
    "lbl_diet": "Diet type",
    "lbl_coffee": "Coffee cups / day",
    "lbl_smoke": "I am a smoker",
    "lbl_delivery": "Food delivery / Takeout",
    "lbl_water": "Plastic bottled water",
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
    "explorer_title_fmt": "📂 Explore Raw Dataset ({:,} profiles)",
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
    "sub_pets": "Pets",
    "sub_housework": "Housework",
    "sub_clothing": "Clothing",
    "sub_perfume": "Perfume Ship.",
    "sub_food": "Food",
    "sub_coffee": "Coffee",
    "sub_smoking": "Smoking",
    "sub_delivery": "Food Delivery",
    "sub_water": "Bottled Water",
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
    "tab_dashboard": "🏠 Dashboard",
    "tab_analytics": "📊 Analytics",
    "tab_action": "💡 Tips & Data",
    "percentile_wow": "You are greener than {:.1f}% of students! 👑",
    "percentile_bad": "Your footprint is higher than {:.1f}% of students. Time to act! 🚨",
    "badge_eco_warrior": "🥇 Eco Warrior",
    "badge_green_citizen": "🥈 Green Citizen",
    "badge_average": "🥉 Average",
    "badge_high_impact": "🚨 High Impact",
    "badge_no_percentile": "📊 Rank unavailable",
    "percentile_na": "We could not rank you against the cohort (no valid totals in the loaded dataset).",
    "warn_percentile_body": "Percentile comparison is disabled until the cohort file has valid numeric totals.",
    "warn_percentile_analytics": "Cohort comparison charts may be misleading until totals in the CSV are valid.",
    "share_title": "📸 Share to Instagram Story",
    "share_desc": "Take a screenshot of this card and tag @marmarayesk!",
    "methodology_title": "📘 Methodology & sources",
    "methodology_md": (
        "### What is this?\n\n"
        "This app shows an **illustrative daily CO₂ footprint** in kilograms per day for a student-style lifestyle. "
        "It is **not** a certified carbon audit; treat numbers as a teaching tool.\n\n"
        "### Main assumptions\n\n"
        "- **Grid emissions:** Electricity factors use **0.47 kg CO₂ per kWh** (`grid_co2_kg_per_kwh` in the JSON file), a rough average for Turkey.\n"
        "- **Flights:** Each short/medium trip is modeled as **250 kg CO₂ per year**, spread over 365 days.\n"
        "- **Showers:** Hot water is approximated as **0.1 kg CO₂ per minute** of showering.\n"
        "- **Synthetic data:** Profiles come from `generate_complex_data.py` → `complex_emissions.csv`. **Percentiles** rank you against that file only.\n\n"
        "### Smoking line in the diet category\n\n"
        "To stay aligned with the synthetic cohort, **non-smokers** include a **−0.3 kg/day calibration** and **smokers** add **+0.3 kg/day**. "
        "This is not a physical negative emission; it keeps totals comparable across the synthetic cohort.\n"
    ),
    "hist_title": "Total daily footprint in the synthetic cohort",
    "hist_caption": "The vertical line is your current total. Histogram uses all rows in the loaded CSV.",
    "hist_vline_label": "You",
    "hist_yaxis": "Count",
    "box_title": "Per-category distribution (synthetic cohort)",
    "explorer_cols": "Columns",
    "explorer_rows": "Max rows to show",
    "explorer_empty": "Select at least one column to preview the table.",
    # UX / a11y / story card
    "help_route": "Choose the main mode you use most days; it scales with distance below.",
    "help_km": "One-way or round-trip total you want to count for a typical study day.",
    "help_flights": "Short/medium flights per year; each is spread evenly across the year in the model.",
    "help_pc": "Higher-watt devices increase grid emissions with use hours.",
    "help_heating": "Dorm vs apartment vs family home changes the daily heating footprint.",
    "help_diet": "Base diet intensity before coffee, delivery, and water add-ons.",
    "help_recycle": "Better recycling slightly lowers lifestyle emissions in this simplified model.",
    "use_precise_transport": "Type exact km / flights (helpful on small screens)",
    "story_brand_title": "YESK Footprint",
    "story_share_btn": "Share / Download image",
    "story_processing": "Preparing…",
    "story_alert_download": "Image saved — open your gallery to post on Instagram.",
    "story_alert_fail": "Share failed. Try again or take a screenshot.",
    "story_share_native_title": "YESK carbon footprint",
    "story_share_native_text": "Here's my footprint! Discover yours via @marmarayesk.",
    "ui_reset": "Reset all inputs to defaults",
    "ui_reset_done": "Inputs were reset to defaults.",
    "ui_progress_title": "Categories",
    "ui_progress_hint": "🚗 · 💻 · 🎧 · 👗 · 🥗 — open each section in the sidebar and adjust your habits",
    "sidebar_methodology_hint": (
        "Figures are **rough teaching estimates**, not certified audits. "
        "See **Analytics → Methodology** for how they are calculated."
    ),
    "url_sidebar_tip": "On a phone, close the left menu first so the main content fills the screen.",
    "hist_summary": "Cohort median total: **{med:.2f}** kg/day · Yours: **{you:.2f}** ({cmp}).",
    "hist_cmp_above": "above median",
    "hist_cmp_below": "below median",
    "hist_cmp_equal": "near median",
    "box_summary": "Each box summarizes the synthetic cohort for that category (median line inside the box).",
    "treemap_summary": "Area shows each sub-source’s share of the treemap display values (very small slices use a visibility floor).",
    "summary_top_cat": "Largest share of your total today: **{name}** (~{pct:.0f}% of your footprint).",
  },
  "tr": {
    "page_title": "🌍 Karbon Ayak İzi Panosu",
    "page_title_browser": "Karbon Ayak İzi · YESK",
    "page_subtitle": (
        "Yeşil Ekonomi ve Sürdürülebilirlik Kulübü — Marmara Üniversitesi. "
        "Ücretsiz, öğrenci yaşamına uygun günlük tahmin; resmi karbon denetimi değildir."
    ),
    "dashboard_howto": (
        "**Nasıl kullanılır**\n\n"
        "1. Soldaki **yan paneli** aç ve her kategoriyi (ulaşımdan beslenmeye) genişlet.\n"
        "2. **Tipik bir gününü** yansıtan değerleri seç.\n"
        "3. **Pano**da toplamları, **Detaylı Analiz**de grafikleri incele. "
        "Yüzdelik dilim, yalnızca **sentetik kohort veri setine** göre hesaplanır."
    ),
    "badge_fmt": "📊 VERİ: {:,} PROFİL",
    "sidebar_title": "🌿 Yaşam Tarzı Girdileri",
    "sidebar_caption": "Aşağıdaki tüm kategorileri düzenleyebilirsin; bölümleri açıp alışkanlıklarını seçerek tahmini oluştur.",
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
    "lbl_pets": "Evcil hayvan",
    "lbl_housework": "Çamaşır/Bulaşık (haftalık yıkama)",
    # Fashion
    "lbl_clothes": "Aylık satın alınan kıyafet",
    "lbl_style": "Moda tarzı",
    "lbl_perfume": "Kozmetik / parfüm kargosu",
    # Diet
    "lbl_diet": "Diyet tipi",
    "lbl_coffee": "Günlük kahve (fincan)",
    "lbl_smoke": "Sigara içiyorum",
    "lbl_delivery": "Dışarıdan Yemek (Getir/Yemeksepeti)",
    "lbl_water": "Plastik Su Şişesi Tüketimi",
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
    "explorer_title_fmt": "📂 Ham Veri Seti ({:,} profil)",
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
    "sub_pets": "Evcil Hayvan",
    "sub_housework": "Ev İşleri",
    "sub_clothing": "Kıyafet",
    "sub_perfume": "Parfüm Kargosu",
    "sub_food": "Yemek",
    "sub_coffee": "Kahve",
    "sub_smoking": "Sigara",
    "sub_delivery": "Paket Servis",
    "sub_water": "Pet Şişe Su",
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
    "tab_dashboard": "🏠 Pano",
    "tab_analytics": "📊 Detaylı Analiz",
    "tab_action": "💡 Tavsiyeler & Veri",
    "percentile_wow": "Öğrencilerin %{:.1f}'inden daha çevrecisin! 👑",
    "percentile_bad": "Ayak izin öğrencilerin %{:.1f}'inden daha yüksek. Harekete geçme zamanı! 🚨",
    "badge_eco_warrior": "🥇 Eko-Savaşçı",
    "badge_green_citizen": "🥈 Yeşil Vatandaş",
    "badge_average": "🥉 Ortalama",
    "badge_high_impact": "🚨 Yüksek Etki",
    "badge_no_percentile": "📊 Sıralama yok",
    "percentile_na": "Kohort ile kıyaslama yapılamıyor (yüklenen veri setinde geçerli toplamlar yok).",
    "warn_percentile_body": "Yüzdelik dilim, kohort dosyasında geçerli sayısal toplamlar olana kadar devre dışı.",
    "warn_percentile_analytics": "CSV’deki toplamlar geçerli olana kadar kohort grafikleri yanıltıcı olabilir.",
    "share_title": "📸 Instagram Story'de Paylaş",
    "share_desc": "Bu kartın ekran görüntüsünü al ve @marmarayesk'i etiketle!",
    "methodology_title": "📘 Metodoloji ve varsayımlar",
    "methodology_md": (
        "### Bu araç ne sunuyor?\n\n"
        "Uygulama, öğrenci yaşam tarzına yakın bir günlük **tahmini CO₂ ayak izini** (kg/gün) gösterir. "
        "Resmi bir karbon denetimi **değildir**; sayılar eğitim ve farkındalık içindir.\n\n"
        "### Temel varsayımlar\n\n"
        "- **Şebeke emisyonu:** Elektrik için **kWh başına 0,47 kg CO₂** (`complex_factors.json` içindeki `grid_co2_kg_per_kwh`) kullanılır; Türkiye için kabaca bir ortalamadır.\n"
        "- **Uçuşlar:** Kısa/orta mesafe bir uçuş için yılda **250 kg CO₂** varsayılır ve günlük ortalamaya **365'e bölünerek** yansıtılır.\n"
        "- **Duş:** Sıcak su için **dakika başına 0,1 kg CO₂** yaklaşımı kullanılır.\n"
        "- **Sentetik veri:** Profiller `generate_complex_data.py` ile üretilir ve `complex_emissions.csv` dosyasına yazılır. **Yüzdelik dilimler** yalnızca bu dosyaya göre hesaplanır.\n\n"
        "### Beslenme kategorisinde sigara satırı\n\n"
        "Sentetik veri setiyle uyum için **sigara içmeyenlerde −0,3 kg/gün**, **içenlerde +0,3 kg/gün** düzeltmesi uygulanır. "
        "Bu, fiziksel anlamda “negatif emisyon” değildir; sentetik kohorttaki dağılımla kıyaslamayı tutarlı tutmak içindir.\n"
    ),
    "hist_title": "Sentetik kohortta günlük toplam ayak izi",
    "hist_caption": "Dikey çizgi şu anki toplamınızdır. Histogram yüklenen CSV'deki tüm satırları kullanır.",
    "hist_vline_label": "Sen",
    "hist_yaxis": "Frekans",
    "box_title": "Kategori bazında dağılım (sentetik kohort)",
    "explorer_cols": "Sütunlar",
    "explorer_rows": "Gösterilecek satır sayısı",
    "explorer_empty": "Tabloyu görmek için en az bir sütun seç.",
    "help_route": "Çoğu gün kullandığın ana ulaşım tipi; aşağıdaki mesafe ile çarpılır.",
    "help_km": "Tipik bir ders günü için saymak istediğin toplam km (tek yön veya gidiş-dönüş).",
    "help_flights": "Yıllık kısa/orta uçuş sayısı; modelde yıla eşit yayılır.",
    "help_pc": "Daha yüksek güç tüketen cihazlar, kullanım saatine göre şebeke emisyonunu artırır.",
    "help_heating": "Yurt, öğrenci evi veya aile evi günlük ısınma ayak izini değiştirir.",
    "help_diet": "Kahve, paket servis ve su eklentilerinden önceki temel beslenme yoğunluğu.",
    "help_recycle": "Bu modelde daha iyi geri dönüşüm yaşam emisyonunu hafifçe düşürür.",
    "use_precise_transport": "Tam km / uçuş sayısını yaz (küçük ekranda kolay)",
    "story_brand_title": "YESK Ayak İzi",
    "story_share_btn": "Paylaş / Görsel indir",
    "story_processing": "Hazırlanıyor…",
    "story_alert_download": "Görsel kaydedildi — galeriden Instagram’da paylaşabilirsin.",
    "story_alert_fail": "Paylaşım başarısız. Tekrar dene veya ekran görüntüsü al.",
    "story_share_native_title": "YESK karbon ayak izi",
    "story_share_native_text": "İşte benim ayak izim! Seninkini @marmarayesk üzerinden keşfet.",
    "ui_reset": "Tüm girdileri varsayılana sıfırla",
    "ui_reset_done": "Girdiler varsayılan değerlere döndü.",
    "ui_progress_title": "Kategoriler",
    "ui_progress_hint": "🚗 · 💻 · 🎧 · 👗 · 🥗 — yan panelde her bölümü açıp alışkanlıklarını güncelle",
    "sidebar_methodology_hint": (
        "Sayılar **yaklaşık eğitim tahminidir**, sertifikalı denetim değildir. "
        "Hesaplama için **Detaylı Analiz → Metodoloji**ye bak."
    ),
    "url_sidebar_tip": "Telefonda önce sol menüyü kapat; ana içerik tam genişlikte görünsün.",
    "hist_summary": "Kohort medyan toplam: **{med:.2f}** kg/gün · Senin toplamın: **{you:.2f}** ({cmp}).",
    "hist_cmp_above": "medyanın üstünde",
    "hist_cmp_below": "medyanın altında",
    "hist_cmp_equal": "medyana yakın",
    "box_summary": "Her kutu, o kategoride sentetik kohortun dağılımını özetler (kutu içi çizgi medyana yakındır).",
    "treemap_summary": "Alan, treemap görünüm değerlerine göre alt kaynak payını gösterir (çok küçük dilimler görünürlük tabanı alır).",
    "summary_top_cat": "Bugünkü toplamının en büyük payı: **{name}** (yaklaşık %{pct:.0f}).",
  },
}

DROPDOWN_TR: dict[str, str] = {
    "Marmaray + Metro (cross-city)": "Marmaray + Metro (şehirler arası)",
    "Ferry + Bus": "Vapur + Otobüs",
    "Metrobüs": "Metrobüs",
    "Bus Only": "Sadece Otobüs",
    "Personal Car (Gasoline)": "Özel Araç (Benzinli)",
    "Personal Car (Diesel)": "Özel Araç (Dizel)",
    "Personal Car (Hybrid)": "Özel Araç (Hibrit)",
    "Electric Scooter / E-Bike": "Elektrikli Scooter / E-Bisiklet",
    "Walking / Cycling": "Yürüyüş / Bisiklet",
    "High-End Gaming Laptop": "Üst Seviye Oyun Laptopı",
    "Mid-Range Gaming Laptop": "Orta Seviye Oyun Laptopı",
    "Standard Office Laptop": "Standart Ofis Laptopı",
    "Ultrabook / Thin Laptop": "İnce / Ultrabook Laptop",
    "Desktop Gaming PC": "Masaüstü Oyun Bilgisayarı",
    "Desktop Office PC": "Masaüstü Ofis Bilgisayarı",
    "Tablet Only": "Sadece Tablet",
    "Flagship Phone (5000 mAh)": "Amiral Gemisi Telefon (5000 mAh)",
    "Mid-Range Phone (4500 mAh)": "Orta Segment Telefon (4500 mAh)",
    "Budget Phone (4000 mAh)": "Bütçe Dostu Telefon (4000 mAh)",
    "Dormitory (Shared)": "KYK / Paylaşımlı Yurt",
    "Apartment (Natural Gas)": "Öğrenci Evi (Doğalgaz)",
    "Apartment (Electric)": "Öğrenci Evi (Elektrikli Isıtıcı)",
    "Family Home (High Usage)": "Aile Evi (Yoğun Isıtma)",
    "Strict Recycler": "Her zaman (Kağıt, Plastik, Pil)",
    "Sometimes": "Bazen (Aklıma geldikçe)",
    "Never": "Hiçbir zaman",
    "Heavy Meat Eater": "Yoğun Et Tüketimi",
    "Moderate Meat": "Orta Düzey Et",
    "Pescatarian": "Pesketaryen",
    "Vegetarian": "Vejetaryen",
    "Vegan": "Vegan",
    "Streetwear / Heavy Denim": "Sokak Modası / Ağır Denim",
    "Fast Fashion": "Hızlı Moda",
    "Vintage / Thrift": "Vintage / İkinci El",
    "Designer / Luxury": "Tasarım / Lüks",
    "Minimal / Capsule": "Minimal / Kapsül",
    "Rarely (1-2/yr)": "Nadiren (yılda 1-2)",
    "Sometimes (3-6/yr)": "Bazen (yılda 3-6)",
    "Frequently (monthly)": "Sık sık (ayda 1)",
    "Rarely (1-2/month)": "Nadiren (ayda 1-2)",
    "Sometimes (1-2/week)": "Bazen (haftada 1-2)",
    "Frequently (3+/week)": "Sık sık (haftada 3+)",
    "Tap / Filtered (0)": "Musluk / süzgeçli (0)",
    "1-2 bottles/day": "Günde 1-2 şişe",
    "3-4 bottles/day": "Günde 3-4 şişe",
    "5+ bottles/day": "Günde 5+ şişe",
    "None": "Yok",
    "Cat (Indoor)": "Kedi (ev içi)",
    "Small Dog": "Küçük köpek",
    "Medium/Large Dog": "Orta/büyük köpek",
    "Low (1-2 cycles/wk)": "Düşük (haftada 1-2 yıkama)",
    "Medium (3-4 cycles/wk)": "Orta (haftada 3-4 yıkama)",
    "High (5+ cycles/wk)": "Yüksek (haftada 5+ yıkama)",
    "Dormitory / Outsourced": "Yurt / dışarıdan hizmet",
}
