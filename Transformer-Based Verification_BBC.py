import os
import pandas as pd
import numpy as np
import hashlib
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AdamW
import torch
from torch.utils.data import DataLoader
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk

# NLTK İndirme
nltk.download('wordnet')
nltk.download('punkt')

# Parametrelerin Merkezi Yönetimi
CONFIG = {
    "batch_size": 8,
    "learning_rate": 5e-5,
    "epochs": 4,
    "max_input_length": 512,
    "max_summary_length": 150,
    "min_summary_length": 40,
    "categories": ["sport", "business", "politics"],
    "doc_counts": [5, 50, 100],
    "output_dir": "saved_model",
    "results_file": "experiment_results.csv",
    "results_plot": "experiment_results.png"
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

# WordNet Spell Checker
def apply_wordnet_spell_checker(text):
    tokens = word_tokenize(text)
    corrected_tokens = []
    for token in tokens:
        if wordnet.synsets(token):
            corrected_tokens.append(token)
        else:
            suggestions = wordnet.synsets(token)
            if suggestions:
                corrected_tokens.append(suggestions[0].lemmas()[0].name())
            else:
                corrected_tokens.append(token)
    return ' '.join(corrected_tokens)

# Simhash Algoritması
def calculate_simhash_similarity(text1, text2):
    hash1 = int(hashlib.md5(text1.encode()).hexdigest(), 16)
    hash2 = int(hashlib.md5(text2.encode()).hexdigest(), 16)
    hamming_distance = bin(hash1 ^ hash2).count('1')
    return 1 - (hamming_distance / 128)

# Cross Encoder Benzerlik
def calculate_cross_encoder_similarity(model, tokenizer, text1, text2):
    inputs = tokenizer(text1, text2, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    similarity_score = torch.sigmoid(outputs.logits).item()
    return similarity_score

# Transformer Modeli Eğitimi
def train_transformer_model(dataset, model, tokenizer):
    def tokenize_data(example):
        inputs = tokenizer(example["content"], truncation=True, padding="max_length", max_length=CONFIG["max_input_length"], return_tensors="pt")
        labels = tokenizer(example["summary"], truncation=True, padding="max_length", max_length=CONFIG["max_summary_length"], return_tensors="pt")
        return inputs, labels

    tokenized_data = [(tokenize_data(row)) for _, row in dataset.iterrows()]
    dataloader = DataLoader(tokenized_data, batch_size=CONFIG["batch_size"], shuffle=True)

    optimizer = AdamW(model.parameters(), lr=CONFIG["learning_rate"], eps=1e-8)
    model.train()

    for epoch in range(CONFIG["epochs"]):
        total_loss = 0
        for inputs, labels in dataloader:
            # Ensure inputs are properly formatted
            inputs = {k: v.squeeze(1).to(model.device) for k, v in inputs.items()}
            labels = labels["input_ids"].squeeze(1).to(model.device)

            outputs = model(input_ids=inputs["input_ids"],
                            attention_mask=inputs["attention_mask"],
                            labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss:.4f}")

    return model

# Özet Üretimi
def generate_summary(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=CONFIG["max_input_length"])
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    summary_ids = model.generate(inputs["input_ids"], max_length=CONFIG["max_summary_length"], min_length=CONFIG["min_summary_length"], length_penalty=2.0, num_beams=4)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Deneyler
def experiment(model, tokenizer, data, category, doc_counts, use_spell_checker=False):
    if use_spell_checker:
        print("WordNet Spell Checker uygulanıyor...")
        data["content"] = data["content"].apply(apply_wordnet_spell_checker)
        data["summary"] = data["summary"].apply(apply_wordnet_spell_checker)

    filtered_data = data[data["category"] == category]

    results = {}
    for count in doc_counts:
        print(f"Processing {count} documents from category: {category}")
        subset = filtered_data.sample(n=min(count, len(filtered_data)))

        simhash_scores = []
        cross_encoder_scores = []

        for _, row in subset.iterrows():
            generated_summary = generate_summary(model, tokenizer, row["content"])
            simhash_score = calculate_simhash_similarity(row["summary"], generated_summary)
            cross_encoder_score = calculate_cross_encoder_similarity(model, tokenizer, row["summary"], generated_summary)

            simhash_scores.append(simhash_score)
            cross_encoder_scores.append(cross_encoder_score)

        avg_simhash = np.mean(simhash_scores)
        avg_cross_encoder = np.mean(cross_encoder_scores)

        results[count] = {
            "simhash": avg_simhash,
            "cross_encoder": avg_cross_encoder
        }

    return results

# Sonuçları Kaydetme ve Görselleştirme
def save_and_plot_results(results, output_file, output_plot):
    df = pd.DataFrame(results).T
    df.to_csv(output_file, index_label="Document Count")
    print(f"Results saved to {output_file}")

    df.plot(kind="bar", figsize=(10, 6))
    plt.title("Experiment Results")
    plt.ylabel("Scores")
    plt.xlabel("Document Count")
    plt.grid(axis="y")
    plt.savefig(output_plot)
    plt.show()

# Modeli Kaydetme Fonksiyonu
def save_model(model, tokenizer, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model and tokenizer saved to {output_dir}")

# Ana Süreç
if __name__ == "__main__":
    print("Veri hazırlanıyor...")
    bbc_data = download_and_prepare_bbc_dataset()

    print("Model yükleniyor...")
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    print("Model eğitiliyor...")
    model = train_transformer_model(bbc_data, model, tokenizer)

    print("Model kaydediliyor...")
    save_model(model, tokenizer, CONFIG["output_dir"])

    all_results = {}
    for category in CONFIG["categories"]:
        print(f"Experiment I for category: {category} (WordNet Spell Checker ile)")
        results_i = experiment(model, tokenizer, bbc_data, category, CONFIG["doc_counts"], use_spell_checker=True)
        all_results[f"{category}_with_spell_checker"] = results_i

        print(f"Experiment II for category: {category} (WordNet Spell Checker olmadan)")
        results_ii = experiment(model, tokenizer, bbc_data, category, CONFIG["doc_counts"], use_spell_checker=False)
        all_results[f"{category}_without_spell_checker"] = results_ii

    print("Sonuçlar kaydediliyor ve görselleştiriliyor...")
    save_and_plot_results(all_results, CONFIG["results_file"], CONFIG["results_plot"])