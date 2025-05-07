import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load konfigurasi dari .env
load_dotenv()
URL_LPSE = os.getenv("URL_LPSE")
URL_TENDER_BASE = os.getenv("URL_TENDER")

st.set_page_config(page_title="Dashboard Tender LPSE", layout="wide")
st.title("📊 Dashboard Tender LPSE")

# --- Ambil data LPSE dari API JSON ---
st.subheader("🔍 Pilih LPSE dan Tahun")
url_lpse = URL_LPSE
response = requests.get(url_lpse)

if response.status_code == 200:
    data_lpse = response.json()
    lpse_options = {item['nama_lpse']: item['kd_lpse'] for item in data_lpse}
    selected_lpse = st.selectbox("Pilih LPSE", list(lpse_options.keys()))
    selected_kd_lpse = lpse_options[selected_lpse]
else:
    st.error("Gagal mengambil data LPSE.")
    st.stop()

# --- Pilih tahun ---
tahun = st.selectbox("Pilih Tahun", list(range(2027, 2019, -1)))

# --- Ambil data tender dari API CSV ---
url_tender = f"{URL_TENDER_BASE}/{tahun}/{selected_kd_lpse}"

try:
    df_tender = pd.read_csv(url_tender)
    st.success(f"✅ Data berhasil dimuat: {len(df_tender)} entri ditemukan")

    # Tampilkan data
    st.dataframe(df_tender)

    # Statistik dasar
    st.subheader("📈 Ringkasan Statistik")
    st.write(df_tender.describe(include='all'))

except Exception as e:
    st.error(f"Gagal memuat data tender: {e}")
