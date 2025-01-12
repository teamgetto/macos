import os
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BartTokenizer, BartForConditionalGeneration
from simhash import Simhash
from sklearn.model_selection import train_test_split
import pandas as pd
from rouge_score import rouge_scorer
import numpy as np
import kaggle
import zipfile

# 1. Veri Yükleme ve Hazırlık

def download_kaggle_dataset(user, key, dataset="pariza/bbc-news-summary", download_path="bbc_dataset"):
    # Kaggle API kullanıcı ve anahtar bilgisi ile doğrulama
    os.environ['KAGGLE_USERNAME'] = user
    os.environ['KAGGLE_KEY'] = key

    # Veri setini indir
    kaggle.api.dataset_download_files(dataset, path=download_path, unzip=True)
    print(f"Dataset downloaded and extracted at {download_path}")

def load_dataset_by_category(dataset_path="bbc_dataset/BBC News Summary"):
    articles = []
    summaries = []
    categories = []

    articles_dir = os.path.join(dataset_path, "News Articles")
    summaries_dir = os.path.join(dataset_path, "Summaries")

    for category in os.listdir(articles_dir):
        category_articles_dir = os.path.join(articles_dir, category)
        category_summaries_dir = os.path.join(summaries_dir, category)

        if not os.path.isdir(category_articles_dir):
            continue

        for filename in os.listdir(category_articles_dir):
            article_path = os.path.join(category_articles_dir, filename)
            summary_path = os.path.join(category_summaries_dir, filename)

            if os.path.isfile(article_path) and os.path.isfile(summary_path):
                with open(article_path, 'r', encoding='latin1') as article_file:
                    articles.append(article_file.read().strip())
                with open(summary_path, 'r', encoding='latin1') as summary_file:
                    summaries.append(summary_file.read().strip())
                categories.append(category)

    return pd.DataFrame({"full_text": articles, "summary": summaries, "category": categories})

def preprocess_data(data):
    return data.fillna("").astype(str).str.lower().str.strip()

# 2. Dataset Özel Sınıfı
class SummarizationDataset(Dataset):
    def __init__(self, texts, summaries, tokenizer, max_len=512):
        self.texts = texts
        self.summaries = summaries
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        summary = self.summaries[idx]
        inputs = self.tokenizer(
            text, max_length=self.max_len, truncation=True, padding="max_length", return_tensors="pt"
        )
        targets = self.tokenizer(
            summary, max_length=self.max_len, truncation=True, padding="max_length", return_tensors="pt"
        )
        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": targets["input_ids"].squeeze(),
        }

# 3. Simhash ile Gruplama

def group_sentences(sentences, group_ratio=0.25):
    simhash_values = [Simhash(sentence).value for sentence in sentences]
    n_groups = max(1, int(len(sentences) * group_ratio))
    grouped = [[] for _ in range(n_groups)]

    # Gruplama: Hamming mesafesiyle benzer cümleleri grupla
    for i, h1 in enumerate(simhash_values):
        closest_group = None
        min_distance = float('inf')
        for g_idx in range(len(grouped)):
            if grouped[g_idx]:
                h2 = Simhash(grouped[g_idx][0]).value
                distance = bin(h1 ^ h2).count('1')
                if distance < min_distance:
                    closest_group = g_idx
                    min_distance = distance
        if closest_group is not None and min_distance < 10:  # Hamming eşik değeri
            grouped[closest_group].append(sentences[i])
        else:
            grouped.append([sentences[i]])

    return [group for group in grouped if group]

# 4. Transformer Modeli Eğitimi

def train_model(train_data, model_name="facebook/bart-large-cnn", epochs=1, batch_size=4):
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    dataset = SummarizationDataset(
        train_data['full_text'].tolist(), train_data['summary'].tolist(), tokenizer
    )
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    model.train()

    for epoch in range(epochs):
        total_loss = 0
        for batch in dataloader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["labels"]
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(dataloader)}")

    return model, tokenizer

# 5. Grupların Transformer Modeline Gönderilmesi ve Sıralama

def summarize_groups(groups, model, tokenizer):
    summaries = []
    for group in groups:
        input_text = " ".join(group)
        inputs = tokenizer.encode(
            input_text, return_tensors="pt", max_length=512, truncation=True
        )
        summary_ids = model.generate(
            inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True
        )
        summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))
    return summaries

# 6. Deneyler ve Değerlendirme

def evaluate_summaries(true_summaries, predicted_summaries):
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = []
    for ref, pred in zip(true_summaries, predicted_summaries):
        scores.append(scorer.score(ref, pred))
    avg_scores = {
        "rouge1": np.mean([score['rouge1'].fmeasure for score in scores]),
        "rouge2": np.mean([score['rouge2'].fmeasure for score in scores]),
        "rougeL": np.mean([score['rougeL'].fmeasure for score in scores]),
    }
    return avg_scores

def experiment(train_data, test_data, model_name="facebook/bart-large-cnn", group_ratio=0.25):
    print("\nStarting experiment with model:", model_name)
    model, tokenizer = train_model(train_data, model_name=model_name)

    predicted_summaries = []
    for text in test_data['full_text']:
        sentences = text.split('.')
        groups = group_sentences(sentences, group_ratio=group_ratio)
        group_summaries = summarize_groups(groups, model, tokenizer)
        predicted_summaries.append(" ".join(group_summaries))

    rouge_scores = evaluate_summaries(test_data['summary'], predicted_summaries)
    print("ROUGE Scores:", rouge_scores)

    return rouge_scores

def main(user, key):
    # Kaggle'dan veri setini indirme
    download_kaggle_dataset(user, key)

    # Veri setini yükleme ve hazırlama
    df = load_dataset_by_category()
    df['full_text'] = preprocess_data(df['full_text'])
    df['summary'] = preprocess_data(df['summary'])

    # Belirli bir kategori üzerinde çalışmak için filtreleme (örnek: "business")
    categories_to_experiment = ["business", "politics", "sport"]

    for category in categories_to_experiment:
        print(f"\nRunning experiments for category: {category}")
        category_data = df[df['category'] == category]

        # Veriyi bölme
        train_data, test_data = train_test_split(category_data, test_size=0.2, random_state=42)

        # Deneyler
        models = ["facebook/bart-large-cnn"]
        group_ratios = [0.25, 0.5]

        for model_name in models:
            for group_ratio in group_ratios:
                print(f"\nRunning experiment with group_ratio={group_ratio}")
                experiment(train_data, test_data, model_name=model_name, group_ratio=group_ratio)

if __name__ == "__main__":
    # Kullanıcı adı ve anahtar burada sağlanmalı
    kaggle_user = "ahmetoprak63"
    kaggle_key = "d5e75ac75f088da9d43c9afdd850ecf4"
    main(kaggle_user, kaggle_key)