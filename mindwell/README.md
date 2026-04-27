# 🧠 Mindwell

> A mental health and wellness web application for college students.

Mindwell helps students track their mental health through standardized assessments (PHQ-9 & GAD-7), access wellness resources, and connect with counsellors.

---

## ✨ Features

- 🔐 **Authentication** — Email/password login & registration
- 📋 **Mental Health Assessments** — PHQ-9 (depression) & GAD-7 (anxiety) screening
- 📊 **Dashboard** — Track your wellness scores over time
- 📚 **Resources** — Curated mental health resources
- 👩‍⚕️ **Counsellors** — Find and connect with counsellors

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Auth:** Flask sessions + Google OAuth

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mindwell.git
cd mindwell

# Install dependencies
pip install flask

# Run the app
python app.py
```

Then open your browser and go to: `http://localhost:5000`

---

## 📁 Project Structure

```
mindwell/
├── app.py                  # Flask backend & routes
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   └── ...
├── static/                 # CSS, JS, images
├── static_web_prototype/   # Standalone SPA prototype
└── README.md
```

---

## 📄 License

This project is for educational purposes.
