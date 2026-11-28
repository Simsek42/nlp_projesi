import pandas as pd
from transformers import pipeline

print("1. Watsons final dosyası okunuyor...")
try:
    df = pd.read_csv("watsons_final.csv", on_bad_lines='skip')
except FileNotFoundError:
    print("Hata: 'watsons_final.csv' dosyası bulunamadı! Aynı klasörde olduğundan emin ol.")
    exit()

# Boş satırları temizleyelim
df = df.dropna(subset=['Yorumlar'])

print("2. Türkçe yapay zeka modeli (BERT) indiriliyor ve hazırlanıyor...")
print("(İlk çalıştırmada model internetten indirileceği için birkaç saniye sürebilir, bekle...)")

# Türkçe duygu analizi için eğitilmiş hazır profesyonel model
sentiment_pipeline = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

print("3. Yapay zeka 5000 yorumu okumaya ve etiketlemeye başladı...")

duygular = []
etiketler = []

# 5000 yorumu sırayla işliyoruz
for i, yorum in enumerate(df['Yorumlar']):
    if not isinstance(yorum, str) or len(yorum.strip()) == 0:
        duygular.append("Nötr")
        etiketler.append(1)
        continue
        
    try:
        # Modelin kafasının karışmaması için çok uzun metinleri ilk 512 karakterle sınırlayalım
        temiz_yorum = yorum[:512]
        sonuc = sentiment_pipeline(temiz_yorum)[0]
        label = sonuc['label'] # Model 'POSITIVE' veya 'NEGATIVE' döndürür
        
        # Bizim istediğimiz formata çeviriyoruz:
        if label == 'POSITIVE':
            duygular.append("Olumlu")
            etiketler.append(2)
        elif label == 'NEGATIVE':
            duygular.append("Olumsuz")
            etiketler.append(0)
        else:
            duygular.append("Nötr")
            etiketler.append(1)
            
    except Exception as e:
        # Hata olursa sistemi durdurmasın, nötr geçsin
        duygular.append("Nötr")
        etiketler.append(1)
        
    # Her 500 yorumda bir ne kadar kaldığını ekrana yazdırsın ki çalıştığını göresin
    if (i + 1) % 500 == 0:
        print(f"👉 {i + 1} yorum başarıyla incelendi ve etiketlendi...")

# Yeni sütunları tablomuza ekleyelim
df['Duygu'] = duygular
df['Etiket'] = etiketler

# Sonucu yeni bir dosyaya kaydedelim
yeni_dosya = "watsons_final_etiketli.csv"
df.to_csv(yeni_dosya, index=False, encoding="utf-8-sig", quoting=1)

print(f"\n🎉 İŞLEM TAMAM! Etiketlenmiş dosya '{yeni_dosya}' adıyla kaydedildi.")
print("\n--- Yeni Sınıf Dağılımı ---")
print(df['Duygu'].value_counts())