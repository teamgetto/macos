from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

# Veri kümesini yükle
# Veri kümesini yükle
dataset = load_dataset("reuters21578", split="train[:80%]", trust_remote_code=True)
val_dataset = load_dataset("reuters21578", split="test[:20%]", trust_remote_code=True)


# Tokenizer ve model yükle
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Eğitim parametreleri
training_args = TrainingArguments(
    output_dir="./results",          # Çıktı dizini
    evaluation_strategy="epoch",     # Değerlendirme stratejisi
    learning_rate=1e-9,              # Öğrenme hızı
    per_device_train_batch_size=64,  # Batch boyutu
    per_device_eval_batch_size=64,   # Değerlendirme için batch boyutu
    num_train_epochs=2,              # Epoch sayısı
    weight_decay=0.01,               # Ağırlık azalma oranı
    save_strategy="epoch",           # Model kaydetme stratejisi
    logging_dir="./logs",            # Log dizini
    logging_steps=10,                # Log adım sayısı
    load_best_model_at_end=True      # Eğitim sonunda en iyi modeli yükle
)

# Veri kümesini hazırlama
def preprocess_function(examples):
    inputs = examples["text"]
    targets = examples["summary"]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=150, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Eğitim verilerini ön işleme
train_dataset = dataset.map(preprocess_function, batched=True)
val_dataset = val_dataset.map(preprocess_function, batched=True)

# Trainer sınıfı ile modeli eğit
trainer = Trainer(
    model=model,                         # Model
    args=training_args,                  # Eğitim parametreleri
    train_dataset=train_dataset,         # Eğitim verisi
    eval_dataset=val_dataset             # Değerlendirme verisi
)

# Modeli eğit
trainer.train()

# Modeli kaydet
trainer.save_model("./t5_finetuned_reuters")

# Sonuçları değerlendir
trainer.evaluate()
