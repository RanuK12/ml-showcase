"""
Iris Species Predictor using Logistic Regression
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def train_model():
    """Load Iris dataset and train a logistic regression model."""
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = LogisticRegression(max_iter=200, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    
    return model, iris


def predict_species(model, sepal_length, sepal_width, petal_length, petal_width):
    """
    Predict iris species from measurements.
    
    Args:
        model: Trained logistic regression model
        sepal_length: Sepal length in cm
        sepal_width: Sepal width in cm
        petal_length: Petal length in cm
        petal_width: Petal width in cm
    
    Returns:
        Predicted species name
    """
    iris = load_iris()
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(features)
    return iris.target_names[prediction[0]]


if __name__ == "__main__":
    print("Training Iris classifier...")
    model, iris = train_model()
    
    print("\n" + "="*50)
    print("Example Predictions:")
    print("="*50)
    
    examples = [
        (5.1, 3.5, 1.4, 0.2, "setosa"),
        (6.2, 2.9, 4.3, 1.3, "versicolor"),
        (7.7, 3.0, 6.1, 2.3, "virginica"),
    ]
    
    for sl, sw, pl, pw, expected in examples:
        result = predict_species(model, sl, sw, pl, pw)
        print(f"  [{sl}, {sw}, {pl}, {pw}] -> {result} (expected: {expected})")
