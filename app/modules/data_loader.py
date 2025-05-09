import requests
import json
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

URL_LPSE = os.getenv("URL_LPSE")
URL_TENDER_BASE = os.getenv("URL_TENDER")
HEADERS = {"User-Agent": "curl/7.68.0"}

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

def load_and_prepare_tender_data(lpse_options, selected_lpse, tahun):
    data_json = []

    if selected_lpse == "Semua":
        total = len(lpse_options)
        progress_bar = st.progress(0, text="🔄 Memuat data tender dari semua LPSE...")
        for idx, (nama_lpse, kd_lpse) in enumerate(lpse_options.items(), 1):
            url = f"{URL_TENDER_BASE}/{tahun}/{kd_lpse}"
            try:
                result = load_tender_data_func(url)
                for row in result:
                    row["nama_lpse"] = nama_lpse
                data_json.extend(result)
            except Exception:
                # Tidak ditampilkan agar tidak mengganggu UI
                pass
            progress_bar.progress(idx / total, text=f"🔄 Memuat LPSE: {nama_lpse} ({idx}/{total})")
        progress_bar.empty()
    else:
        kd_lpse = lpse_options[selected_lpse]
        url = f"{URL_TENDER_BASE}/{tahun}/{kd_lpse}"
        with st.spinner(f"🔄 Memuat data dari {selected_lpse}..."):
            try:
                data_json = load_tender_data_func(url)
                for row in data_json:
                    row["nama_lpse"] = selected_lpse
            except Exception as e:
                st.error(f"❌ Tidak ada data tender di {selected_lpse}")
                st.stop()

    if not data_json:
        st.warning("⚠️ Tidak ada data untuk kombinasi LPSE dan tahun yang dipilih.")
        return pd.DataFrame()

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
            "Jenis Pengadaan": item.get("Kategori Pekerjaan", ""),
            "HPS": f"Rp {int(hps):,}".replace(",", ".") if isinstance(hps, (int, float)) else "-",
            "Tanggal Tayang DT": tanggal_tayang_dt,
            "LPSE": item.get("nama_lpse", selected_lpse),
        })

    df_tender = pd.DataFrame(tender_rows)
    df_tender["Tanggal Tayang"] = pd.to_datetime(df_tender["Tanggal Tayang"], errors="coerce")
    return df_tender