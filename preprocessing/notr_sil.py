import pandas as pd

# Dosya adını güncel ikili dosyan olarak belirliyoruz
dosya_adi = "watsons_ikili_etiketli.csv"

print("1. Dosya güvenli bir şekilde okunuyor...")
try:
    # on_bad_lines='skip' parametresi sayesinde bozuk satırlar hata vermez, atlanır
    df = pd.read_csv(dosya_adi, on_bad_lines='skip', encoding="utf-8-sig")
    print(f"✔ Başarıyla okundu. Toplam satır: {len(df)}")
except FileNotFoundError:
    print(f"Hata: '{dosya_adi}' dosyası bulunamadı! Dosya adını kontrol et.")
    exit()

# 2. Yalnızca 'Yorumlar' sütunundaki harfleri küçük harfe çeviriyoruz
# (Duygu ve Etiket sütunlarına kesinlikle dokunulmaz!)
if 'Yorumlar' in df.columns:
    df['Yorumlar'] = df['Yorumlar'].astype(str).str.lower()
    print("✔ 'Yorumlar' sütunundaki tüm harfler küçük harfe dönüştürüldü.")
else:
    print("Hata: Dosyada 'Yorumlar' adında bir sütun bulunamadı!")
    exit()

# 3. Dosyayı aynı isimle temiz bir şekilde tekrar kaydedelim
df.to_csv(dosya_adi, index=False, encoding="utf-8-sig", quoting=1)

print(f"\n🎉 İŞLEM TAMAM! Güncellenmiş dosya '{dosya_adi}' olarak kaydedildi.")
print("Duygu ve Etiket sütunları güvenle korundu.")

# Kontrol için ilk 3 satırı ekrana yazdıralım
print("\n--- Örnek Güncel Satırlar ---")
print(df[['Yorumlar', 'Duygu', 'Etiket']].head(3))