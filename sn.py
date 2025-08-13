import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path

TRAIN_PATH = "twitter_training.csv"      
VAL_PATH   = "twitter_validation.csv"
VEC_PATH   = "models/tfidf_vectorizer.joblib"
MODEL_PATH = "models/sentiment_model.joblib"
MAX_FEATURES = 20000  


def clean_tweet(text: str) -> str:
    text = re.sub(r"http\S+", "", str(text))   
    text = re.sub(r"@\w+", "", text)           
    text = re.sub(r"#", "", text)              
    text = re.sub(r"[^\w\s]", " ", text)       
    text = re.sub(r"\s+", " ", text).strip()   
    return text


col_names = ["ID", "Entity", "Sentiment", "Text"]
train_df = pd.read_csv(TRAIN_PATH, header=None, names=col_names)
val_df   = pd.read_csv(VAL_PATH, header=None, names=col_names)


keep = {"Positive", "Negative"}
train_df = train_df[train_df["Sentiment"].isin(keep)].copy()
val_df   = val_df[val_df["Sentiment"].isin(keep)].copy()


train_df["clean_text"] = train_df["Text"].apply(clean_tweet)
val_df["clean_text"]   = val_df["Text"].apply(clean_tweet)


vectorizer = TfidfVectorizer(max_features=MAX_FEATURES)
X_train = vectorizer.fit_transform(train_df["clean_text"]) 
X_val   = vectorizer.transform(val_df["clean_text"]) 

y_train = train_df["Sentiment"]
y_val   = val_df["Sentiment"]


model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)


y_pred = model.predict(X_val)
print("accuracy: ", accuracy_score(y_val, y_pred))
print(classification_report(y_val, y_pred))


Path("models").mkdir(parents=True, exist_ok=True)
joblib.dump(vectorizer, VEC_PATH)
joblib.dump(model, MODEL_PATH)


