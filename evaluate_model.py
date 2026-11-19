
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)

# Load Dataset
data = pd.read_csv("emails.csv")

X = data["email_text"]
y = data["label"]

# Convert text into numerical features
vectorizer = TfidfVectorizer()
X_features = vectorizer.fit_transform(X)

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_features,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("MODEL EVALUATION")
print("-----------------------")
print("Accuracy:", accuracy * 100, "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["Phishing", "Safe"]
)

print("\nConfusion Matrix:")
print(cm)

# Display Graph
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Phishing", "Safe"]
)

display.plot(cmap="Blues", values_format="d")
plt.title("Phishing Email Detection - Confusion Matrix")
plt.tight_layout()
plt.show()
