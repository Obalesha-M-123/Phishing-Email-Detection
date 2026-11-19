import csv

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load Dataset
with open("emails.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

X = [row["email_text"] for row in data]
y = [row["label"] for row in data]

# Convert text into numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Test Model
predictions = model.predict(X_test)

print("===================================")
print(" PHISHING EMAIL DETECTION MODEL")
print("===================================")

print("\nModel Training Completed!")
print("Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# Test New Email
email = input("\nEnter an email message: ")

email_vector = vectorizer.transform([email])
result = model.predict(email_vector)[0]

print("\nEmail Classification:", result)