import streamlit as st
import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv

# Load konfigurasi dari .env
load_dotenv()
URL_LPSE = os.getenv("URL_LPSE")
URL_TENDER_BASE = os.getenv("URL_TENDER")

HEADERS = {
    "User-Agent": "curl/7.68.0"
}

st.set_page_config(page_title="Dashboard Tender LPSE", layout="wide")
st.title("📊 Dashboard Tender LPSE")

# --- Ambil data LPSE dari API JSON, fallback ke file lokal ---
st.subheader("🔍 Pilih LPSE dan Tahun")

try:
    response = requests.get(URL_LPSE, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data_lpse = response.json()
    st.success("✅ Data LPSE berhasil dimuat dari API")
except Exception:
    st.warning("⚠️ Gagal mengambil data dari API LPSE. Menggunakan file lokal.")
    try:
        with open("data/daftarlpse.json", "r", encoding="utf-8") as f:
            data_lpse = json.load(f)
        st.success("✅ Data LPSE berhasil dimuat dari file lokal")
    except Exception as e:
        st.error(f"❌ Gagal memuat data LPSE dari file lokal: {e}")
        st.stop()

# --- Dropdown pilihan LPSE ---
lpse_options = {item['nama_lpse']: item['kd_lpse'] for item in data_lpse if item.get('kd_lpse') and item.get('nama_lpse')}
selected_lpse = st.selectbox("Pilih LPSE", list(lpse_options.keys()))
selected_kd_lpse = lpse_options[selected_lpse]

# --- Pilih tahun (2022–2026) ---
tahun = st.selectbox("Pilih Tahun", list(range(2026, 2021, -1)), index=0)

# --- Ambil data tender dari API JSON ---
url_tender = f"{URL_TENDER_BASE}/{tahun}/{selected_kd_lpse}"

try:
    response = requests.get(url_tender, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data_json = response.json()

    if not data_json:
        st.warning("⚠️ Tidak ada data untuk kombinasi LPSE dan tahun yang dipilih.")
    else:
        st.success(f"✅ Data berhasil dimuat: {len(data_json)} entri ditemukan")

        # Transformasi data JSON menjadi DataFrame
        tender_rows = []
        for item in data_json:
            kode_tender = item.get("Kode Tender")
            hps = item.get("HPS", 0)
            tender_rows.append({
                "Kode Tender": int(kode_tender) if kode_tender else None,
                "Nama Paket": item.get("Nama Paket"),
                "Instansi": item.get("Instansi dan Satker", [{}])[0].get("nama_instansi", ""),
                "Status": item.get("Status_Tender"),
                "Tanggal Tayang": item.get("tanggal paket tayang", "")[:10],
                "Metode": item.get("Metode Pemilihan"),
                "HPS": f"Rp {int(hps):,}".replace(",", ".") if isinstance(hps, (int, float)) else "-",
            })

        df_tender = pd.DataFrame(tender_rows)

        # --- Pagination ---
        items_per_page = 25
        total_items = len(df_tender)
        total_pages = (total_items - 1) // items_per_page + 1

        page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1, step=1)

        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        st.write(f"Menampilkan {start_idx + 1} - {min(end_idx, total_items)} dari {total_items} data")

        # Tampilkan data sesuai halaman
        st.dataframe(df_tender.iloc[start_idx:end_idx])

except Exception as e:
    st.error(f"❌ Gagal memuat data tender: {e}")
