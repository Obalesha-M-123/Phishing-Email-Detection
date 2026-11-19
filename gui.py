 
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import re
from urllib.parse import urlparse
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- MODEL TRAINING ----------------

data = pd.read_csv("emails.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["email_text"])

model = MultinomialNB()
model.fit(X, data["label"])

suspicious_keywords = [
    "password", "verify", "urgent", "free prize",
    "claim reward", "bank account", "click here",
    "login", "winner", "account blocked"
]

history = []

# ---------------- MAIN FUNCTIONS ----------------

def scan_email():
    email = email_input.get("1.0", tk.END).strip()

    if not email:
        messagebox.showwarning("Warning", "Please enter an email!")
        return

    prediction = model.predict(vectorizer.transform([email]))[0]

    found_keywords = [
        word for word in suspicious_keywords
        if word in email.lower()
    ]

    urls = re.findall(r'https?://\S+|www\.\S+', email)
    suspicious_url = False

    for url in urls:
        if url.startswith("www."):
            url = "http://" + url

        domain = urlparse(url).hostname or ""

        if any(x in domain.lower() for x in [
            "bit.ly", "tinyurl.com", "t.co",
            "is.gd", "verify", "login", "secure", "account"
        ]):
            suspicious_url = True

    is_phishing = prediction == "Phishing" or suspicious_url

    # Heuristic risk score, not a calibrated probability
    risk_score = 20

    if prediction == "Phishing":
        risk_score += 40

    risk_score += min(len(found_keywords) * 8, 32)

    if suspicious_url:
        risk_score += 30

    risk_score = min(risk_score, 100)

    result = "Phishing" if is_phishing else "Safe"

    if is_phishing:
        result_label.config(
            text="⚠ POTENTIAL PHISHING EMAIL",
            fg="red"
        )
    else:
        result_label.config(
            text="✓ LIKELY SAFE EMAIL",
            fg="green"
        )

    risk_label.config(
        text=f"Risk Level: {risk_score}%",
        fg="red" if risk_score >= 70 else
           "orange" if risk_score >= 40 else "green"
    )

    risk_bar["value"] = risk_score

    keyword_label.config(
        text="Suspicious Keywords: " +
        (", ".join(found_keywords) if found_keywords else "None")
    )

    url_label.config(
        text=f"URLs Found: {len(urls)}" +
        (" | Suspicious URL detected!" if suspicious_url else "")
    )

    scan_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    history.append({
        "Date & Time": scan_time,
        "Email": email,
        "Result": result,
        "Risk Score": risk_score,
        "Keywords": ", ".join(found_keywords),
        "URLs Found": len(urls)
    })

    update_dashboard()


# ---------------- DASHBOARD ----------------

def update_dashboard():
    total = len(history)
    phishing = sum(1 for item in history if item["Result"] == "Phishing")
    safe = sum(1 for item in history if item["Result"] == "Safe")

    total_label.config(text=f"Total Scanned: {total}")
    phishing_label.config(text=f"Phishing: {phishing}")
    safe_label.config(text=f"Safe: {safe}")

    history_list.delete(0, tk.END)

    for item in reversed(history):
        history_list.insert(
            tk.END,
            f'{item["Date & Time"]} | {item["Result"]} | '
            f'{item["Risk Score"]}% | {item["Email"][:35]}'
        )

    update_chart(phishing, safe)


# ---------------- PIE CHART ----------------

def update_chart(phishing, safe):
    chart_ax.clear()

    if phishing + safe == 0:
        chart_ax.text(
            0.5, 0.5, "No scan data yet",
            ha="center", va="center"
        )
        chart_ax.axis("off")
    else:
        chart_ax.pie(
            [phishing, safe],
            labels=["Phishing", "Safe"],
            autopct="%1.1f%%",
            startangle=90
        )
        chart_ax.axis("equal")

    chart_canvas.draw()


# ---------------- CLEAR FUNCTIONS ----------------

def clear_email():
    email_input.delete("1.0", tk.END)
    result_label.config(text="Waiting for scan...", fg="blue")
    risk_label.config(text="Risk Level: 0%", fg="blue")
    risk_bar["value"] = 0
    keyword_label.config(text="Suspicious Keywords: None")
    url_label.config(text="URLs Found: 0")


def clear_history():
    if messagebox.askyesno("Confirm", "Clear all scan history?"):
        history.clear()
        clear_email()
        update_dashboard()


# ---------------- EXPORT CSV ----------------

def export_report():
    if not history:
        messagebox.showwarning("Warning", "No scan history to export!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        initialfile="phishing_scan_report.csv"
    )

    if file_path:
        pd.DataFrame(history).to_csv(file_path, index=False)
        messagebox.showinfo(
            "Success",
            "Scan report exported successfully!"
        )


# ---------------- GUI DESIGN ----------------

root = tk.Tk()
root.title("Phishing Email Detector - Ultra PRO")
root.geometry("1000x900")
root.configure(bg="#eef2f7")

title = tk.Label(
    root,
    text="PHISHING EMAIL DETECTOR",
    font=("Arial", 24, "bold"),
    bg="#eef2f7",
    fg="#123456"
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="AI Powered Email Security System",
    font=("Arial", 12),
    bg="#eef2f7",
    fg="#555555"
)
subtitle.pack()

# Dashboard

dashboard = tk.Frame(root, bg="#dce8f5", padx=15, pady=15)
dashboard.pack(fill="x", padx=25, pady=15)

tk.Label(
    dashboard,
    text="DASHBOARD",
    font=("Arial", 15, "bold"),
    bg="#dce8f5"
).pack()

stats = tk.Frame(dashboard, bg="#dce8f5")
stats.pack(pady=10)

total_label = tk.Label(
    stats, text="Total Scanned: 0",
    font=("Arial", 12, "bold"), bg="#dce8f5"
)
total_label.pack(side=tk.LEFT, padx=25)

phishing_label = tk.Label(
    stats, text="Phishing: 0",
    font=("Arial", 12, "bold"),
    fg="red", bg="#dce8f5"
)
phishing_label.pack(side=tk.LEFT, padx=25)

safe_label = tk.Label(
    stats, text="Safe: 0",
    font=("Arial", 12, "bold"),
    fg="green", bg="#dce8f5"
)
safe_label.pack(side=tk.LEFT, padx=25)

# Email Input

tk.Label(
    root,
    text="Enter Email Message:",
    font=("Arial", 13, "bold"),
    bg="#eef2f7"
).pack(pady=8)

email_input = tk.Text(
    root,
    height=6,
    width=100,
    font=("Arial", 11),
    wrap=tk.WORD
)
email_input.pack(padx=25)

# Buttons

button_frame = tk.Frame(root, bg="#eef2f7")
button_frame.pack(pady=12)

tk.Button(
    button_frame,
    text="SCAN EMAIL",
    command=scan_email,
    bg="#1769aa",
    fg="white",
    font=("Arial", 11, "bold"),
    width=16
).pack(side=tk.LEFT, padx=8)

tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_email,
    bg="#555555",
    fg="white",
    width=12
).pack(side=tk.LEFT, padx=8)

