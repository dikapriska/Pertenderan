import requests
import json
from time import sleep
from dotenv import load_dotenv
import os

# Load variabel dari .env
load_dotenv()
URL_TENDER = os.getenv("URL_TENDER")

tahun = 2025
start_kd_lpse = 10
end_kd_lpse = 1000
output_file = "data/daftarlpse.json"
result_data = []

headers = {
    "User-Agent": "curl/7.68.0"
}

for kd_lpse in range(start_kd_lpse, end_kd_lpse + 1):
    url = f"{URL_TENDER}/{tahun}/{kd_lpse}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                first_entry = data[0]
                extracted = {
                    "kd_lpse": first_entry.get("Repo id LPSE"),
                    "nama_lpse": first_entry.get("LPSE")
                }
                result_data.append(extracted)
                print(f"Berhasil ambil data LPSE {kd_lpse}")
        else:
            print(f"Kode LPSE {kd_lpse} tidak tersedia. Status: {response.status_code}")
    except Exception as e:
        print(f"Terjadi kesalahan pada LPSE {kd_lpse}: {e}")
    sleep(10)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)

print(f"Selesai. Total data tersimpan: {len(result_data)}")
