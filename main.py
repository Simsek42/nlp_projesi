import joblib
from fastapi import FastAPI

# FastAPI uygulamasını başlatıyoruz
app = FastAPI(
    title='Watsons Duygu Analizi API',
    description='E-ticaret yorumları için makine öğrenmesi duygu analizi servisi',
    version='1.0',
)

# Önceden eğittiğimiz modeli ve TF-IDF vektörleştiriciyi yüklüyoruz
print('Model ve vektörleştirici yükleniyor...')
model = joblib.load('watsons_duygu_modeli.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
print('✔ Model ve vektörleştirici başarıyla yüklendi, API hazır!')


@app.get('/')
def anasayfa():
  return {
      'mesaj': (
          'Watsons Duygu Analizi API sistemine hoş geldiniz! 🚀 /docs adresine'
          ' giderek testi yapabilirsiniz.'
      )
  }


@app.post('/predict')
def duygu_tahmini(yorum: str):
  # 1. Gelen yeni yorumu vektör matrisine dönüştür
  yorum_vec = vectorizer.transform([yorum])

  # 2. Model ile tahmin yap (0 veya 1 döner)
  tahmin = model.predict(yorum_vec)[0]

  # 3. Modelin tahmin olasılığını (güven skorunu) hesapla
  olasiliklar = model.predict_proba(yorum_vec)[0]
  guven_skoru = float(max(olasiliklar))

  # Etiketi metne çevir
  duygu_sonucu = 'Olumlu' if tahmin == 1 else 'Olumsuz'

  return {
      'girilen_yorum': yorum,
      'tahmin_edilen_duygu': duygu_sonucu,
      'etiket_kodu': int(tahmin),
      'guven_orani_yuzde': round(guven_skoru * 100, 2),
  }