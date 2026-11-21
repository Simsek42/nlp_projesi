# Resmi hafif Python imajını kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Gerekli sistem paketlerini yüklüyoruz
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Önce bağımlılık dosyasını kopyalayıp kütüphaneleri yüklüyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarımızı (kodlar, model klasörü vb.) konteynere kopyalıyoruz
COPY . .

# FastAPI'nin çalışacağı portu açıyoruz
EXPOSE 8000

# Konteyner ayağa kalkınca çalışacak komut (FastAPI sunucusu)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]