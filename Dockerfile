# Gunakan image Python minimal
FROM python:3.10-slim

# Atur direktori kerja
WORKDIR /app

# Install dependencies untuk wkhtmltopdf
RUN apt-get update && \
    apt-get install -y \
    wget \
    fontconfig \
    libfreetype6 \
    libx11-dev \
    libxrender1 \
    libxext6 \
    libjpeg-turbo8 \
    libssl1.1 \
    software-properties-common

RUN apt-add-repository -y "deb http://security.ubuntu.com/ubuntu bionic-security main" \
    && apt-get update

RUN apt-get install -y \
    libxrender1 \
    libfontconfig1 \
    libx11-dev \
    libjpeg62 \
    libxtst6 \
    fontconfig \
    xfonts-75dpi \
    xfonts-base \
    libpng12-0 \
    && apt-get clean

# Install wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    apt-get install -f && \
    rm wkhtmltox_0.12.6-1.bionic_amd64.deb

# Salin semua file ke image
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable untuk PDFKit
ENV PATH="/usr/local/bin/wkhtmltopdf:${PATH}"

# Expose port default Streamlit
EXPOSE 8501

# Jalankan Streamlit saat container start
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.address=0.0.0.0"]
