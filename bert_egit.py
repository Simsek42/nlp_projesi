import evaluate
import numpy as np
import pandas as pd
from datasets import Dataset, Value
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

print('1. Veri seti yükleniyor...')
df = pd.read_csv('watsons_ikili_etiketli.csv', on_bad_lines='skip')
df = df.dropna(subset=['Yorumlar', 'Etiket'])

# Hugging Face Dataset formatına dönüştürme
dataset = Dataset.from_pandas(df[['Yorumlar', 'Etiket']])
dataset = dataset.rename_column('Yorumlar', 'text')
dataset = dataset.rename_column('Etiket', 'label')

# Etiket sütununu açıkça tam sayı (integer) olarak ayarlıyoruz (Boyut hatasını önler)
dataset = dataset.cast_column('label', Value('int64'))

# Veriyi Train (%80) ve Test (%20) olarak ayır
dataset = dataset.train_test_split(test_size=0.2, seed=42)

print('2. Türkçe BERT modeli ve Tokenizer yükleniyor...')
model_name = 'dbmdz/bert-base-turkish-cased'
tokenizer = AutoTokenizer.from_pretrained(model_name)


def tokenize_function(examples):
  return tokenizer(
      examples['text'], padding='max_length', truncation=True, max_length=128
  )


print('3. Metinler BERT formatına tokenize ediliyor...')
tokenized_datasets = dataset.map(tokenize_function, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2
)

# Başarı metriği (Accuracy) tanımlama
metric = evaluate.load('accuracy')


def compute_metrics(eval_pred):
  logits, labels = eval_pred
  predictions = np.argmax(logits, axis=-1)
  return metric.compute(predictions=predictions, references=labels)


# 4. Eğitim Argümanları
training_args = TrainingArguments(
    output_dir='./watsons-bert-results',
    eval_strategy='epoch',
    save_strategy='epoch',
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    push_to_hub=True,  # Modeli otomatik Hugging Face Hub'a yükler
    hub_model_id='watsons-sentiment-bert-tr',  # Hugging Face'deki repo adın
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
    compute_metrics=compute_metrics,
)

print('4. BERT Model Eğitimi (Fine-Tuning) Başladı! Bu biraz sürebilir...')
trainer.train()

# Yerel olarak kaydetme
trainer.save_model('./watsons_bert_model')
tokenizer.save_pretrained('./watsons_bert_model')
print(
    '\n🎉 İŞLEM TAMAM! BERT modeli eğitildi, yerel olarak kaydedildi ve'
    ' Hugging Face Hub\'a yüklendi!'
)