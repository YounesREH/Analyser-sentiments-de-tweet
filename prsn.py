import joblib
import re
import sys


def clean_tweet(text: str) -> str:
    text = re.sub(r"http\S+", "", str(text))
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


VEC_PATH   = "models/tfidf_vectorizer.joblib"
MODEL_PATH = "models/sentiment_model.joblib"

vectorizer = joblib.load(VEC_PATH)
model = joblib.load(MODEL_PATH)


text = sys.argv[1]
clean_text = clean_tweet(text)
X = vectorizer.transform([clean_text])


proba = model.predict_proba(X)[0]
pred  = model.predict(X)[0]
conf  = max(proba)


label_fr = "Positif" if pred.lower().startswith("pos") else "Negatif"
print(f"Resultat : {label_fr} (Classe brute : {pred}, Confiance : {conf*100:.1f}%)")
