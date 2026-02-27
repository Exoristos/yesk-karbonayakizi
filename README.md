<div align="center">
  <h1>🌍 Karbon Ayak İzi Hesaplayıcı (YESK)</h1>
  <p><strong>Marmara Üniversitesi Yeşil Ekonomi ve Sürdürülebilirlik Kulübü (YESK) Etkinlik Uygulaması</strong></p>
  
  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/) <!-- Buraya kendi Streamlit linkini ekleyebilirsin -->
</div>

<br>

## 📌 Proje Hakkında
Bu proje, Marmara Üniversitesi öğrencileri için özel olarak geliştirilmiş interaktif bir **Karbon Ayak İzi Hesaplama Panosu**'dur. Kulüp etkinliklerinde, tanıtım stantlarında öğrencilerin kendi telefonlarından QR kod okutarak hızlıca karbon ayak izlerini hesaplamaları, kulüp hakkında bilgi almaları ve sürdürülebilirlik farkındalığı kazanmaları amacıyla tasarlanmıştır.

Uygulama arka planda **1.500 sentetik öğrenci profilinden** oluşan bir veri setini kullanarak kullanıcının değerlerini ortalama bir öğrenci ile anlık olarak kıyaslar.

## 🚀 Özellikler
* **Çift Dil Desteği:** Tek tıkla Türkçe ve İngilizce arayüz geçişi.
* **Kapsamlı Kategoriler:** Ulaşım, Teknoloji, Yaşam Tarzı, Moda ve Beslenme olmak üzere 5 ana alanda detaylı emisyon hesaplaması.
* **Gelişmiş Görselleştirme:** Toplam ayak izini gösteren hız göstergesi (Gauge), detaylı emisyon ağacı (Treemap), ortalama ile kıyaslayan Radar ve Bar grafikleri.
* **Oyunlaştırma (Gamification):** Ortalamanın altında emisyona sahip kullanıcılara kutlama balonları ve tebrik mesajları.
* **Akıllı Tavsiye Motoru:** Kişinin en çok emisyon ürettiği kategoriye özel anlık sürdürülebilirlik tavsiyeleri.
* **Mobil Uyumluluk:** Standlarda akıllı telefonlardan mükemmel görünüm için özel CSS optimizasyonu.
* **Kulüp Entegrasyonu (CTA):** Etkinliğe katılanları YESK Instagram sayfasına yönlendiren özel yönlendirme butonları.

## 🛠️ Kullanılan Teknolojiler
* **Python**
* **Streamlit** (Web arayüzü ve dağıtım)
* **Plotly** (İnteraktif grafikler ve görselleştirme)
* **Pandas** (Sentetik veri analizi)

## 📂 Dosya Yapısı
* `app.py`: Ana Streamlit web uygulaması kodu, arayüz bileşenleri ve hesaplama mantığı.
* `requirements.txt`: Streamlit Cloud'un projeyi ayağa kaldırması için gereken kütüphane listesi.
* `data/`
  * `complex_factors.json`: Araç emisyonları, diyet faktörleri gibi tüm hesaplama çarpanları ve kategorik ortalamalar.
  * `complex_emissions.csv`: Halka açık olarak incelenebilen 1.500 satırlık sentetik öğrenci ayak izi veri seti.

## 💡 Kurulum (Lokal Çalıştırma)
Projeyi kendi bilgisayarında çalıştırmak istersen:
1. Depoyu klonla: `git clone https://github.com/kullaniciadin/yesk-karbon.git`
2. Kütüphaneleri kur: `pip install -r requirements.txt`
3. Uygulamayı başlat: `streamlit run app.py`

## 📣 Bize Katılın!
Bu uygulama **YESK (Yeşil Ekonomi ve Sürdürülebilirlik Kulübü)** tarafından açık kaynak araçlar kullanılarak tasarlanmıştır. Gelişmelerden haberdar olmak ve etkinliklerimize katılmak için bizi takip edin!

👉 [**Instagram: @marmarayesk**](https://instagram.com/marmarayesk)
