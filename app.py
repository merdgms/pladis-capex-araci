import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# --- AYARLAR ---
# 1. Adımda kopyaladığınız Google linkini buraya tırnakların içine yapıştırın
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRh9iyaNHEK4PDuMMQoIzdzh15RvWxfcKXOHEHFysvq-S6Ndw_LvjIvbwfZe9hUk-mSyj66F36You7i/pub?output=csv"
AMORTISMAN_SINIRI = 12000

st.set_page_config(page_title="pladis Karar Destek", page_icon="🛡️")

# Veri Çekme
@st.cache_data(ttl=600) # Her 60 saniyede bir günceller
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Keyword'] = df['Keyword'].astype(str).str.lower()
    return df

# Tasarım
st.title("🛡️ pladis Türkiye")
st.subheader("CAPEX / OPEX Karar Destek Sistemi")

with st.form("soru_formu"):
    desc = st.text_input("Malzeme veya İşlem Adı:", placeholder="Örn: Konveyör Bant")
    price = st.number_input("Tutar (KDV Hariç TL):", min_value=0, value=15000)
    check = st.form_submit_button("Sorgula")

if check and desc:
    df = load_data()
    if price < AMORTISMAN_SINIRI:
        st.success("### SONUÇ: OPEX")
        st.info(f"Gerekçe: Tutar {AMORTISMAN_SINIRI} TL altındadır (VUK 2026).")
    else:
        # Anlamsal eşleşme
        matches = process.extractOne(desc.lower(), df['Keyword'].tolist(), scorer=fuzz.partial_ratio)
        if matches and matches[1] > 70:
            row = df[df['Keyword'] == matches[0]].iloc[0]
            cat = row['Category']
            if cat == "CAPEX": st.error(f"### SONUÇ: {cat}")
            else: st.success(f"### SONUÇ: {cat}")
            st.info(f"Gerekçe: {row['Reason']}")
        else:
            st.warning("### SONUÇ: İNCELENMELİ")
            st.write("Net bir kural bulunamadı. Lütfen rehber dökümana bakınız.")
