from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

driver = webdriver.Chrome()

try:
    # Hedef ürün linki
    url = "https://www.gratis.com/tirnak-bakim-urunleri/mixup-sulphur-tirnak-bakim-yagi-p-10135026" 
    
    driver.get(url)
    print("Ürün sayfası açıldı...")
    time.sleep(4)
    
    # "Yorumlar" sekmesine otomatik tıklama
    try:
        yorumlar_sekmesi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Yorumlar' or text()='Yorumlar']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", yorumlar_sekmesi)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", yorumlar_sekmesi)
        print("✔ 'Yorumlar' sekmesine başarıyla tıklandı!")
        time.sleep(3)
    except Exception as e:
        print("⚠ Yorumlar sekmesi zaten açık veya bulunamadı:", e)
    
    tum_toplanan_yorumlar = []
    toplam_sayfa_sayisi = 19  # Toplam sayfa sayısı
    
    for sayfa in range(1, toplam_sayfa_sayisi + 1):
        print(f"\n--- Sayfa {sayfa} taranıyor ---")
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 400);")
        time.sleep(3)
        
        try:
            yorum_elementleri = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.text-xs.text-primary-850.break-words"))
            )
            
            sayfa_ici_sayac = 0
            for el in yorum_elementleri:
                try:
                    metin = el.text.strip()
                    if metin and metin not in tum_toplanan_yorumlar:
                        tum_toplanan_yorumlar.append(metin)
                        sayfa_ici_sayac += 1
                except Exception:
                    continue
            print(f"Bu sayfadan {sayfa_ici_sayac} yeni yorum alındı.")
            
        except Exception as e:
            print(f"Sayfa {sayfa} üzerinde yorumlar yüklenirken sorun oluştu:", e)
            break
        
        # Sonraki sayfa numarasına tıklama
        if sayfa < toplam_sayfa_sayisi:
            try:
                hedef_sayfa = str(sayfa + 1)
                sonraki_sayfa_butonu = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'cursor-pointer') and normalize-space()='{hedef_sayfa}']"))
                )
                
                driver.execute_script("arguments[0].scrollIntoView(true);", sonraki_sayfa_butonu)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", sonraki_sayfa_butonu)
                
                print(f"Sayfa {hedef_sayfa}'ye tıklandı, yeni yorumlar bekleniyor...")
                time.sleep(4)
                
            except Exception as e:
                print(f"Sonraki sayfaya ({sayfa + 1}) geçilemedi (Son sayfaya ulaşılmış olabilir):", e)
                break

    print(f"\n✨ Bu oturumda toplanan benzersiz yorum sayısı: {len(tum_toplanan_yorumlar)}")
    
    # Hedef dosya adı
    dosya_adi = "watsons_yorumlar.csv"
    yeni_df = pd.DataFrame(tum_toplanan_yorumlar, columns=["Yorumlar"])
    
    # Dosya birleştirme ve kaydetme mantığı
    if os.path.exists(dosya_adi):
        try:
            eski_df = pd.read_csv(dosya_adi, on_bad_lines='skip')
            print(f"Mevcut '{dosya_adi}' dosyası okundu. İçinde {len(eski_df)} satır var.")
        except Exception as e:
            print("Eski dosya okunurken hata oluştu, sıfırdan oluşturuluyor:", e)
            eski_df = pd.DataFrame(columns=["Yorumlar"])
            
        toplam_df = pd.concat([eski_df, yeni_df], ignore_index=True)
        toplam_df = toplam_df.drop_duplicates(subset=["Yorumlar"])
        toplam_df.to_csv(dosya_adi, index=False, encoding="utf-8-sig", quoting=1)
        print(f"✅ Başarıyla birleştirildi! Toplam benzersiz satır sayısı: {len(toplam_df)}")
    else:
        yeni_df = yeni_df.drop_duplicates(subset=["Yorumlar"])
        yeni_df.to_csv(dosya_adi, index=False, encoding="utf-8-sig", quoting=1)
        print(f"✅ '{dosya_adi}' dosyası ilk kez oluşturuldu ve kaydedildi! Toplam satır: {len(yeni_df)}")

except Exception as e:
    print("Bir hata oluştu (Detay):", e)

finally:
    input("\nİşlem tamamlandı. Kapatmak için Enter'a basın...")
    driver.quit()