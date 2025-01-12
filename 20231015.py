import os
import pandas as pd
from torch.utils.data import Dataset
from transformers import BartForConditionalGeneration, BartTokenizer, Trainer, TrainingArguments
import torch

# Veri setini okuma
def read_file_pair(article_path, summary_path, topic, num_files):
    articles = []
    summaries = []
    for i in range(1, num_files + 1):
        filename = f"{i:03}.txt"
        with open(os.path.join(article_path, topic, filename), 'r', encoding="utf-8", errors='ignore') as a_file:
            articles.append(a_file.read())
        with open(os.path.join(summary_path, topic, filename), 'r', encoding="utf-8", errors='ignore') as s_file:
            summaries.append(s_file.read())
    return articles, summaries

NUM_FILES = 510
train_articles, train_summaries = read_file_pair("/Users/ahmettoprak/Desktop/BBC News Summary/BBC News Summary/News Articles", "/Users/ahmettoprak/Desktop/BBC News Summary/BBC News Summary/Summaries", "business", NUM_FILES)

# Tokenizer ve Modeli yükleme
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
device = torch.device("cpu")
model = model.to(device)

# Dataset sınıfı
class BBCDataset(Dataset):
    def __init__(self, articles, summaries):
        self.articles = articles
        self.summaries = summaries
    def __len__(self):
        return len(self.articles)
    def __getitem__(self, idx):
        article = self.articles[idx]
        summary = self.summaries[idx]
        tokenized_article = tokenizer(article, return_tensors="pt", max_length=512, truncation=True, padding='max_length')
        tokenized_summary = tokenizer(summary, return_tensors="pt", max_length=512, truncation=True, padding='max_length')
        return {
            "input_ids": tokenized_article["input_ids"].squeeze(),
            "attention_mask": tokenized_article["attention_mask"].squeeze(),
            "labels": tokenized_summary["input_ids"].squeeze()
        }

# Dataset oluşturma
train_dataset = BBCDataset(train_articles, train_summaries)

# Eğitim argümanları
training_args = TrainingArguments(
    per_device_train_batch_size=4,
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
    num_train_epochs=1,
    output_dir="./results",
)

# Model eğitimi
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
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
document = """Mr Elgindy was convicted of racketeering, securities fraud and extortion. Defense lawyers contended that Mr Royer had been feeding information to Mr Elgindy and another trader in an attempt to expose corporate fraud. Mr Royer was convicted of racketeering, securities fraud, obstruction of justice and witness tampering. Mr Elgindy had been trying to sell stock prior to the attack and had predicted a slump in the market. "Under the guise of protecting investors from fraud, Royer and Elgindy used the FBI's crime-fighting tools and resources actually to defraud the public," said US Attorney Roslynn Mauskopf. When the guilty verdict was announced by the jury foreman, Mr Elgindy dropped his face into his hands and sobbed, the Associated Press news agency reported. The charges carry sentences of up to 20 years."""
print(summarize(document))
