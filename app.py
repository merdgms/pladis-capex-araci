import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# --- AYARLAR ---
# Buraya Google Sheets'ten aldığınız CSV linkini yapıştırın
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRh9iyaNHEK4PDuMMQoIzdzh15RvWxfcKXOHEHFysvq-S6Ndw_LvjIvbwfZe9hUk-mSyj66F36You7i/pub?output=csv"
AMORTISMAN_SINIRI = 12000

st.set_page_config(page_title="pladis Karar Destek", page_icon="🛡️")

# --- BAŞLIK ---
st.markdown("<h1 style='text-align: center; color: #E30613;'>pladis</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>CAPEX / OPEX Karar Destek</h3>", unsafe_allow_html=True)

# Veriyi 10 saniyede bir tazeleyecek şekilde çeker
@st.cache_data(ttl=10) 
def load_data():
    return pd.read_csv(SHEET_URL)

# Sorgulama
desc = st.text_input("Malzeme Adı:", placeholder="Örn: Bant")
price = st.number_input("Tutar (TL):", min_value=0, value=15000)

if st.button("Sorgula") and desc:
    try:
        df = load_data()
        df['Keyword'] = df['Keyword'].astype(str).str.lower()
        
        if price < AMORTISMAN_SINIRI:
            st.success("SONUÇ: OPEX (Sınır Altı)")
        else:
            matches = process.extractOne(desc.lower(), df['Keyword'].tolist(), scorer=fuzz.partial_ratio)
            if matches and matches[1] > 65:
                res = df[df['Keyword'] == matches[0]].iloc[0]
                if res['Category'] == "CAPEX": st.error(f"SONUÇ: {res['Category']}")
                else: st.success(f"SONUÇ: {res['Category']}")
                st.info(f"Gerekçe: {res['Reason']}")
            else:
                st.warning("SONUÇ: İNCELENMELİ (Kural Bulunamadı)")
    except Exception as e:
        st.error(f"Veri Bağlantı Hatası: {e}")
