import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# --- AYARLAR ---
# Buraya Google Sheet CSV linkinizi tekrar yapıştırın
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRh9iyaNHEK4PDuMMQoIzdzh15RvWxfcKXOHEHFysvq-S6Ndw_LvjIvbwfZe9hUk-mSyj66F36You7i/pub?output=csv"
AMORTISMAN_SINIRI = 12000

st.set_page_config(page_title="pladis Karar Destek", page_icon="🛡️", layout="centered")

# --- LOGO VE BAŞLIK ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # pladis Resmi Logosu
    st.image("https://www.pladisglobal.com/wp-content/themes/pladis/assets/images/pladis-logo.svg", width=200)

st.markdown("<h1 style='text-align: center; color: #E30613;'>Türkiye Finans & Bakım</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #002B49;'>CAPEX / OPEX Karar Destek Sistemi</h3>", unsafe_allow_html=True)

# Veri Çekme Fonksiyonu
@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Keyword'] = df['Keyword'].astype(str).str.lower()
    return df

# Sorgulama Formu
st.markdown("---")
with st.container():
    desc = st.text_input("Malzeme veya İşlem Adı:", placeholder="Örn: Konveyör Bant veya Servo Motor")
    price = st.number_input("Tutar (KDV Hariç TL):", min_value=0, value=15000)
    check = st.button("🔍 Sorgula")

if check and desc:
    df = load_data()
    if price < AMORTISMAN_SINIRI:
        st.success("### SONUÇ: OPEX")
        st.info(f"**Gerekçe:** Tutar {AMORTISMAN_SINIRI} TL altındadır (VUK 2026 Mevzuatı).")
    else:
        # Anlamsal eşleşme (Fuzzy Matching)
        matches = process.extractOne(desc.lower(), df['Keyword'].tolist(), scorer=fuzz.partial_ratio)
        
        if matches and matches[1] > 70:
            row = df[df['Keyword'] == matches[0]].iloc[0]
            cat = row['Category']
            
            if cat == "CAPEX":
                st.error(f"### SONUÇ: {cat}")
                st.warning(f"**Gerekçe:** {row['Reason']}")
            else:
                st.success(f"### SONUÇ: {cat}")
                st.info(f"**Gerekçe:** {row['Reason']}")
        else:
            st.warning("### SONUÇ: İNCELENMELİ")
            st.markdown("⚠️ Net bir kural bulunamadı. Lütfen **pladis Capex/Opex Rehber dökümanına** bakınız veya Finans birimine danışınız.")

st.markdown("---")
st.caption("UFRS (IAS 16) ve pladis Global Muhasebe Standartlarına göre yapılandırılmıştır.")
