import pandas as pd

dosya_adi = "watsons_net.csv"  # Kendi ham dosya adın neyse buraya yazabilirsin

print(f"'{dosya_adi}' dosyası okunuyor...")
df = pd.read_csv(dosya_adi, on_bad_lines='skip')

baslangic_sayisi = len(df)

# Birebir aynı olan tekrar eden yorumları temizle
df = df.drop_duplicates(subset=['Yorumlar']).reset_index(drop=True)

silinen_sayi = baslangic_sayisi - len(df)
print(f"🧹 Toplam {silinen_sayi} adet tekrar eden (kopya) yorum silindi.")
print(f"✨ Kalan güncel satır sayısı: {len(df)}")

# Aynı dosyanın üzerine temizlenmiş haliyle kaydet
df.to_csv(dosya_adi, index=False, encoding="utf-8-sig", quoting=1)
print(f"✅ Temizlenmiş veri başarıyla '{dosya_adi}' dosyasına kaydedildi!")