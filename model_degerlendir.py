import evaluate
import numpy as np
import pandas as pd
from datasets import Dataset, Value
from sklearn.metrics import classification_report, confusion_matrix
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer

print('1. Test verisi yükleniyor ve hazırlanıyor...')
df = pd.read_csv('watsons_ikili_etiketli.csv', on_bad_lines='skip')
df = df.dropna(subset=['Yorumlar', 'Etiket'])

# Hugging Face Dataset formatına dönüştürme
dataset = Dataset.from_pandas(df[['Yorumlar', 'Etiket']])
dataset = dataset.rename_column('Yorumlar', 'text')
dataset = dataset.rename_column('Etiket', 'label')
dataset = dataset.cast_column('label', Value('int64'))

# Eğitimde kullandığımız aynı seed (42) ile train/test ayrımını yapiyoruz ki aynı test kümesi gelsin
dataset = dataset.train_test_split(test_size=0.2, seed=42)
test_dataset = dataset['test']

print('2. Eğittiğimiz yerel BERT modeli yükleniyor...')
model_path = './watsons_bert_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)


# Tokenize fonksiyonu
def tokenize_function(examples):
  return tokenizer(
      examples['text'], padding='max_length', truncation=True, max_length=128
  )


print('3. Test verileri tokenize ediliyor...')
tokenized_test = test_dataset.map(tokenize_function, batched=True)

# 4. Trainer ile tahmin (Prediction) alma
trainer = Trainer(model=model)

print('4. Test verisi üzerinde tahminler hesaplanıyor...')
predictions_output = trainer.predict(tokenized_test)
logits = predictions_output.predictions
y_true = predictions_output.label_ids
y_pred = np.argmax(logits, axis=-1)

# 5. Metrikleri Hesaplama ve Raporlama
accuracy_metric = evaluate.load('accuracy')
acc = accuracy_metric.compute(predictions=y_pred, references=y_true)

print('\n================ BERT MODEL DEĞERLENDİRME RAPORU ================' )
print(f'🎯 Doğruluk Oranı (Accuracy): % {acc["accuracy"] * 100:.2f}')
print('\nDetaylı Sınıflandırma Raporu (Precision, Recall, F1-Score):')
print(
    classification_report(
        y_true, y_pred, target_names=['Olumsuz (0)', 'Olumlu (1)']
    )
)
print('Confusion Matrix (Hata Matrisi):')
print(confusion_matrix(y_true, y_pred))
print('==================================================================')