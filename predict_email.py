 
import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load Dataset
data = pd.read_csv("emails.csv")

X = data["email_text"]
y = data["label"]

# Train Machine Learning Model
vectorizer = TfidfVectorizer()
X_features = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_features, y)

# Suspicious keywords
suspicious_keywords = [
    "password",
    "verify",
    "urgent",
    "free prize",
    "claim reward",
    "bank account",
    "click here",
    "login",
    "winner",
    "account blocked"
]

# URL Detection Function
def detect_urls(email):

    urls = re.findall(r'https?://\S+|www\.\S+', email)

    suspicious_urls = []

    short_domains = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd"
    ]

    for url in urls:

        clean_url = url.rstrip(".,!?;)")
        parsed = urlparse(
            clean_url if clean_url.startswith("http")
            else "http://" + clean_url
        )

        domain = parsed.netloc.lower()

        if any(short in domain for short in short_domains):
            suspicious_urls.append(clean_url)

        elif re.fullmatch(r'\d{1,3}(?:\.\d{1,3}){3}', domain):
            suspicious_urls.append(clean_url)

        elif any(word in domain for word in [
            "verify", "login", "secure", "account"
        ]):
            suspicious_urls.append(clean_url)

    return urls, suspicious_urls


# Email Analysis
print("================================")
print("   PHISHING EMAIL DETECTOR PRO")
print("================================")

email = input("\nEnter Email Text: ")

# Machine Learning Prediction
email_features = vectorizer.transform([email])
prediction = model.predict(email_features)[0]

# Keyword Detection
found_keywords = [
    word for word in suspicious_keywords
    if word in email.lower()
]

# URL Detection
urls, suspicious_urls = detect_urls(email)

# Display Results
print("\n--- ANALYSIS REPORT ---")

print("\nML Prediction:", prediction)

print("\nSuspicious Keywords:")
if found_keywords:
    print(found_keywords)
else:
    print("No suspicious keywords found.")

print("\nURLs Found:")
if urls:
    for url in urls:
        print(url)
else:
    print("No URLs found.")

print("\nSuspicious URLs:")
if suspicious_urls:
    for url in suspicious_urls:
        print(url)
else:
    print("No suspicious URLs detected.")

# Final Result
print("\n--- FINAL RESULT ---")

if prediction == "Phishing" or suspicious_urls:
    print("WARNING! Potential Phishing Email.")
elif found_keywords:
    print("CAUTION! Suspicious Email. Verify before clicking.")
else:
    print("Email classified as SAFE by the model.")

print("\n================================")
