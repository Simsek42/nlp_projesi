import pandas as pd

# 1. Dosyayı oku
dosya_adi = "watsons_final.csv"
try:
    df = pd.read_csv(dosya_adi, on_bad_lines='skip')
    print(f"'{dosya_adi}' başarıyla okundu. Toplam satır: {len(df)}")
except FileNotFoundError:
    print(f"Hata: '{dosya_adi}' dosyası bulunamadı.")
    exit()

def gelismis_duygu_etiketle(yorum):
    if not isinstance(yorum, str) or len(yorum.strip()) == 0:
        return "Nötr", 1
    
    yorum_kucuk = yorum.lower()
    
    # Kelime listeleri
    olumsuz_kelimeler = [
        "kötü", "berbat", "rezalet", "iğrenç", "çöp", "begenmedim", "beğenmedim", "hayal kırıklığı","iade", "döküyor","beyazlattı","beyazladı","yaramadı",
        "sevmedim", "hasarlı", "döküldü", "tavsiye etmem", "almayın", "yararsız", "kuru","kurudu","kuruyor","alerji","topaklanma","kupkuru","hala","gelmedi","tahriş etti",
        "etki etmedi", "para israfı", "kuruttu", "alerji", "pişman", "işe yaramaz","bozulmuş","bozuk","bozuldu","sakın","yazık","döküp","ne zaman","beyazlatıyor"
        "kalitesiz", "hiçbir", "hiç", "kirletti", "söktü", "bir daha almam","nefret","yağlandırdı","sivilce yaptı","sivilcelerimi arttırdı","kırık","alınmaz","dökülmüştü",
        "ağırlaştırdı","olumsuz değil","almam","boşa gider","yaramaz",
    ]
    
    olumlu_kelimeler = [
        "harika", "süper", "mükemmel", "muhteşem", "güzel", "beğendim", "tavsiye ederim", "dökülmem azaldı","dökülmemi azalttı","tavsiye ediyorum",
        "alın", "aldırın", "yumuşacık", "parlaklık", "efsane", "başarılı", "tavsiye edilir","faydasını gördüm","fayda gördüm",
        "favorim", "kurtarıcı", "kaliteli", "memnun", "stok", "muazzam", "hızlı","uzattı","işe yarıyor","dolgunluk",
        "muazzam", "canım","tatlı","dayanıklı","iyi","yaradı","etkisini gördüm","teşekkür ederim","teşekkür ediyorum","ferahlık","özenli","özenilmiş"
    ]
    
    notr_kelimeler = [
        "idare eder", "fena değil", "orta", "normal", "kararsız", "ne iyi ne kötü", "inşallah",
        "fazla bir şey", "fark etmedim", "değişen bir şey", "klasik", "ama", "ancak","fark göremedim","stok yenilensin","yenilensin","stok yenile",
    ]
    
    # Skorları hesapla
    olumsuz_skor = sum(1 for kelime in olumsuz_kelimeler if kelime in yorum_kucuk)
    olumlu_skor = sum(1 for kelime in olumlu_kelimeler if kelime in yorum_kucuk)
    notr_skor = sum(1 for kelime in notr_kelimeler if kelime in yorum_kucuk)
    
    # Mantıksal karar mekanizması
    if olumlu_skor > olumsuz_skor and olumlu_skor >= notr_skor:
        return "Olumlu", 2
    elif olumsuz_skor > olumlu_skor and olumsuz_skor >= notr_skor:
        return "Olumsuz", 0
    elif notr_skor > 0 or (olumlu_skor == 0 and olumsuz_skor == 0):
        # Gerçekten nötr ibareler geçiyorsa veya belirgin kelime yoksa Nötr (1)
        return "Nötr", 1
    else:
        return "Nötr", 1

print("Yorumlar analiz ediliyor ve etiketleniyor...")
# Fonksiyonu tüm sütuna uygulayalım
sonuclar = df['Yorumlar'].apply(gelismis_duygu_etiketle)

# Sonuçları DataFrame'e ayrı sütunlar olarak ekleyelim
df['Duygu'] = [s[0] for s in sonuclar]
df['Etiket'] = [s[1] for s in sonuclar]

# Yeni dosyaya kaydedelim
yeni_dosya = "watsons_final_etiketli.csv"
df.to_csv(yeni_dosya, index=False, encoding="utf-8-sig", quoting=1)

print(f"✅ İşlem tamamlandı! Etiketlenmiş veri '{yeni_dosya}' dosyasına kaydedildi.")

# Dağılımı ekrana yazdıralım
print("\n--- Yeni Sınıf Dağılımı ---")
print(df['Duygu'].value_counts())
print("\nOransal Dağılım (%):")
print(df['Duygu'].value_counts(normalize=True) * 100)