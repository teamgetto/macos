import os
import pandas as pd
from datasets import load_dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification, AdamW
import torch
from torch.utils.data import DataLoader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Veri İndirme ve Ön İşleme
def download_and_prepare_dataset():
    # Kaggle API anahtarınızın yüklü olduğundan emin olun
    os.environ['KAGGLE_USERNAME'] = "ahmetoprak63"
    os.environ['KAGGLE_KEY'] = "d5e75ac75f088da9d43c9afdd850ecf4"

    # Kaggle veri setini indirme
    os.system("kaggle datasets download -d snapcrack/all-the-news")
    os.system("unzip all-the-news.zip -d dataset")

    # Veri setini yükleme ve işleme
    df = pd.read_csv("dataset/articles1.csv")
    df = df[["content", "title"]].dropna().sample(500)  # Küçük bir örnek seti için 500 örnek alın
    df["content"] = df["content"].apply(lambda x: x.lower())
    df["title"] = df["title"].apply(lambda x: x.lower())
    return df

# Transformer Modelini Hazırlama
def train_transformer_model(df):
    tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
    model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)

    # Veri setini PyTorch tensörlerine dönüştür
    def tokenize_data(example):
        inputs = tokenizer(example["content"], truncation=True, padding="max_length", max_length=512, return_tensors="pt")
        labels = tokenizer(example["title"], truncation=True, padding="max_length", max_length=128, return_tensors="pt")["input_ids"]
        return inputs["input_ids"].squeeze(), labels.squeeze()

    dataset = [{"content": row["content"], "title": row["title"]} for _, row in df.iterrows()]
    tokenized_data = [tokenize_data(row) for row in dataset]
    dataloader = DataLoader(tokenized_data, batch_size=4, shuffle=True)

    # Eğitim döngüsü
    optimizer = AdamW(model.parameters(), lr=1e-5)
    model.train()
    for epoch in range(2):  # 2 epoch kısa eğitim için yeterli
        total_loss = 0
        for batch in dataloader:
            inputs, labels = batch
            outputs = model(inputs, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss:.4f}")

    return model, tokenizer

# Özet Oluşturma
def generate_summary(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    summary = tokenizer.decode(torch.argmax(outputs.logits, dim=-1)[0], skip_special_tokens=True)
    return summary

# Simhash Benzerlik Hesaplama
def calculate_similarity(text1, text2):
    vector1 = np.array([hash(word) for word in text1.split()])
    vector2 = np.array([hash(word) for word in text2.split()])
    return cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))[0][0]

# Ana Süreç
if __name__ == "__main__":
    print("Veri hazırlanıyor...")
    data = download_and_prepare_dataset()

    print("Model eğitiliyor...")
    model, tokenizer = train_transformer_model(data)

    print("Özet oluşturuluyor...")
    sample_text = data.iloc[0]["content"]
    generated_summary = generate_summary(model, tokenizer, sample_text)
    original_summary = data.iloc[0]["title"]

    print(f"Orijinal Özet: {original_summary}")
    print(f"Oluşturulan Özet: {generated_summary}")

    similarity = calculate_similarity(original_summary, generated_summary)
    print(f"Benzerlik Skoru: {similarity:.2f}")
