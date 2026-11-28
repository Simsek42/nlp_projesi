import pandas as pd

print('1. "watsons_ikili_etiketli.csv" okunuyor...')
dosya_adi = 'watsons_ikili_etiketli.csv'

try:
  df = pd.read_csv(dosya_adi, on_bad_lines='skip')
  df = df.dropna(subset=['Yorumlar', 'Etiket'])
except FileNotFoundError:
  print(f"Hata: '{dosya_adi}' dosyası bulunamadı! Dosya adını kontrol et.")
  exit()

# Genişletilmiş ve Optimize Edilmiş Durdurma Kelimeleri (Stop Words) Listesi
turkce_durak_kelimeler = {
    # Standart Bağlaçlar ve Zamirler
    've',
    'bir',
    'bu',
    'da',
    'de',
    'için',
    'ile',
    'ne',
    'çok',
    'daha',
    'en',
    'o',
    'ama',
    'lakin',
    'fakat',
    'ancak',
    'gibi',
    'kadar',
    'ki',
    'ise',
    'ya',
    'hem',
    'arasında',
    'şu',
    'ben',
    'sen',
    'biz',
    'siz',
    'onlar',
    'birkaç',
    'bazı',
    'her',
    'hiç',
    'şey',
    'olarak',
    'değil',
    # Listenden Eklenen Nötr Bağlaçlar, Kısaltmalar ve Soru Kelimeleri
    'aynı',
    'zamanda',
    'rağmen',
    'ondan',
    'vs',
    'falan',
    'neden',
    'nasıl',
    'yine',
    'ayrıca',
}


def tokenize_ve_temizle(metin):
  # 1. Küçük harfe dönüştür ve boşluklardan böl
  kelimeler = str(metin).lower().split()

  # 2. Noktalama işaretlerini temizle
  tokens = [''.join(c for c in kelime if c.isalnum()) for kelime in kelimeler]

  # 3. Durdurma kelimelerini (Stop Words) ve tek harfli anlamsız kalıntıları ele
  temiz_tokens = [
      t
      for t in tokens
      if t and t not in turkce_durak_kelimeler and len(t) > 1
  ]

  return ' '.join(temiz_tokens)


print(
    '2. Tokenizasyon ve güncellenmiş Stop-Words temizliği uygulanıyor...'
)
df['Yorumlar'] = df['Yorumlar'].apply(tokenize_ve_temizle)

# Boş kalan satırları temizleyelim
df = df[df['Yorumlar'].str.strip() != '']

# Güncellenmiş tokenli dosyayı kaydedelim
cikis_dosyasi = 'watsons_tokenikli.csv'
df[['Yorumlar', 'Duygu', 'Etiket']].to_csv(
    cikis_dosyasi, index=False, encoding='utf-8-sig', quoting=1
)

print(
    f'\n🎉 İŞLEM TAMAM! Toplam {len(df)} yorum güncellenmiş kurallarla'
    ' temizlendi.'
)
print(f'Güncel dosya kaydedildi: "{cikis_dosyasi}"')

print('\n--- Temizlenmiş İlk 3 Satır Örnekleri ---')
print(df[['Yorumlar', 'Duygu']].head(3))