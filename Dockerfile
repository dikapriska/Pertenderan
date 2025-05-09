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

# Download dan install libjpeg-turbo, lalu hapus file.deb
#RUN wget http://mirrors.kernel.org/ubuntu/pool/main/libj/libjpeg-turbo/libjpeg-turbo8_2.1.2-0ubuntu1_amd64.deb \
#    && dpkg -i libjpeg-turbo8_2.1.2-0ubuntu1_amd64.deb \
#    && rm libjpeg-turbo8_2.1.2-0ubuntu1_amd64.deb

# Download dan install libssl1.1, lalu hapus file .deb
#RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
#    && dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
#    && rm libssl1.1_1.1.0g-2ubuntu4_amd64.deb

# Salin semua file ke image
COPY . .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable untuk PDFKit
ENV PATH="/usr/local/bin/wkhtmltopdf:${PATH}"

# Expose port default Streamlit
EXPOSE 8501

# Jalankan Streamlit saat container start
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.address=0.0.0.0"]
