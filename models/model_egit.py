import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

print('1. "watsons_tokenikli.csv" okunuyor...')
dosya_adi = 'watsons_tokenikli.csv'

try:
  df = pd.read_csv(dosya_adi, on_bad_lines='skip')
  df = df.dropna(subset=['Yorumlar', 'Etiket'])
except FileNotFoundError:
  print(f"Hata: '{dosya_adi}' dosyası bulunamadı! Önceki adımı kontrol et.")
  exit()

# Özellik (X) ve Etiket (y) sütunlarını belirleme
X = df['Yorumlar'].astype(str)
y = df['Etiket'].astype(int)

# 2. Train / Test Ayrımı (%80 Eğitim, %20 Test)
print('2. Veri Eğitim ve Test olarak ayrılıyor...')
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f'Eğitim kümesi boyutu: {len(X_train)} | Test kümesi boyutu: {len(X_test)}')

# 3. TF-IDF Vektörleştirme (Kelimeleri sayısal matrise çevirme)
print('3. TF-IDF vektör matrisi oluşturuluyor...')
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Model Eğitimi (Logistic Regression)
print('4. Logistic Regression modeli eğitiliyor...')
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)
print('✔ Model başarıyla eğitildi!')

# 5. Model Değerlendirme (Şemadaki 6. Adım)
print('5. Model test verisiyle değerlendiriliyor...')
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)

print('\n================ MODEL PERFORMANS RAPORU ================' )
print(f'🎯 Doğruluk Oranı (Accuracy): % {acc * 100:.2f}')
print('\nDetaylı Sınıflandırma Raporu:')
print(
    classification_report(
        y_test, y_pred, target_names=['Olumsuz (0)', 'Olumlu (1)']
    )
)
print('Confusion Matrix (Hata Matrisi):')
print(confusion_matrix(y_test, y_pred))
print('==========================================================')

# 6. Model Kaydetme (Model Artifact / Registry - Şemadaki 7. Adım)
joblib.dump(model, 'watsons_duygu_modeli.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
print(
    '\n🎉 İŞLEM TAMAM! Model "watsons_duygu_modeli.pkl" ve Vektörleştirici'
    ' "tfidf_vectorizer.pkl" olarak kaydedildi.'
)