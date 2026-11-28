import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Senin etiketlediğin 20 örneğin olduğu dosyayı okuyoruz
# (Dosya adın farklıysa parantez içindeki ismi kendi dosya adınla değiştirebilirsin)
etiketli_dosya = "manuel_etiketlenecek.csv" 

try:
    egitim_df = pd.read_csv(etiketli_dosya)
    # Boş etiket bırakılmış satırları temizleyelim
    egitim_df = egitim_df.dropna(subset=['Etiket'])
    egitim_df['Etiket'] = egitim_df['Etiket'].astype(int)
    print(f"✔ Elinle etiketlediğin {len(egitim_df)} adet örnek başarıyla yüklendi.")
except Exception as e:
    print(f"Hata: '{etiketli_dosya}' dosyası okunamadı. Dosya adını veya sütunları kontrol et!", e)
    exit()

# 2. TF-IDF Vektörleştirme (Metinleri sayısal matrise çevirme)
vectorizer = TfidfVectorizer(max_features=5000)
X_train = vectorizer.fit_transform(egitim_df['Yorumlar'])
y_train = egitim_df['Etiket']

# 3. Makine Öğrenmesi Modeli (Logistic Regression) Kurulumu ve Eğitimi
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("✔ Model senin mantığını ve etiketleme tarzını öğrendi!")

# 4. Büyük veri setini (watsons_final.csv) okuyup modelle tahmin ettirelim
tum_dosya = "watsons_final.csv"
tum_df = pd.read_csv(tum_dosya, on_bad_lines='skip')
tum_df = tum_df.dropna(subset=['Yorumlar'])

# Tüm veriyi vektörleştir ve modelle tahmin ettir
X_tum = vectorizer.transform(tum_df['Yorumlar'])
tahminler = model.predict(X_tum)

# Sonuçları DataFrame'e ekleyelim
tum_df['Etiket'] = tahminler
etiket_ters_haritasi = {0: "Olumsuz", 1: "Nötr", 2: "Olumlu"}
tum_df['Duygu'] = tum_df['Etiket'].map(etiket_ters_haritasi)

# 5. Final dosyasını kaydedelim
son_dosya = "watsons_final_etiketli.csv"
tum_df.to_csv(son_dosya, index=False, encoding="utf-8-sig", quoting=1)

print(f"\n🎉 HARİKA! Tüm büyük veri seti etiketlendi ve '{son_dosya}' olarak kaydedildi.")
print("\n--- Oluşan Sınıf Dağılımı ---")
print(tum_df['Duygu'].value_counts())
print("\nOransal Dağılım (%):")
print(tum_df['Duygu'].value_counts(normalize=True) * 100)