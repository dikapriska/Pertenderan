import requests
import json
import os
from time import sleep
from dotenv import load_dotenv

# Load .env
load_dotenv()
URL_TENDER = os.getenv("URL_TENDER")

# Parameter
tahun = datetime.now().year
start_kd_lpse = 10
end_kd_lpse = 1000
output_dir = "data"
output_file = os.path.join(output_dir, "daftarlpse.json")
result_data = []

# Buat folder jika belum ada
os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "curl/7.68.0"
}

print(f"Mulai crawling dari {start_kd_lpse} sampai {end_kd_lpse} untuk tahun {tahun}...")

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
                print(f"[✓] LPSE {kd_lpse} - {extracted['nama_lpse']}")
            else:
                print(f"[-] LPSE {kd_lpse} kosong")
        else:
            print(f"[x] LPSE {kd_lpse} - Status: {response.status_code}")
    except Exception as e:
        print(f"[!] Error LPSE {kd_lpse}: {e}")
    sleep(10)  # Ubah jika perlu

# Simpan hasil
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)

print(f"\nSelesai ✅ Total data tersimpan: {len(result_data)} ke {output_file}")
