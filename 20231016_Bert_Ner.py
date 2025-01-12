import torch
from transformers import BertForTokenClassification, BertTokenizerFast, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

# Veriyi yükleme
dataset = load_dataset("conll2003")

# Tokenizer ve Modeli yükleme
model_name = "dbmdz/bert-base-cased-finetuned-conll03-english"
tokenizer = BertTokenizerFast.from_pretrained(model_name)  # Fast tokenizer kullanıldı
model = BertForTokenClassification.from_pretrained(model_name)

# Tokenizasyon işlemi
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, padding="max_length", is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)

# Eğitim argümanları
training_args = TrainingArguments(
    per_device_train_batch_size=64,
    num_train_epochs=2,
    evaluation_strategy="epoch",
    logging_dir="./logs",
    save_strategy="epoch",
    output_dir="./results",
    logging_steps=1,
)

# Model eğitimi
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
)

trainer.train()

# Modeli kaydetme
model.save_pretrained("./ner_model")
tokenizer.save_pretrained("./ner_model")

# Modeli yükleme
loaded_tokenizer = BertTokenizerFast.from_pretrained("./ner_model")
loaded_model = BertForTokenClassification.from_pretrained("./ner_model")

# Named Entity Recognition işlemi
def ner(text):
    tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))
    inputs = tokenizer.encode(text, return_tensors="pt")
    outputs = loaded_model(inputs).logits
    predictions = torch.argmax(outputs, dim=2)
    id2label = {i: label for i, label in enumerate(dataset["train"].features["ner_tags"].feature)}
    labels = [id2label[prediction] for prediction in predictions[0].tolist()]
    return list(zip(tokens, labels))

# Örnek
text = "Hugging Face is a French company that is based in New York City."
print(ner(text))