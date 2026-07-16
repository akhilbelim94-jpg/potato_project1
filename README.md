# 🌿 Potato Leaf Disease Detection System

> An AI-powered web application that detects potato leaf diseases from leaf images using Deep Learning, helping farmers identify plant diseases early for timely treatment.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=for-the-badge&logo=tensorflow)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

# 📌 Overview

Potato crops are highly vulnerable to diseases such as **Early Blight** and **Late Blight**, which can significantly reduce crop yield if not detected early.

This project uses a **Convolutional Neural Network (CNN)** built with **TensorFlow** to classify potato leaf images into:

- 🟢 Healthy
- 🟤 Early Blight
- ⚫ Late Blight

The application provides a clean web interface where users can upload a leaf image and receive an instant prediction with confidence score and disease information.

---

# ✨ Features

- 🌱 Detects potato leaf diseases using Deep Learning
- 📷 Upload leaf images directly from browser
- ⚡ Real-time disease prediction
- 📊 Confidence score for every prediction
- 💾 Stores scan history in MySQL
- 📁 Saves uploaded images
- 📱 Responsive user interface
- 🔥 FastAPI REST API backend
- 🧠 TensorFlow CNN model integration

---

# 🛠 Tech Stack

## Backend

- FastAPI
- Python
- SQLAlchemy
- MySQL
- Uvicorn

## Machine Learning

- TensorFlow
- Keras
- NumPy
- Pillow

## Frontend

- HTML5
- CSS3
- JavaScript

---

# 📂 Project Structure

```text
potato_project/
│
├── api/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── scan_images/
│
├── model/
│   ├── potato_model.keras
│   └── labels.txt
│
├── frontend/
│   ├── index.html
│   ├── scan.html
│   ├── login.html
│   ├── css/
│   └── js/
│
├── requirements.txt
└── README.md
```

---

# 🧠 Model Information

| Attribute | Details |
|-----------|----------|
| Model | CNN |
| Framework | TensorFlow |
| Classes | Healthy, Early Blight, Late Blight |
| Input Size | 256 × 256 |
| Output | Disease Prediction + Confidence |

---

# 🚀 Workflow

```text
Leaf Image
      │
      ▼
Image Upload
      │
      ▼
Image Preprocessing
      │
      ▼
TensorFlow CNN Model
      │
      ▼
Disease Prediction
      │
      ▼
Confidence Score
      │
      ▼
Store Scan in MySQL
      │
      ▼
Display Result
```

---

# 📸 Screenshots

## Home Page

> Here's is screenshot of Home page
<img width="1208" height="3515" alt="homepage" src="https://github.com/user-attachments/assets/3c591a30-e8c1-4c95-948a-1c062f933caa" />



---

## Here's is screenshot of Scan Page

> <img width="1208" height="3065" alt="scanpage" src="https://github.com/user-attachments/assets/e2ca9018-464c-4c0e-bb36-41529d7da1b9" />


---

## Here's is screenshot of Prediction Result

> <img width="1208" height="3619" alt="result" src="https://github.com/user-attachments/assets/3a5979ca-a8a8-4e59-b4f5-53f7461cb82a" />


---

## Here's is screenshot of Scan History of Leaves

> <img width="1692" height="802" alt="image" src="https://github.com/user-attachments/assets/b6f32e67-e503-4da9-a6e0-74e827610514" />


---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/potato-leaf-disease-detection.git
```

Move into the project

```bash
cd potato-leaf-disease-detection
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn api.main:app --reload
```

Open browser

```
http://127.0.0.1:8000
```

---


# 📊 Extra Featurres 
- Automatically stores every scanned leaf
- Saves prediction results in MySQL
- Stores scan date & time
- View complete scan history
- Search previous scans
- Delete scan history
- Fertilizer Recommendation
- Treatment Recommendation
  

# 📊 Future Improvements

- Mobile Application
- Multi-language Support
- Farmer Dashboard
- Cloud Deployment
- Disease Severity Estimation
- Weather-based Disease Prediction

---

# 💡 Key Learning

This project helped strengthen practical knowledge of:

- Deep Learning
- TensorFlow
- CNN Image Classification
- FastAPI Development
- REST APIs
- SQLAlchemy ORM
- MySQL Database Integration
- Frontend & Backend Integration
- Git & GitHub

---

# 👨‍💻 Author

**AKKi | Akhil Sipahi**

Frontend Developer & Machine Learning Engineer

GitHub: github.com/akhilbelim94-jpg 

LinkedIn: linkedin.com/in/akhil-sipahi-5b0079379 

Email: akhilnelim94@gmail.com

---
---

# 👨‍💻 Author

**Udit Sanghavi**

Database and Backend Developer Developer

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://linkedin.com/in/YOUR_LINKEDIN

Email: YOUR_EMAIL

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
