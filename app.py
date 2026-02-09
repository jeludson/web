from flask import Flask, render_template, request, redirect, session
from models import db, Contact, Admin
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-secret")

# DATABASE
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# CREATE TABLES + ADMIN (SAFE)
with app.app_context():
    db.create_all()
    if not Admin.query.first():
        admin = Admin(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        contact = Contact(
            name=request.form["name"],
            email=request.form["email"],
            message=request.form["message"]
        )
        db.session.add(contact)
        db.session.commit()
        return redirect("/")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        admin = Admin.query.filter_by(
            username=request.form["username"]
        ).first()

        if admin and admin.check_password(request.form["password"]):
            session["admin"] = admin.id
            return redirect("/admin")

    return render_template("login.html")

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")

    contacts = Contact.query.order_by(Contact.id.desc()).all()
    return render_template("admin.html", contacts=contacts)

@app.route("/admin/change-credentials", methods=["GET", "POST"])
def change_credentials():
    if "admin" not in session:
        return redirect("/login")

    admin = Admin.query.get(session["admin"])

    if request.method == "POST":
        if request.form.get("username"):
            admin.username = request.form["username"]
        if request.form.get("password"):
            admin.set_password(request.form["password"])
        db.session.commit()
        return redirect("/admin")

    return render_template("change_credentials.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)