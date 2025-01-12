import os
import pandas as pd
import numpy as np
import hashlib
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, BertForTokenClassification
from torch.optim import AdamW
import torch
from torch.utils.data import DataLoader, Dataset
from textblob import TextBlob
import re
import nltk
from nltk.tokenize import word_tokenize
from termcolor import colored
import logging

# Logging Ayarları
logging.basicConfig(filename="training.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# NLTK İndirme
nltk.download('punkt')

# GPU Kontrolü
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(colored(f"Model {device} üzerinde çalışıyor.", "green"))
logging.info(f"Model {device} üzerinde çalışıyor.")

# Parametrelerin Merkezi Yönetimi
CONFIG = {
    "batch_size": 32,
    "learning_rate": 1e-4,
    "epochs": 16,
    "max_len": 512,
    "num_labels": 8,
    "doc_counts": [5, 50, 100],
    "output_dir": "saved_ner_model",
    "results_file": "experiment_results.csv",
    "results_plot": "experiment_results.png",
    "patience": 3  # Early stopping için sabır değeri
}

# Veri İndirme ve İşleme
def download_and_prepare_bbc_dataset():
    os.environ['KAGGLE_USERNAME'] = "ahmetoprak63"
    os.environ['KAGGLE_KEY'] = "d5e75ac75f088da9d43c9afdd850ecf4"

    os.system("kaggle datasets download -d pariza/bbc-news-summary")
    os.system("unzip -o bbc-news-summary.zip -d bbc_dataset")

    articles = []
    data_path = "bbc_dataset/BBC News Summary/News Articles"
    for category in os.listdir(data_path):
        category_path = os.path.join(data_path, category)
        for file in os.listdir(category_path):
            file_path = os.path.join(category_path, file)
            with open(file_path, "r", encoding="latin1") as f:
                content = f.read()
                summary_path = os.path.join("bbc_dataset/BBC News Summary/Summaries", category, file)
                with open(summary_path, "r", encoding="latin1") as s:
                    summary = s.read()
                    articles.append({"category": category, "content": content, "summary": summary})

    df = pd.DataFrame(articles)
    return df

# TextBlob Spell Checker
def apply_textblob_spell_checker(text):
    blob = TextBlob(text)
    return str(blob.correct())

# Regex Kuralları
def apply_regex_rules(text):
    patterns = {
        'monetary': r'\b(?:\$|€|£)?\d+[.,]?\d*%?\b',
        'email': r'[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}',
        'percentage': r'\b\d+[.,]?\d*%\b',
        'phone_number': r'\b\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',
        'date': r'\b(?:\d{1,2}[/-])?(?:\d{1,2}[/-])?\d{2,4}\b',
        'time': r'\b\d{1,2}:\d{2}(?:\s?[APap][Mm])?\b',
        'url': r'\bhttps?://[\w.-]+(?:\.[a-zA-Z]{2,})+\S*\b',
        'hashtag': r'#\w+',
        'mention': r'@\w+'
    }
    for key, pattern in patterns.items():
        text = re.sub(pattern, lambda x: x.group(0).upper(), text)
    return text

# Simhash Algoritması
def calculate_simhash_similarity(text1, text2):
    hash1 = int(hashlib.md5(text1.encode()).hexdigest(), 16)
    hash2 = int(hashlib.md5(text2.encode()).hexdigest(), 16)
    hamming_distance = bin(hash1 ^ hash2).count('1')
    return 1 - (hamming_distance / 128)

# Named Entity Recognition (NER) Modeli Eğitimi
class CustomDataset(Dataset):
    def __init__(self, data, tokenizer, max_len):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data.iloc[index]
        inputs = self.tokenizer(row['content'], truncation=True, padding="max_length", max_length=self.max_len, return_tensors="pt")
        labels = self.tokenizer(row['summary'], truncation=True, padding="max_length", max_length=self.max_len, return_tensors="pt")['input_ids']
        return inputs['input_ids'].squeeze(), labels.squeeze()

# Model Eğitimi (Erken Durdurma ile)
def train_ner_model(dataset, model, tokenizer):
    dataloader = DataLoader(CustomDataset(dataset, tokenizer, max_len=CONFIG["max_len"]), batch_size=CONFIG["batch_size"], shuffle=True)

    optimizer = AdamW(model.parameters(), lr=CONFIG["learning_rate"])
    model.to(device)
    model.train()

    start_time = time.time()
    patience_counter = 0
    best_loss = float('inf')

    for epoch in range(CONFIG["epochs"]):
        total_loss = 0
        for inputs, labels in tqdm(dataloader, desc=f"Epoch {epoch + 1}/{CONFIG['epochs']}"):
            inputs, labels = inputs.to(device), labels.to(device)
            attention_mask = (inputs != tokenizer.pad_token_id).to(device)

            # Etiketleri doğrula ve düzelt
            if labels.max() >= CONFIG["num_labels"]:
                print(colored(f"Geçersiz etiket tespit edildi: {labels.max().item()}", "red"))
                labels = labels.clamp(0, CONFIG["num_labels"] - 1)

            outputs = model(input_ids=inputs, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += loss.item()

        print(colored(f"Epoch {epoch + 1}, Loss: {total_loss:.4f}", "yellow"))
        logging.info(f"Epoch {epoch + 1}, Loss: {total_loss:.4f}")

        # Early Stopping
        if total_loss < best_loss:
            best_loss = total_loss
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= CONFIG["patience"]:
                print(colored("Erken durdurma tetiklendi.", "red"))
                logging.info("Erken durdurma tetiklendi.")
                break

    elapsed_time = time.time() - start_time
    print(colored(f"Eğitim tamamlandı. Toplam süre: {elapsed_time:.2f} saniye.", "green"))
    logging.info(f"Eğitim tamamlandı. Toplam süre: {elapsed_time:.2f} saniye.")

    return model

# Doğruluk Hesaplama
def calculate_accuracy(named_entities_summary, named_entities_original):
    named_entities_summary = [item for sublist in named_entities_summary for item in sublist]
    named_entities_original = [item for sublist in named_entities_original for item in sublist]
    sm = len(set(named_entities_summary) & set(named_entities_original))
    st = len(named_entities_summary)
    return (sm / st) * 100 if st > 0 else 0

# Deneyler
def experiment(data, model, tokenizer):
    results = {}
    start_time = time.time()

    for count in CONFIG["doc_counts"]:
        subset = data.sample(n=min(count, len(data)))
        accuracies = []
        for _, row in tqdm(subset.iterrows(), total=len(subset), desc=f"Processing {count} documents"):
            original_text = apply_textblob_spell_checker(row['content'])
            original_text = apply_regex_rules(original_text)
            summary_text = apply_textblob_spell_checker(row['summary'])
            summary_text = apply_regex_rules(summary_text)

            named_entities_original = tokenizer(original_text, return_tensors="pt", truncation=True, padding=True)['input_ids'].tolist()
            named_entities_summary = tokenizer(summary_text, return_tensors="pt", truncation=True, padding=True)['input_ids'].tolist()

            accuracy = calculate_accuracy(named_entities_summary, named_entities_original)
            accuracies.append(accuracy)

        results[count] = np.mean(accuracies)

    elapsed_time = time.time() - start_time
    print(colored(f"Deneyler tamamlandı. Toplam süre: {elapsed_time:.2f} saniye.", "blue"))
    logging.info(f"Deneyler tamamlandı. Toplam süre: {elapsed_time:.2f} saniye.")

    return results

# Sonuçları Kaydetme ve Görselleştirme
def save_and_plot_results(results):
    # Sonuçları CSV olarak kaydetme
    df = pd.DataFrame(list(results.items()), columns=["Document Count", "Accuracy"])
    df.to_csv(CONFIG["results_file"], index=False)
    print(colored(f"Sonuçlar {CONFIG['results_file']} dosyasına kaydedildi.", "cyan"))
    logging.info(f"Sonuçlar {CONFIG['results_file']} dosyasına kaydedildi.")

    # Sonuçları görselleştirme
    plt.figure(figsize=(8, 6))
    plt.plot(df["Document Count"], df["Accuracy"], marker="o", linestyle="-", label="Accuracy")
    plt.title("Experiment Results")
    plt.xlabel("Document Count")
    plt.ylabel("Accuracy (%)")
    plt.grid(True)
    plt.legend()
    plt.savefig(CONFIG["results_plot"])
    print(colored(f"Sonuçlar grafiği {CONFIG['results_plot']} dosyasına kaydedildi.", "magenta"))
    logging.info(f"Sonuçlar grafiği {CONFIG['results_plot']} dosyasına kaydedildi.")
    plt.show()

# Modeli Kaydetme Fonksiyonu
def save_model(model, tokenizer):
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    model.save_pretrained(CONFIG["output_dir"])
    tokenizer.save_pretrained(CONFIG["output_dir"])
    print(colored(f"Model ve tokenizer {CONFIG['output_dir']} dizinine kaydedildi.", "green"))
    logging.info(f"Model ve tokenizer {CONFIG['output_dir']} dizinine kaydedildi.")

# Ana Süreç
if __name__ == "__main__":
    print(colored("Veri hazırlanıyor...", "cyan"))
    bbc_data = download_and_prepare_bbc_dataset()

    print(colored("Model yükleniyor...", "cyan"))
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    model = BertForTokenClassification.from_pretrained("bert-base-cased", num_labels=CONFIG["num_labels"])

    print(colored("Model eğitiliyor...", "cyan"))
    model = train_ner_model(bbc_data, model, tokenizer)

    print(colored("Model kaydediliyor...", "cyan"))
    save_model(model, tokenizer)

    print(colored("Deneyler başlatılıyor...", "cyan"))
    results = experiment(bbc_data, model, tokenizer)
    print(colored(f"Deney sonuçları: {results}", "cyan"))

    print(colored("Sonuçlar kaydediliyor ve görselleştiriliyor...", "cyan"))
    save_and_plot_results(results)
