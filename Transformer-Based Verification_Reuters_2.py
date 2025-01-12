import os
import tarfile
import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Reuters Veri Setini İndirme ve İşleme
def download_and_prepare_reuters_dataset():
    # Veri setini indirme URL'si
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/reuters21578-mld/reuters21578.tar.gz"
    tar_path = "reuters21578.tar.gz"
    extract_path = "reuters_dataset"

    # Eğer veri seti daha önce indirilmediyse indir
    if not os.path.exists(tar_path):
        print("Veri seti indiriliyor...")
        response = requests.get(url, stream=True)
        with open(tar_path, "wb") as file:
            file.write(response.content)

    # Eğer veri seti çıkarılmadıysa arşivi aç
    if not os.path.exists(extract_path):
        print("Veri seti çıkarılıyor...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=extract_path)

    # SGML dosyalarını işleme
    print("Veri seti işleniyor...")
    articles = []
    sgml_files = [f for f in os.listdir(extract_path) if f.endswith(".sgm")]
    for file_name in sgml_files:
        with open(os.path.join(extract_path, file_name), "r", encoding="latin-1") as file:
            content = file.read()
            soup = BeautifulSoup(content, "html.parser")
            for article in soup.find_all("reuters"):
                title = article.find("title")
                body = article.find("body")
                if title and body:
                    articles.append({"title": title.text, "content": body.text})

    # Pandas DataFrame oluştur
    df = pd.DataFrame(articles)
    print(f"Toplam {len(df)} makale işlendi.")
    return df

# Özetleme Fonksiyonu
def generate_summary(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="longest", max_length=1024)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Ana Süreç
if __name__ == "__main__":
    # Veri setini indir ve hazırla
    print("Reuters veri seti indiriliyor ve işleniyor...")
    reuters_data = download_and_prepare_reuters_dataset()

    # Örnek bir veri ile çalışma
    print("Model yükleniyor...")
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

    # İlk makaleden bir örnek özet oluşturma
    print("Özet oluşturuluyor...")
    sample_text = reuters_data.iloc[0]["content"]
    original_title = reuters_data.iloc[0]["title"]
    generated_summary = generate_summary(model, tokenizer, sample_text)

    print("\n--- Özetleme Sonuçları ---")
    print(f"Orijinal Başlık: {original_title}")
    print(f"Oluşturulan Özet: {generated_summary}")
