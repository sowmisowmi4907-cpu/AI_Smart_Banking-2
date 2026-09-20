from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)

# Demo secret key
app.secret_key = "ai-smart-banking-demo-key"

# Load transaction dataset
data = pd.read_csv("bank_transactions.csv")


# =========================
# LOGIN
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":

            session["logged_in"] = True

            return redirect(url_for("home"))

    return render_template("login.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def home():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    transactions = []

    for _, row in data.iterrows():

        if row["Is_Fraud"] == 1:
            status = "Suspicious Transaction"
        else:
            status = "Normal Transaction"

        transactions.append({
            "id": row["Transaction_ID"],
            "customer": row["Customer_ID"],
            "amount": row["Transaction_Amount"],
            "type": row["Transaction_Type"],
            "location": row["Location"],
            "status": status
        })

    return render_template(
        "index.html",
        transactions=transactions
    )


# =========================
# NEW TRANSACTION
# =========================

@app.route("/new-transaction", methods=["GET", "POST"])
def new_transaction():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":

        customer_id = request.form["customer_id"]
        amount = float(request.form["amount"])
        transaction_type = request.form["transaction_type"]
        location = request.form["location"]

        if amount >= 20000:

            result = "Suspicious Transaction"

        elif transaction_type == "International":

            result = "Suspicious Transaction"

        elif location.lower() not in ["chennai", "coimbatore"]:

            result = "Suspicious Transaction"

        else:

            result = "Normal Transaction"

    return render_template(
        "transaction.html",
        result=result
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# RUN APPLICATION
# =========================

print("APP STARTED")

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        use_reloader=False
    )
