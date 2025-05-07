# Gunakan image Python minimal
FROM python:3.10-slim

# Atur direktori kerja
WORKDIR /app

# Salin semua file ke image
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Expose port default Streamlit
EXPOSE 8501

# Jalankan Streamlit saat container start
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.address=0.0.0.0"]
