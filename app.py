from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('bmi_history.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS bmi_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, weight REAL, height REAL, bmi REAL, date TEXT)''')
    conn.commit()
    conn.close()

def calculate_bmi(weight, height):
    return weight / (height * height)

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal"
    elif bmi < 30: return "Overweight"
    else: return "Obese"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    name = request.form.get("name")
    weight = float(request.form.get("weight"))
    height = float(request.form.get("height"))
    bmi = round(calculate_bmi(weight, height), 2)
    category = bmi_category(bmi)
    conn = get_db_connection()
    conn.execute("INSERT INTO bmi_history (name, weight, height, bmi, date) VALUES (?,?,?,?,?)",
                 (name, weight, height, bmi, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return render_template("result.html", name=name, weight=weight, height=height, bmi=bmi, category=category)

@app.route("/history")
def history():
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM bmi_history ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("result.html", history=records, show_history=True)

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST": name = request.form.get("name")
    else: name = request.args.get("name")
    if not name: return "Please enter a name."
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM bmi_history WHERE LOWER(name) = LOWER(?) ORDER BY id ASC", (name,)).fetchall()
    conn.close()
    if len(records) == 0:
        return render_template("result.html", error=f"No BMI history found for {name}.")
    bmi_values = [float(r["bmi"]) for r in records]
    dates = [r["date"] for r in records]
    latest_bmi = bmi_values[-1]
    first_bmi = bmi_values[0]
    difference = round(latest_bmi - first_bmi, 2)
    if difference > 0.5: trend = "Increasing"
    elif difference < -0.5: trend = "Decreasing"
    else: trend = "Stable"
    average_bmi = round(sum(bmi_values) / len(bmi_values), 2)
    latest_category = bmi_category(latest_bmi)
    return render_template("result.html", name=name, records=records, latest_bmi=latest_bmi, first_bmi=first_bmi, average_bmi=average_bmi, difference=difference, trend=trend, category=latest_category, bmi_values=bmi_values, dates=dates, show_analysis=True)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)