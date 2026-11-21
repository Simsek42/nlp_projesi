import streamlit as st
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Sayfa yapılandırması
st.set_page_config(
    page_title="Watsons BERT Duygu Analizi",
    page_icon="🛍️",
    layout="centered"
)

# Eğittiğimiz BERT modelini ve tokenizer'ı önbelleğe alarak yüklüyoruz
@st.cache_resource
def model_ve_tokenizer_yukle():
    model_path = "./watsons_bert_model"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    return model, tokenizer

with st.spinner("Yapay zeka modeli yükleniyor, lütfen bekleyin..."):
    model, tokenizer = model_ve_tokenizer_yukle()

# Arayüz Tasarımı
st.title("🛍️ Watsons E-Ticaret Yorumları BERT Duygu Analizi")
st.write("Bu uygulama, fine-tune edilmiş **Türkçe BERT** modeli kullanarak Watsons ürün yorumlarının duygu durumunu **%98 doğrulukla** analiz eder.")

st.markdown("---")

# Kullanıcıdan metin alma kutusu
yorum_input = st.text_area(
    "💬 Analiz edilmesini istediğiniz Watsons ürün yorumunu yazın:",
    placeholder="Örn: Kargo inanılmaz hızlıydı ve ürünün paketlenmesi harikaydı, bayıldım!",
    height=130
)

# Analiz Butonu
if st.button("BERT ile Duygu Analizini Çalıştır 🚀", type="primary"):
    if not yorum_input.strip():
        st.warning("⚠️ Lütfen boş bir yorum girmeyin!")
    else:
        with st.spinner("Yapay zeka yorumu inceliyor..."):
            # 1. Tokenize etme
            inputs = tokenizer(yorum_input, return_tensors="pt", truncation=True, padding=True, max_length=128)
            
            # 2. Model tahmini
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                
            # 3. Olasılık ve skor hesaplama
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            tahmin_idx = torch.argmax(probabilities, dim=-1).item()
            guven_skoru = probabilities[0][tahmin_idx].item()
            
            duygu_sonucu = "Olumlu" if tahmin_idx == 1 else "Olumsuz"
            
        # 4. Sonucu şık bir şekilde ekrana yazdırma
        st.markdown("### 📊 Analiz Sonucu:")
        
        if tahmin_idx == 1:
            st.success(f"**Sonuç: OLUMLU 😊** (Model Güven Oranı: %{round(guven_skoru * 100, 2)})")
        else:
            st.error(f"**Sonuç: OLUMSUZ 😞** (Model Güven Oranı: %{round(guven_skoru * 100, 2)})")