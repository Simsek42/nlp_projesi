import pandas as pd

print('1. "watsons_ikili_etiketli.csv" okunuyor...')
dosya_adi = 'watsons_ikili_etiketli.csv'

try:
  df = pd.read_csv(dosya_adi, on_bad_lines='skip')
  df = df.dropna(subset=['Yorumlar', 'Etiket'])
except FileNotFoundError:
  print(f"Hata: '{dosya_adi}' dosyası bulunamadı! Dosya adını kontrol et.")
  exit()


def tokenize_et(metin):
  # 1. Küçük harfe dönüştür ve boşluklardan bölerek token'larına (kelimelerine) ayır
  kelimeler = str(metin).lower().split()

  # 2. Noktalama işaretlerini temizle ve tek harfli anlamsız kalıntıları ele
  tokens = [''.join(c for c in kelime if c.isalnum()) for kelime in kelimeler]
  temiz_tokens = [t for t in tokens if len(t) > 1]

  # Token'ları tekrar aralarında boşluk bırakarak metin formatında birleştir
  return ' '.join(temiz_tokens)


print('2. Yorumlar tokenizasyon işleminden geçiriliyor...')
df['Yorumlar'] = df['Yorumlar'].apply(tokenize_et)

# Boş kalan satırları temizleyelim
df = df[df['Yorumlar'].str.strip() != '']

# İstediğin gibi eski ve yeni hali yan yana YOK!
# Dosyada sadece tokenize edilmiş 'Yorumlar', 'Duygu' ve 'Etiket' sütunları kalıyor.
cikis_dosyasi = 'watsons_tokenikli.csv'
df[['Yorumlar', 'Duygu', 'Etiket']].to_csv(
    cikis_dosyasi, index=False, encoding='utf-8-sig', quoting=1
)

print(f'\n🎉 İŞLEM TAMAM! Toplam {len(df)} yorum tokenize edildi.')
print(f'Yeni dosya kaydedildi: "{cikis_dosyasi}"')

print('\n--- Dosyadaki İlk 3 Tokenize Satır Örneği ---')
print(df[['Yorumlar', 'Duygu']].head(3))