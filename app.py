import streamlit as st
import pandas as pd
from datetime import datetime

from data_loader import load_lpse_data, load_and_prepare_tender_data
from utils import format_tanggal_indonesia
from ui_components import display_filters, display_table, display_download_buttons

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Tender LPSE", layout="wide", initial_sidebar_state="collapsed")

st.title("📊 Dashboard Tender LPSE")
st.subheader("🔍 Pilih LPSE dan Tahun")

# Sidebar untuk refresh cache
with st.sidebar:
    st.header("⚙️ Pengaturan")
    if st.button("Refresh Cache"):
        st.cache_data.clear()
        st.success("✅ Cache berhasil dibersihkan. Silakan muat ulang halaman.")

# --- Ambil data LPSE ---
data_lpse, sumber = load_lpse_data()
if not data_lpse:
    st.error("❌ Gagal memuat data LPSE dari API maupun file lokal.")
    st.stop()
else:
    st.success(f"✅ Data LPSE berhasil dimuat dari {sumber}")

lpse_options = {item['nama_lpse']: item['kd_lpse'] for item in data_lpse if item.get('kd_lpse') and item.get('nama_lpse')}
selected_lpse = st.selectbox("Pilih LPSE", ["Semua"] + list(lpse_options.keys()))

# Tahun
tahun_sekarang = datetime.now().year
tahun_list = list(range(tahun_sekarang, tahun_sekarang + 3))
tahun = st.selectbox("Pilih Tahun", tahun_list, index=0)

# --- Ambil & Siapkan Data Tender ---
data_generator = load_and_prepare_tender_data(selected_lpse, tahun, lpse_options)
for result in data_generator:
    if "error" in result:
        st.warning(result["error"])
    elif "fatal" in result:
        st.error(result["fatal"])
        st.stop()
    elif "warning" in result:
        st.warning(result["warning"])
        st.stop()
    elif "success" in result:
        data_json = result["success"]

# --- Transformasi ke DataFrame ---
tender_rows = []
for item in data_json:
    kode_tender = item.get("Kode Tender")
    hps = item.get("HPS", 0)

    tanggal_tayang_raw = item.get("tanggal paket tayang", "")
    tanggal_tayang = tanggal_tayang_raw.split(" ")[0] if tanggal_tayang_raw else ""
    tanggal_tayang_dt = pd.to_datetime(tanggal_tayang_raw) if tanggal_tayang_raw else pd.NaT

    tender_rows.append({
        "Kode Tender": int(kode_tender) if kode_tender else None,
        "Nama Paket": item.get("Nama Paket"),
        "Instansi": item.get("Instansi dan Satker", [{}])[0].get("nama_instansi", ""),
        "Status": item.get("Status_Tender"),
        "Tanggal Tayang": tanggal_tayang,
        "Metode": item.get("Metode Pemilihan"),
        "Kategori": item.get("Kategori Pekerjaan", ""),
        "HPS": f"Rp {int(hps):,}".replace(",", ".") if isinstance(hps, (int, float)) else "-",
        "Tanggal Tayang DT": tanggal_tayang_dt,
        "LPSE": item.get("nama_lpse", selected_lpse),
    })

df_tender = pd.DataFrame(tender_rows)

# Format tanggal
df_tender["Tanggal Tayang"] = pd.to_datetime(df_tender["Tanggal Tayang"], errors="coerce").apply(format_tanggal_indonesia)

# --- Filter ---
df_filtered = display_filters(df_tender)

# Sortir default: Tanggal Tayang DESC
df_filtered = df_filtered.sort_values(by="Tanggal Tayang DT", ascending=False).reset_index(drop=True)
df_display = df_filtered.drop(columns=["Tanggal Tayang DT"])

# --- Tabel dan Unduhan ---
display_table(df_display)
display_download_buttons(df_display, tahun)
