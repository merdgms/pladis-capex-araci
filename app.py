import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# --- AYARLAR ---
# Buraya Google Sheet CSV linkinizi tekrar yapıştırın
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRh9iyaNHEK4PDuMMQoIzdzh15RvWxfcKXOHEHFysvq-S6Ndw_LvjIvbwfZe9hUk-mSyj66F36You7i/pub?output=csv"
AMORTISMAN_SINIRI = 12000

st.set_page_config(page_title="pladis Karar Destek", page_icon="🛡️", layout="centered")

# Logo ve Başlık
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # Alternatif PNG logo linki
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Pladis_logo.png", width=200)

st.markdown("<h1 style='text-align: center; color: #E30613;'>Türkiye Finans & Bakım</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #002B49;'>CAPEX / OPEX Karar Destek Sistemi</h3>", unsafe_allow_html=True)

# Veri Çekme
@st.cache_data(ttl=300) # 5 dakikada bir günceller
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Keyword'] = df['Keyword'].astype(str).str.lower()
    return df

# Sorgulama Formu
st.markdown("---")
desc = st.text_input("Malzeme veya İşlem Adı:", placeholder="Örn: Büro Masası veya Konveyör Bant")
price = st.number_input("Tutar (KDV Hariç TL):", min_value=0, value=15000)
check = st.button("🔍 Sorgula")

if check and desc:
    df = load_data()
    # 1. Öncelik: Tam Eşleşme (Masa gibi net kelimeler için)
    
