import pandas as pd
from utils.preprocess import clean_text
import joblib

model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def classify_whatsapp(file):
    raw = file.read().decode("utf-8")
    lines = raw.split("\n")
    messages = [line for line in lines if line and "]" in line]
    df = pd.DataFrame(messages, columns=['text'])
    df['clean'] = df['text'].apply(clean_text)
    df['label'] = model.predict(vectorizer.transform(df['clean']))
    return df[['text', 'label']]
