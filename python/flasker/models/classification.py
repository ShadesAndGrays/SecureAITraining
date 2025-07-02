from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from tqdm.auto import tqdm
import spacy
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import accuracy_score, f1_score, classification_report


class SpacyPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, model='en_core_web_sm'):
        self.model = model
        self.nlp = spacy.load(model)
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return [self._preprocess(text) for text in X]
    
    def _preprocess(self, text):
        doc = self.nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens)

class SpamClassificationHandler:
    # Handle loads the model from a file downloaded from ipfs
    # Check the download folder for the model 
    def __init__(self, model_path=None):
        if model_path and os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            print("Error: Failed to find model")
            self.model = MultinomialNB()
        
        self.preprocessor = SpacyPreprocessor() 
        self.vectorizer = joblib.load('download/tfidf_vectorizer.joblib')
        self.preprocessor_pipeline = Pipeline([
            ('spacy_preprocessor',self.preprocessor),
            ('vectorizer_tfidf',self.vectorizer),
        ])

    def load_dataset(self, dataset_path, size, client_id = 0):
        df = pd.read_csv(dataset_path)
        # Deterministically shuffle using client_id as seed
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        # Split into non-overlapping chunks
        chunk_size = len(df) // size
        start = client_id * chunk_size
        # Last client takes the remainder if not divisible
        if client_id == size - 1:
            end = len(df)
        else:
            end = start + chunk_size
        self.dataset = df[start:end]
        self.classes = np.unique(df['label'])
        self.x = self.dataset['text']
        self.y = self.dataset['label'] 

    def train(self, dataset_path, num_clients=1, client_id=0):
        if dataset_path and os.path.exists(dataset_path):
            self.load_dataset(dataset_path, num_clients, client_id)
        else:
            print("datapath does not exist")
            return
        batch_size = 10
        num_batches = (len(self.x) + batch_size - 1) // batch_size
        for i in tqdm(range(0, len(self.x), batch_size), total=num_batches):
            self.model.partial_fit(
                self.preprocessor_pipeline.transform(self.x[i:i+batch_size]),
                self.y[i:i+batch_size],
                classes=self.classes
            )
        print("Training Complete")

    def evaluate(self, test_fraction=0.2):
        # Use a held-out section of the dataset for testing
        test_size = max(1, int(len(self.dataset) * test_fraction))
        test_df = self.dataset.tail(test_size)
        X_test = test_df['text']
        y_test = test_df['label']
        y_pred = self.model.predict(self.preprocessor_pipeline.transform(X_test))
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='binary')
        report = classification_report(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print(f"F1-score: {f1:.4f}")
        print(report)
        return {'accuracy': acc, 'f1': f1, 'report': report}

    def extract_updates(self):
        # Return model state dict (weights)
        return self.model.state_dict()

    def save_model(self, save_path):
        joblib.dump(self.model, save_path)

# Example usage:
# handler = ClassificationHandler(model_path='downloaded_model.pt', input_dim=10, num_classes=2)
# handler.train('datasets/dataset1', epochs=5)
# handler.save_updates('updates/update_1.pt')

def main():
    dataset_path = "../data/classification_dataset/combined_data.csv"
    num_clients = 4  # Set the number of clients/sections here
    unique_id = 0    # Set the client id (0 to num_clients-1)
    model = SpamClassificationHandler()
    model.train(dataset_path, num_clients=num_clients, client_id=0)
    model.evaluate()
  
  #ExtractWeights
  #SaveOrSendWeights

if __name__ == "__main__":
    main()