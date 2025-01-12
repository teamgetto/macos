import torch
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig
from transformers import Trainer, TrainingArguments
from datasets import load_dataset

# Veri setini yükleme
dataset = load_dataset('gopalkalpande/bbc-news-summary')

# Tokenizer ve Modeli yükleme
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Tokenizasyon işlemi
def tokenize_data(example):
    return tokenizer(example['Articles'], example['Summaries'], truncation=True, padding='max_length', max_length=512)

tokenized_datasets = dataset.map(tokenize_data, batched=True)

# Eğitim argümanları
training_args = TrainingArguments(
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    evaluation_strategy="steps",
    eval_steps=500,
    logging_dir='./logs',
    logging_steps=500,
    save_strategy="steps",
    save_steps=500,
    remove_unused_columns=False,
    push_to_hub=False,
    report_to="none",
    logging_first_step=True,
    load_best_model_at_end=True,
    save_total_limit=2,
    num_train_epochs=1, # Daha uzun eğitim için bu değeri artırabilirsiniz.
    output_dir="./results",
)

# Model eğitimi
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
)

trainer.train()

# Modeli kaydetme
model.save_pretrained("./saved_model")
tokenizer.save_pretrained("./saved_model")

# Modeli yükleme
loaded_tokenizer = BartTokenizer.from_pretrained("./saved_model")
loaded_model = BartForConditionalGeneration.from_pretrained("./saved_model")

# Özetleme işlemi
def summarize(document):
    inputs = loaded_tokenizer(document, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = loaded_model.generate(inputs["input_ids"])
    summary = loaded_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Özetleme işlemi için örnek test
document = "ahmet toprak 1994 de doğdu."
print(summarize(document))
