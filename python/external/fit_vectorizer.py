from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import joblib

df = pd.read_csv('python/data/classification_dataset/preprocessed_train.csv')
print(df.head())

tfidf  = TfidfVectorizer()
tfidf.fit(df['text'])

joblib.dump(tfidf,'fitted_tfidf_vectorizer.joblib')