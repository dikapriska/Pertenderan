import streamlit as st
import pandas as pd
import requests
import os
import json
import pdfkit
from io import BytesIO
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

st.set_page_config(page_title="Dashboard Tender LPSE", layout="wide", initial_sidebar_state="collapsed")

st.title("📊 Dashboard Tender LPSE")
st.subheader("🔍 Pilih LPSE dan Tahun")

# Tombol refresh cache
with st.sidebar:
    st.header("⚙️ Pengaturan")
    if st.button("Refresh Cache"):
        st.cache_data.clear()
        st.success("✅ Cache berhasil dibersihkan. Silakan muat ulang halaman.")

# Fungsi untuk mengonversi DataFrame ke PDF
def generate_pdf_from_html(dataframe, year):
    html = dataframe.to_html(index=False)  # Convert dataframe to HTML
    html_content = f"""
    <html>
    <head><style>
    body {{font-family: Arial, sans-serif;}}
    table {{width: 100%; border-collapse: collapse;}}
    th, td {{border: 1px solid #ddd; padding: 8px; text-align: left;}}
    th {{background-color: #f2f2f2;}}
    </style></head>
    <body>
    <h2>Data Tender LPSE - {year}</h2>
    {html}
    </body></html>
    """
    
    # Convert HTML to PDF using pdfkit
    pdf = pdfkit.from_string(html_content, False)
    return pdf

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
            })

        df_tender = pd.DataFrame(tender_rows)

        # Konversi tanggal ke format DD Bulan Tahun (Indonesia)
        def format_tanggal_indonesia(dt):
            bulan_id = [
                "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"
            ]
            if pd.isnull(dt):
                return ""
            dt = pd.to_datetime(dt, errors="coerce")
            if pd.isnull(dt):
                return ""
            return f"{dt.day} {bulan_id[dt.month]} {dt.year}"

        # Format tanggal
        df_tender["Tanggal Tayang"] = pd.to_datetime(df_tender["Tanggal Tayang"], errors="coerce").apply(format_tanggal_indonesia)

        # Filter instansi & kategori
        st.subheader("🎛️ Filter Data")

        kategori_opsi = ["Semua"] + sorted(df_tender["Kategori"].dropna().unique().tolist())
        instansi_opsi = ["Semua"] + sorted(df_tender["Instansi"].dropna().unique().tolist())

        selected_kategori = st.selectbox("Filter Kategori", kategori_opsi)
        selected_instansi = st.selectbox("Filter Instansi", instansi_opsi)

        if selected_kategori != "Semua":
            df_tender = df_tender[df_tender["Kategori"] == selected_kategori]
        if selected_instansi != "Semua":
            df_tender = df_tender[df_tender["Instansi"] == selected_instansi]

        # Search Nama Paket
        search_query = st.text_input("🔍 Cari Nama Paket")
        if search_query:
            df_tender = df_tender[df_tender["Nama Paket"].str.contains(search_query, case=False, na=False)]

        # Sort tanggal tayang DESC (default tanpa kontrol di UI)
        df_tender = df_tender.sort_values(by="Tanggal Tayang DT", ascending=False).reset_index(drop=True)

        # Hapus kolom internal
        df_display = df_tender.drop(columns=["Tanggal Tayang DT"])

        # --- Tampilkan tabel dengan AgGrid ---
        st.subheader("📄 Daftar Tender")
        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
        gb.configure_default_column(resizable=True, sortable=True, filter=True)
        grid_options = gb.build()

        AgGrid(
            df_display,
            gridOptions=grid_options,
            enable_enterprise_modules=False,
            fit_columns_on_grid_load=True,
            height=500,
            theme="balham"
        )

        # --- Opsi download ---
        st.subheader("⬇️ Unduh Data")

        col1, col2, col3 = st.columns(3)
        with col1:
            csv = df_display.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Unduh CSV",
                csv,
                file_name="tender_lpse_{tahun}.csv",
                mime="text/csv"
            )
        with col2:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_display.to_excel(writer, index=False, sheet_name='Tender')
            st.download_button("📥 Unduh Excel",
                output.getvalue(),
                file_name="tender_lpse_{tahun}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with col3:
            pdf = generate_pdf_from_html(df_display, tahun)
            st.download_button("📥 Unduh PDF",
                pdf,
                file_name="tender_lpse_{tahun}.pdf",
                mime="application/pdf"
            )

except Exception as e:
    st.error(f"❌ Gagal memuat data tender: {e}")
