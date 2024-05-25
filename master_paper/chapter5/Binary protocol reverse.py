from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_recall_curve


class ProtocolDataProcessor:
    def __init__(self, filepath):

        self.filepath = filepath
        self.data = None
        self.processed = False

        print(f"ProtocolDataProcessor initialized with file: {self.filepath}")

    def load_data(self):

        try:

            self.data = pd.read_csv(self.filepath)
            print(f"Data loaded successfully from {self.filepath}")

            self.data.dropna(axis=1, how='all', inplace=True)

            if 'temp_column' in self.data.columns:
                self.data.drop('temp_column', axis=1, inplace=True)

            for col in self.data.select_dtypes(include='number').columns:
                if self.data[col].isnull().any():
                    self.data[col].fillna(self.data[col].median(), inplace=True)

            for col in self.data.select_dtypes(include='object').columns:
                self.data[col].fillna('Unknown', inplace=True)

            if 'date_column' in self.data.columns:
                self.data['date_column'] = pd.to_datetime(self.data['date_column'], errors='coerce')

            self.processed = True
            print("Data processing completed successfully.")

        except Exception as e:
            print(f"An error occurred while loading the data: {e}")


class FeatureExtractor:
    def __init__(self, data):

        self.data = data
        self.features = None
        self.target = None

        print("FeatureExtractor initialized and ready to process data.")

    def extract(self):

        if 'target' in self.data.columns:
            self.target = self.data['target']
            self.features = self.data.drop('target', axis=1)
        else:
            print("Warning: 'target' column not found in the data.")
            self.features = self.data

        numeric_cols = self.features.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = self.features.select_dtypes(include=['object', 'category']).columns

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ])

        self.features = preprocessor.fit_transform(self.features)

        self.feature_pipeline = preprocessor


class ModelBuilder:
    def __init__(self, features, target):
        self.features = features
        self.target = target
        self.model = RandomForestClassifier(random_state=42)

        print("ModelBuilder initialized with features and target data. Model is ready to be trained.")

    def split_data(self, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.target, test_size=test_size, random_state=random_state
        )

        print(f"Data split into train and test sets with test size = {test_size}.")
        return X_train, X_test, y_train, y_test

    def build_pipeline(self):
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.features.select_dtypes(include=['int64', 'float64']).columns),
                ('cat', categorical_transformer, self.features.select_dtypes(include=['object']).columns)
            ])

        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', self.model)
        ])

        return pipeline

    def train_model(self, pipeline, X_train, y_train):
        param_grid = {
            'classifier__n_estimators': [100, 200, 300],
            'classifier__max_depth': [None, 10, 20, 30],
            'classifier__min_samples_split': [2, 5, 10],
            'classifier__min_samples_leaf': [1, 2, 4]
        }

        grid_search = GridSearchCV(pipeline, param_grid, cv=5, verbose=3)
        grid_search.fit(X_train, y_train)
        self.model = grid_search.best_estimator_
        print(f"Model training completed with best parameters: {grid_search.best_params_}")

    def evaluate_model(self, X_test, y_test):
        if self.pipeline is None:
            raise ValueError("Model has not been trained yet.")

        probabilities = self.pipeline.predict_proba(X_test)[:, 1]
        precision, recall, thresholds = precision_recall_curve(y_test, probabilities)
        threshold_optimal = thresholds[np.argmax(precision[recall > 0.85])]

        predictions = (probabilities >= threshold_optimal).astype(int)
        accuracy = accuracy_score(y_test, predictions)
        cls_report = classification_report(y_test, predictions)
        conf_matrix = confusion_matrix(y_test, predictions)

        print("Optimal Threshold:", threshold_optimal)
        print("Model Evaluation Results with Adjusted Threshold:")
        print("Accuracy:", accuracy)
        print("Classification Report:")
        print(cls_report)
        print("Confusion Matrix:")
        print(conf_matrix)


def main():
    data = pd.read_csv('C:\\Users\\MLTZ\\Desktop\\Simulated_Data.csv')

    features = data.drop('target', axis=1)
    target = data['target']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model_builder = ModelBuilder(features, target)
    pipeline = model_builder.build_pipeline()
    model_builder.train_model(pipeline, X_train, y_train)

    joblib.dump(model_builder.model, 'trained_model.pkl')
    print("Trained model saved to 'trained_model.pkl'.")


if __name__ == "__main__":
    main()
