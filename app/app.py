import streamlit as st
from datetime import datetime

from modules.data_loader import load_lpse_data, load_and_prepare_tender_data
from modules.utils import generate_pdf_from_html
from modules.ui_components import show_filters, show_table, show_download_buttons

st.set_page_config(page_title="Dashboard Tender LPSE", layout="wide", initial_sidebar_state="collapsed")
st.title("📊 Dashboard Tender LPSE")
st.subheader("🔍 Pilih LPSE dan Tahun")

# Tombol refresh cache
with st.sidebar:
    st.header("⚙️ Pengaturan")
    if st.button("Refresh Cache"):
        st.cache_data.clear()
        st.success("✅ Cache berhasil dibersihkan. Silakan muat ulang halaman.")

# Muat LPSE
data_lpse, sumber = load_lpse_data()
if not data_lpse:
    st.error("❌ Gagal memuat data LPSE dari API maupun file lokal.")
    st.stop()
else:
    st.success(f"✅ Data LPSE berhasil dimuat dari {sumber}")

# Dropdown LPSE dan Tahun
lpse_options = {item['nama_lpse']: item['kd_lpse'] for item in data_lpse if item.get('kd_lpse') and item.get('nama_lpse')}
selected_lpse = st.selectbox("Pilih LPSE", ["Semua"] + list(lpse_options.keys()))
tahun_sekarang = datetime.now().year
tahun = st.selectbox("Pilih Tahun", list(range(tahun_sekarang, tahun_sekarang + 3)), index=0)

df_tender = load_and_prepare_tender_data(lpse_options, selected_lpse, tahun)

if df_tender.empty:
    st.warning("⚠️ Tidak ada data untuk kombinasi LPSE dan tahun yang dipilih.")
    st.stop()

# Tampilkan filter, tabel, dan unduhan
df_filtered = show_filters(df_tender)
show_table(df_filtered)
show_download_buttons(df_filtered, tahun)
