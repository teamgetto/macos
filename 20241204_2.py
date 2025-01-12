from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
import torch

# MPS backend ile ilgili olası hataları engellemek için cpu'ya yönlendirme yapalım
torch.device('cpu')

# CNN/Daily Mail veri kümesini yükle
dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:80%]")
val_dataset = load_dataset("cnn_dailymail", "3.0.0", split="test[:20%]")

# Tokenizer ve model yükle
tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Eğitim parametreleri
training_args = TrainingArguments(
    output_dir="./results",  # Çıktı dizini
    evaluation_strategy="epoch",  # Değerlendirme stratejisi
    learning_rate=1e-5,  # Öğrenme hızı
    per_device_train_batch_size=4,  # Batch boyutu
    per_device_eval_batch_size=4,  # Değerlendirme için batch boyutu
    num_train_epochs=3,  # Epoch sayısı
    weight_decay=0.01,  # Ağırlık azalma oranı
    save_strategy="epoch",  # Model kaydetme stratejisi
    logging_dir="./logs",  # Log dizini
    logging_steps=10,  # Log adım sayısı
    load_best_model_at_end=True  # Eğitim sonunda en iyi modeli yükle
)


# Veri kümesini hazırlama (metin ve özet)
def preprocess_function(examples):
    inputs = examples["article"]  # CNN/Daily Mail'de "article" anahtarı
    targets = examples["highlights"]  # "highlights" özet kısmı
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=150, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


# Eğitim verilerini ön işleme
train_dataset = dataset.map(preprocess_function, batched=True)
val_dataset = val_dataset.map(preprocess_function, batched=True)


# MPS veya GPU üzerinde çalışmak için relative_position düzeltmesi ekleme
def fix_relative_position(model):
    """
    T5 modelinin relative position hatasını çözmek için
    relative_position tensörünü float32'ye dönüştürür.
    """

    def custom_forward(*args, **kwargs):
        # kwargs'dan input_ids'ı alalım
        input_ids = kwargs.get("input_ids", None)

        if input_ids is None:
            if len(args) > 0:
                input_ids = args[0]  # Eğer args'da varsa, args[0]'ı alalım
            else:
                raise ValueError("Modelin doğru bir şekilde input_ids parametresine ihtiyacı var.")

        # relative_position'u float32'ye dönüştür
        if 'relative_position' in kwargs:
            kwargs['relative_position'] = kwargs['relative_position'].float()

        # Modelin varsayılan forward fonksiyonunu çağır
        return model.original_forward(*args, **kwargs)

    # Modelin forward fonksiyonunu değiştir
    model.original_forward = model.forward
    model.forward = custom_forward
    return model


# Modeli düzelt ve eğitime başla
model = fix_relative_position(model)

# Trainer sınıfı ile modeli eğit
trainer = Trainer(
    model=model,  # Model
    args=training_args,  # Eğitim parametreleri
    train_dataset=train_dataset,  # Eğitim verisi
    eval_dataset=val_dataset  # Değerlendirme verisi
)

# Modeli eğit
trainer.train()

# Modeli kaydet
trainer.save_model("./t5_finetuned_cnn_dailymail")

# Sonuçları değerlendir
trainer.evaluate()
