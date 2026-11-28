import os
import site

print("Zemberek NumPy 2.x uyumluluk yaması uygulanıyor...")
patched = False

for site_dir in site.getsitepackages():
    target_file = os.path.join(site_dir, 'zemberek', 'lm', 'compression', 'gram_data_array.py')
    if os.path.exists(target_file):
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Hata veren kısımdaki int8 taşmasını engellemek için Python int tipine dönüştürüyoruz
        old_code = "return d[page_index] & 255"
        new_code = "return int(d[page_index]) & 255"
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Zemberek gram_data_array.py başarıyla yamalandı!")
            patched = True
            break
        else:
            # Satırda küçük boşluk farkı ihtimaline karşı genel arama
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if "d[page_index]" in line and "& 255" in line and "int(" not in line:
                    line = line.replace("d[page_index]", "int(d[page_index])")
                    patched = True
                new_lines.append(line)
            if patched:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                print("✅ Zemberek satır bazlı yamalandı!")
                break

if not patched:
    print("⚠️ Dosya bulunamadı veya eşleşme sağlanamadı.")