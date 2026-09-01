import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# --- KONFİGÜRASYON ---
# ÖNEMLİ: Google Sheets'te 'Web'de Yayınla' -> 'CSV' seçip aldığınız linki buraya koyun
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRh9iyaNHEK4PDuMMQoIzdzh15RvWxfcKXOHEHFysvq-S6Ndw_LvjIvbwfZe9hUk-mSyj66F36You7i/pub?output=csv"
AMORTISMAN_SINIRI = 12000

st.set_page_config(page_title="pladis Karar Destek", page_icon="🛡️", layout="centered")

# --- LOGO VE BAŞLIK ---
st.markdown("<center><img src='https://www.pladisglobal.com/wp-content/uploads/2021/04/pladis-logo.png' width='200'></center>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #E30613;'>Türkiye Finans & Bakım</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #002B49;'>CAPEX / OPEX Karar Destek Sistemi</h3>", unsafe_allow_html=True)

# Veri Çekme (Hata Kontrollü)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip() # Başlıklardaki boşlukları siler
        df['Keyword'] = df['Keyword'].astype(str).str.lower().str.strip()
        return df
    except Exception as e:
        st.error(f"Excel verisi çekilemedi! Lütfen 'Web'de Yayınla' linkini kontrol edin. Hata: {e}")
        return None

# Sorgulama Formu
st.markdown("---")
desc = st.text_input("Malzeme veya İşlem Adı:", placeholder="Örn: Büro Masası veya Konveyör Bant")
price = st.number_input("Tutar (KDV Hariç TL):", min_value=0, value=15000)
check = st.button("🔍 Sorgula")

if check and desc:
    df = load_data()
    if df is not None:
        if price < AMORTISMAN_SINIRI:
            st.success("### SONUÇ: OPEX")
            st.info(f"**Gerekçe:** Tutar {AMORTISMAN_SINIRI} TL altındadır (VUK 2026 Mevzuatı).")
        else:
            # Önce tam kelime eşleşmesi (Masa gibi tek kelimeler için)
            exact_match = df[df['Keyword'] == desc.lower().strip()]
            
            if not exact_match.empty:
                row = exact_match.iloc[0]
                category, reason = row['Category'], row['Reason']
            else:
                # Anlamsal eşleşme (Fuzzy)
                matches = process.extractOne(desc.lower(), df['Keyword'].tolist(), scorer=fuzz.partial_ratio)
                if matches and matches[1] > 65:
                    row = df[df['Keyword'] == matches[0]].iloc[0]
                    category, reason = row['Category'], row['Reason']
                else:
                    category, reason = "İNCELENMELİ", "Net bir kural bulunamadı. Lütfen rehber dökümana bakınız."

            # Sonuç Ekranı
            if category == "CAPEX":
                st.error(f"### SONUÇ: {category}")
                st.warning(f"**Gerekçe:** {reason}")
            
