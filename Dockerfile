# Gunakan image Python minimal
FROM python:3.10-slim

# Atur direktori kerja
WORKDIR /app

# Install dependencies untuk wkhtmltopdf dan hapus cache agar image lebih kecil
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    fontconfig \
    libfreetype6 \
    libx11-dev \
    libxrender1 \
    libxext6 \
    xfonts-75dpi \
    xfonts-base \
    wkhtmltopdf \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Salin semua file ke image
COPY . .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Expose port default Streamlit
EXPOSE 8501

# Jalankan Streamlit saat container start
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.address=0.0.0.0"]
