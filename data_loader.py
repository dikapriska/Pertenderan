import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from streamlit import cache_data

load_dotenv()
URL_LPSE = os.getenv("URL_LPSE")
URL_TENDER_BASE = os.getenv("URL_TENDER")
HEADERS = {"User-Agent": "curl/7.68.0"}

@cache_data(ttl=604800)
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

@cache_data(ttl=86400)
def load_tender_data(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()

def load_and_prepare_tender_data(selected_lpse, tahun, lpse_options):
    data_json = []

    if selected_lpse == "Semua":
        for nama_lpse, kd_lpse in lpse_options.items():
            url = f"{URL_TENDER_BASE}/{tahun}/{kd_lpse}"
            try:
                result = load_tender_data(url)
                for row in result:
                    row["nama_lpse"] = nama_lpse
                data_json.extend(result)
            except Exception as e:
                yield {"error": f"Gagal memuat data dari {nama_lpse}: {e}"}
    else:
        kd_lpse = lpse_options[selected_lpse]
        url = f"{URL_TENDER_BASE}/{tahun}/{kd_lpse}"
        try:
            data_json = load_tender_data(url)
            for row in data_json:
                row["nama_lpse"] = selected_lpse
        except Exception as e:
            yield {"fatal": f"Gagal memuat data tender: {e}"}

    if not data_json:
        yield {"warning": "Tidak ada data untuk kombinasi LPSE dan tahun yang dipilih."}
    else:
        yield {"success": data_json}
