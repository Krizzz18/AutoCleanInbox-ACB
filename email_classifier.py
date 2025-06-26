import joblib

model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def classify_emails(messages):
    X = vectorizer.transform(messages)
    return model.predict(X)