# Results

result_label = tk.Label(
    root,
    text="Waiting for scan...",
    font=("Arial", 17, "bold"),
    bg="#eef2f7",
    fg="blue"
)
result_label.pack(pady=8)

risk_label = tk.Label(
    root,
    text="Risk Level: 0%",
    font=("Arial", 14, "bold"),
    bg="#eef2f7"
)
risk_label.pack(pady=5)

risk_bar = ttk.Progressbar(
    root,
    length=450,
    maximum=100,
    mode="determinate"
)
risk_bar.pack(pady=5)

keyword_label = tk.Label(
    root,
    text="Suspicious Keywords: None",
    bg="#eef2f7",
    wraplength=850
)
keyword_label.pack(pady=5)

url_label = tk.Label(
    root,
    text="URLs Found: 0",
    bg="#eef2f7"
)
url_label.pack(pady=5)

# Pie Chart

chart_frame = tk.Frame(root, bg="#eef2f7")
chart_frame.pack(pady=5)

chart_figure = Figure(figsize=(4, 2.5), dpi=90)
chart_ax = chart_figure.add_subplot(111)

chart_canvas = FigureCanvasTkAgg(
    chart_figure,
    master=chart_frame
)
chart_canvas.get_tk_widget().pack()

update_chart(0, 0)

# Scan History

tk.Label(
    root,
    text="SCAN HISTORY",
    font=("Arial", 14, "bold"),
    bg="#eef2f7"
).pack(pady=8)

history_list = tk.Listbox(
    root,
    width=120,
    height=7,
    font=("Arial", 9)
)
history_list.pack(padx=20)

# Bottom Buttons

bottom_frame = tk.Frame(root, bg="#eef2f7")
bottom_frame.pack(pady=12)

tk.Button(
    bottom_frame,
    text="EXPORT CSV REPORT",
    command=export_report,
    bg="#176b45",
    fg="white",
    font=("Arial", 10, "bold")
).pack(side=tk.LEFT, padx=10)

tk.Button(
    bottom_frame,
    text="CLEAR HISTORY",
    command=clear_history,
    bg="#b83232",
    fg="white",
    font=("Arial", 10, "bold")
).pack(side=tk.LEFT, padx=10)

root.mainloop()
