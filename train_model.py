import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
from utils.preprocess import clean_text

print("Loading dataset...")
df = pd.read_csv("datasets/spam.csv", encoding='latin-1')[['v1', 'v2']]
df.columns = ['label', 'text']
df.drop_duplicates(subset='text', inplace=True)
df['text'] = df['text'].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2)

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vec, y_train)

joblib.dump(model, "models/spam_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Training completed.")
print(classification_report(y_test, model.predict(X_test_vec)))
