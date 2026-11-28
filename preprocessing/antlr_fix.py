import os
import site

print("ANTLR4 kütüphanesi Python 3.13 uyumluluğu için güncelleniyor...")
duzeltilen_dosya_sayisi = 0

for site_dir in site.getsitepackages():
    antlr_dir = os.path.join(site_dir, 'antlr4')
    if os.path.exists(antlr_dir):
        for root, dirs, files in os.walk(antlr_dir):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if 'from typing.io import' in content:
                            new_content = content.replace('from typing.io import', 'from typing import')
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            duzeltilen_dosya_sayisi += 1
                    except Exception as e:
                        pass

print(f"✅ İşlem tamamlandı! Toplam {duzeltilen_dosya_sayisi} dosya güncellendi.")