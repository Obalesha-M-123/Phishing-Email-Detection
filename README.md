 # 🔐 Phishing Email Detection System

An AI-powered Phishing Email Detection System built using Python and Machine Learning.

## 📌 About the Project

This project analyzes email messages and identifies potentially phishing emails using Machine Learning and suspicious pattern detection.

It provides a simple graphical user interface (GUI) to scan emails and display risk information.

## ✨ Features

- Email scanning through GUI
- Phishing and Safe email classification
- Suspicious keyword detection
- Suspicious URL detection
- Risk level indicator
- Total scanned email dashboard
- Phishing vs Safe statistics
- Clear and user-friendly interface

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Tkinter
- Machine Learning (TF-IDF and Naive Bayes)

## 📂 Project Structure

```text
Phishing-Email-Detection/
│
├── emails.csv
├── train_model.py
├── predict_email.py
├── evaluate_model.py
├── phishing_detector.py
├── main.py
├── gui.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/Obalesha-M-123/Phishing-Email-Detection.git
```

2. Open the project folder:

```bash
cd Phishing-Email-Detection
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
python gui.py
```

## 🧪 Model Evaluation

The project includes a model evaluation script:

```bash
python evaluate_model.py
```

The current sample dataset is small, so evaluation results are preliminary and should not be treated as real-world accuracy.

## 🚀 Future Improvements

- Use a larger real-world email dataset
- Improve model performance
- Add email file upload support
- Add detailed scan history
- Deploy as a web application

## 👨‍💻 Developer

**Obalesha M**

GitHub: [Obalesha-M-123](https://github.com/Obalesha-M-123)

## ⚠️ Disclaimer

This project is an educational prototype. Its predictions are not a guarantee that an email is safe or malicious.
