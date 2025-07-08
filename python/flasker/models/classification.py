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
from .model import BaseModel


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

class SpamClassificationHandler(BaseModel):
    # Handle loads the model from a file downloaded from ipfs
    # Check the download folder for the model 
    def __init__(self, model_path=None,initial=False):
        self.model = MultinomialNB()
        if model_path and os.path.exists(model_path):
            self.set_parameters_from_file(model_path)
        
        self.preprocessor = SpacyPreprocessor() 
        self.vectorizer = joblib.load('download/tfidf_vectorizer.joblib')
        self.preprocessor_pipeline = Pipeline([
            ('spacy_preprocessor',self.preprocessor),
            ('vectorizer_tfidf',self.vectorizer),
        ])
        # Fit the model to have parameters to send if initial model
        if initial:
            self.train_model(chunk_parts=1000,train_size=0.1)
            pass

    def set_parameters_from_file(self,model_parameters_path):
        parameters = joblib.load(model_parameters_path)

        if not isinstance(parameters, dict) or "class_count_" not in parameters or "feature_count_" not in parameters:
             raise ValueError("Loaded parameters are not in the expected dictionary format.")
        self.set_parameters(parameters)

    def set_parameters(self,parameters):
        class_log_prior, feature_log_prob = self.compute_mnb_params(parameters['class_count_'], parameters['feature_count_'], alpha=1.0)
        self.model.class_count_ = parameters['class_count_']
        self.model.feature_count_ = parameters['feature_count_']
        self.model.class_log_prior_ = class_log_prior
        self.model.feature_log_prob_ = feature_log_prob
        self.model.classes_ = np.array([0,1])
        

    def extract_parameters(self):
        return {
            "class_count_": self.model.class_count_,
            "feature_count_": self.model.feature_count_,
        }

    def save_parameters(self,save_path):
        parameters = {
            "class_count_": self.model.class_count_,
            "feature_count_": self.model.feature_count_,
        }
        joblib.dump(parameters,save_path)
        return save_path

    def aggregate_mnb_models(self,client_stats):
        total_class_count = None
        total_feature_count = None

        for i in client_stats:
            class_count = i['class_count_']
            feature_count = i['feature_count_']
            if total_class_count is None:
                total_class_count = class_count.copy()
                total_feature_count = feature_count.copy()
            else:
                total_class_count += class_count
                total_feature_count += feature_count

        return total_class_count, total_feature_count

    def compute_mnb_params(self,total_class_counts, total_feature_counts, alpha=1.0):
        import numpy as np

        class_log_prior = np.log(total_class_counts / total_class_counts.sum())

        # Apply Laplace smoothing
        smoothed_fc = total_feature_counts + alpha
        smoothed_fc_sum = smoothed_fc.sum(axis=1, keepdims=True)
        feature_log_prob = np.log(smoothed_fc / smoothed_fc_sum)

        return class_log_prior, feature_log_prob

    def build_global_model(self,total_class_count, total_feature_count, alpha=1.0):
        model = MultinomialNB(alpha=alpha, fit_prior=True)

        # Manually set the fitted attributes
        model.class_count_ = total_class_count
        model.feature_count_ = total_feature_count
        model.class_log_prior_,model.feature_log_prob_ = self.compute_mnb_params(total_class_count, total_feature_count, alpha=1.0)

        model.classes_ = np.arange(len(total_class_count))  # Assuming 0-based class labels

        return model


    def _load_dataset(self,dataset_path="data/classification_dataset/spam_data.csv", chunk_parts=1, client_id = 0):
        df = pd.read_csv(dataset_path)
        # Deterministically shuffle using client_id as seed
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        # Split into non-overlapping chunks
        chunk_size = len(df) // chunk_parts
        start = client_id * chunk_size
        # Last client takes the remainder if not divisible
        if client_id == chunk_parts - 1:
            end = len(df)
        else:
            end = start + chunk_size
        self.dataset = df[start:end]
        self.classes = np.unique(df['label'])
        self.x = self.dataset['text']
        self.y = self.dataset['label'] 

    def train_model(self, dataset_path="data/classification_dataset/spam_data.csv", chunk_parts=1, client_id=0,train_size=0.8):
        if dataset_path and os.path.exists(dataset_path):
            self._load_dataset(dataset_path, chunk_parts, client_id)
        else:
            print("datapath does not exist")
            return
            
        self.train_x = self.x.head(int(len(self.x)*train_size))
        self.train_y = self.y.head(int(len(self.y)*train_size)) 
        batch_size = 10
        num_batches = (len(self.train_x) + batch_size - 1) // batch_size
        for i in tqdm(range(0, len(self.train_x), batch_size), total=num_batches):
            self.model.partial_fit(
                self.preprocessor_pipeline.transform(self.train_x[i:i+batch_size]),
                self.train_y[i:i+batch_size],
                self.classes
            )
        print("Training Complete")

    def evaluate_model(self, test_fraction=0.2):
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

    def save_model(self, save_path):
        joblib.dump(self.model, save_path)
        return save_path

    def load_model(self, model_path):
        self.model = joblib.load(model_path)


# Example usage:
# handler = ClassificationHandler(model_path='downloaded_model.pt', input_dim=10, num_classes=2)
# handler.train('datasets/dataset1', epochs=5)
# handler.save_updates('updates/update_1.pt')

def main():
    dataset_path = "data/classification_dataset/spam_data.csv"
    num_clients = 4  # Set the number of clients/sections here
    model = SpamClassificationHandler()
    model2 = SpamClassificationHandler()
    model3 = SpamClassificationHandler()
    model.train_model(chunk_parts=100,client_id=80)
    model.evaluate_model()
    model2.train_model(chunk_parts=100,client_id=12)
    model2.evaluate_model()
    model3.train_model(chunk_parts=100,client_id=58)
    model3.evaluate_model()
    extract1 = model.extract_parameters()
    extract2 = model2.extract_parameters()
    global_model = SpamClassificationHandler()
    global_model._load_dataset(dataset_path,100)

    cc, fc  = global_model.aggregate_mnb_models([extract1,extract2])
    global_model.set_parameters({'class_count_':cc,'feature_count_':fc})
    global_model.evaluate_model(test_fraction=1)

if __name__ == "__main__":
    main()

def simulate(numOfClients,model_parameters_path,dataset_path,current_round):
    models:list[SpamClassificationHandler] = []
    for _ in range(numOfClients):
        m = SpamClassificationHandler()
        m.set_parameters_from_file(model_parameters_path)
        models.append(m)
    # training 
    for client_id in range(numOfClients):
        models[client_id].train_model(chunk_parts=10000*numOfClients,client_id=client_id)
    # evaluation
    for client_id in range(numOfClients):
        print(current_round,": ", models[client_id].evaluate_model())

    # saving
    saves = []
    for client_id in range(numOfClients):
        saves.append(models[client_id].save_parameters(f'download/temp/{client_id}_spam_classifier_{current_round}.joblib'))
    return saves

