from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# FastAPI uygulamasını başlatıyoruz
app = FastAPI(
    title="Watsons BERT Duygu Analizi API",
    description="Fine-tune edilmiş Türkçe BERT modeli ile e-ticaret duygu analizi servisi",
    version="1.0"
)

# Eğittiğimiz BERT modelini ve tokenizer'ı yerel klasörden yüklüyoruz
print("Eğitilmiş BERT modeli yükleniyor...")
model_path = "./watsons_bert_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval() # Değerlendirme moduna alıyoruz
print("✔ BERT modeli başarıyla yüklendi, API hazır!")

# İstek gövdesi (Request Body) tanımı
class YorumIstegi(BaseModel):
    yorum: str

@app.get("/")
def anasayfa():
    return {"mesaj": "Watsons BERT Duygu Analizi API sistemine hoş geldiniz! 🚀 /docs adresinden test edebilirsiniz."}

@app.post("/predict")
def duygu_tahmini(veri: YorumIstegi):
    # 1. Metni BERT formatına tokenize et
    inputs = tokenizer(veri.yorum, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    # 2. Model ile tahmin yap
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        
    # 3. Olasılıkları ve sınıfı hesapla
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    tahmin_idx = torch.argmax(probabilities, dim=-1).item()
    guven_skoru = probabilities[0][tahmin_idx].item()
    
    duygu_sonucu = "Olumlu" if tahmin_idx == 1 else "Olumsuz"
    
    return {
        "girilen_yorum": veri.yorum,
        "tahmin_edilen_duygu": duygu_sonucu,
        "etiket_kodu": int(tahmin_idx),
        "guven_orani_yuzde": round(guven_skoru * 100, 2)
    }