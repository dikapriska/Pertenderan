import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load konfigurasi dari .env
load_dotenv()
#URL_LPSE = os.getenv("URL_LPSE")
URL_TENDER_BASE = os.getenv("URL_TENDER")

# Halaman
st.set_page_config(page_title="Dashboard Tender LKPP", layout="wide")

st.title("📊 Dashboard Tender LKPP")

# --- PILIH TAHUN DENGAN URL PARAM ---
query_params = st.experimental_get_query_params()
tahun_param = int(query_params.get("tahun", [2025])[0])

tahun_list = list(range(2022, 2026))
tahun = st.selectbox("Pilih Tahun", tahun_list, index=tahun_list.index(tahun_param))
st.experimental_set_query_params(tahun=tahun)

# --- LPSE TEST (BUATAN MANUAL) ---
st.subheader("📍 Pilih LPSE")
st.info("API MasterLPSE tidak tersedia. Menggunakan daftar kode LPSE manual.")

kode_lpse_list = list(range(10, 1001, 10))
valid_lpse = {}

tahun_test = 2025
with st.spinner("Menguji LPSE yang aktif..."):
    for kd_lpse in kode_lpse_list:
        url_test = f"{URL_TENDER_BASE}/{tahun_test}/{kd_lpse}"
        try:
            df_test = pd.read_csv(url_test, nrows=1)
            if not df_test.empty:
                valid_lpse[f"LPSE {kd_lpse}"] = kd_lpse
        except:
            continue

if not valid_lpse:
    st.error("Tidak ada kode LPSE yang valid ditemukan.")
    st.stop()

selected_lpse = st.selectbox("Pilih LPSE", list(valid_lpse.keys()))
selected_kd_lpse = valid_lpse[selected_lpse]

# --- LOAD DATA TENDER ---
st.subheader("📄 Data Tender")
url_tender = f"{URL_TENDER_BASE}/{tahun}/{selected_kd_lpse}"
try:
    df_tender = pd.read_csv(url_tender)
    total_items = len(df_tender)

    if total_items == 0:
        st.warning("Data kosong.")
        st.stop()

    st.success(f"✅ Data berhasil dimuat: {total_items} entri ditemukan")

    # --- PAGINATION 10 PER HALAMAN ---
    items_per_page = 10
    total_pages = (total_items - 1) // items_per_page + 1
    page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1, step=1)

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    st.write(f"Menampilkan {start_idx + 1} - {min(end_idx, total_items)} dari {total_items} data")

    st.dataframe(df_tender.iloc[start_idx:end_idx])

    # --- STATISTIK ---
    st.subheader("📈 Statistik Ringkas")
    st.write(df_tender.describe(include='all'))

except Exception as e:
    st.error(f"Gagal memuat data tender: {e}")