import streamlit as st
import pandas as pd
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from st_aggrid import AgGrid, GridOptionsBuilder

# Load konfigurasi dari .env
load_dotenv()
URL_LPSE = os.getenv("URL_LPSE")
URL_TENDER_BASE = os.getenv("URL_TENDER")

HEADERS = {
    "User-Agent": "curl/7.68.0"
}

st.set_page_config(
    page_title="Dashboard Tender LPSE",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📊 Dashboard Tender LPSE")
st.subheader("🔍 Pilih LPSE dan Tahun")

# Tombol refresh cache
with st.sidebar:
    st.header("⚙️ Pengaturan")
    if st.button("Refresh Cache"):
        st.cache_data.clear()
        st.success("✅ Cache berhasil dibersihkan. Silakan muat ulang halaman.")

# --- Fungsi dengan cache untuk data LPSE dan tender ---
@st.cache_data(ttl=604800)
def load_lpse_data():
    try:
        response = requests.get(URL_LPSE, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json(), "API"
    except Exception:
        try:
            with open("data/daftarlpse.json", "r", encoding="utf-8") as f:
                return json.load(f), "file lokal"
        except Exception:
            return None, None

@st.cache_data(ttl=86400)
def load_tender_data(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()

# --- Ambil data LPSE ---
data_lpse, sumber = load_lpse_data()
if not data_lpse:
    st.error("❌ Gagal memuat data LPSE dari API maupun file lokal.")
    st.stop()
else:
    st.success(f"✅ Data LPSE berhasil dimuat dari {sumber}")

# --- Dropdown pilihan LPSE ---
lpse_options = {item['nama_lpse']: item['kd_lpse'] for item in data_lpse if item.get('kd_lpse') and item.get('nama_lpse')}
selected_lpse = st.selectbox("Pilih LPSE", list(lpse_options.keys()))
selected_kd_lpse = lpse_options[selected_lpse]

# --- Pilih tahun (tahun ini sampai 2 tahun ke depan) ---
tahun_sekarang = datetime.now().year
tahun_list = list(range(tahun_sekarang, tahun_sekarang + 3))
tahun = st.selectbox("Pilih Tahun", tahun_list, index=0)

# --- Ambil data tender dari API JSON ---
url_tender = f"{URL_TENDER_BASE}/{tahun}/{selected_kd_lpse}"

try:
    data_json = load_tender_data(url_tender)

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

        # --- Tampilkan dengan AgGrid ---
        st.subheader("📄 Daftar Tender")
        gb = GridOptionsBuilder.from_dataframe(df_tender)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
        gb.configure_default_column(resizable=True, sortable=True, filter=True)
        grid_options = gb.build()

        AgGrid(
            df_tender,
            gridOptions=grid_options,
            enable_enterprise_modules=False,
            fit_columns_on_grid_load=True,
            height=500
        )

except Exception as e:
    st.error(f"❌ Gagal memuat data tender: {e}")
