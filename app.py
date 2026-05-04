from flask import Flask, render_template, request, redirect, session, flash
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret"

# =========================
# UPLOAD
# =========================
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =========================
# LOAD MODEL
# =========================
model = load_model("model/vgg16_fixed.h5")

# =========================
# DB
# =========================
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skin_cancer_db"
    )

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True, buffered=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            session["user"] = username
            flash("Login réussi ✓", "success")
            return redirect("/dashboard")
        else:
            flash("Erreur login ✗", "danger")

    return render_template("login.html")

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

# =========================
# PREDICT
# =========================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        try:
            name = request.form["name"]
            age = request.form["age"]
            file = request.files["image"]

            if not file or file.filename == "":
                flash("Choisir une image", "warning")
                return redirect("/predict")

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            img = image.load_img(filepath, target_size=(224, 224))
            img = image.img_to_array(img) / 255.0
            img = np.expand_dims(img, axis=0)

            pred = float(model.predict(img)[0][0])
            result = "Malignant" if pred > 0.5 else "Benign"

            db = get_db()
            cursor = db.cursor()

            cursor.execute("""
                INSERT INTO patients (name, age, result, probability, image_path)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, age, result, pred, filepath))

            db.commit()
            cursor.close()
            db.close()

            return render_template(
                "result.html",
                result=result,
                prob=round(pred * 100, 2),
                img=filepath
            )

        except Exception as e:
            print(e)
            flash("Erreur système", "danger")
            return redirect("/predict")

    return render_template("predict.html")

# =========================
# PATIENTS
# =========================
@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("patients.html", patients=data)

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)