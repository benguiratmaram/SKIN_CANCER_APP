# 🩺 Skin Cancer Detection App

A Flask web application that uses a fine-tuned VGG16 deep learning model to classify skin lesion images as **Malignant** or **Benign**. Built with Python, TensorFlow, and MySQL.

---

## 🎬 Demo

> Click below to watch the app in action:

**[▶ Watch demo video](https://github.com/benguiratmaram/SKIN_CANCER_APP/blob/main/skin%20cancer.mp4)**

---

## ✨ Features

- User authentication (login / logout)
- Upload a skin lesion image and get an instant AI prediction
- Displays result (Malignant / Benign) with confidence percentage
- Saves all patient records (name, age, result, image) to a MySQL database
- Patient history dashboard

---

## 🗂 Project Structure

```
SKIN_CANCER_APP/
├── app.py              # Flask backend — routes, model inference, DB logic
├── fix.py              # Utility / fix script
├── database.sql        # MySQL schema
├── static/             # CSS, uploaded images
├── templates/          # HTML templates (login, dashboard, predict, result, patients)
└── model/
    └── vgg16_fixed.h5  # Pre-trained VGG16 model (not tracked in git)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/benguiratmaram/SKIN_CANCER_APP.git
cd SKIN_CANCER_APP
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install flask tensorflow mysql-connector-python numpy
```

### 4. Set up the database

Import the schema into MySQL:

```bash
mysql -u root -p < database.sql
```

Make sure your MySQL credentials in `app.py` match your local setup:

```python
host="localhost", user="root", password="", database="skin_cancer_db"
```

### 5. Add the model

Place your trained model file at:

```
model/vgg16_fixed.h5
```

### 6. Run the app

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧠 Model

The app uses a **VGG16** convolutional neural network fine-tuned for binary skin lesion classification:

- Input: 224×224 RGB image
- Output: probability score → `> 0.5` = Malignant, `≤ 0.5` = Benign

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| AI Model | TensorFlow / Keras, VGG16 |
| Database | MySQL |
| Frontend | HTML, CSS (Jinja2 templates) |

---

## 👩‍💻 Author

**Maram Benguirat** — [github.com/benguiratmaram](https://github.com/benguiratmaram)
