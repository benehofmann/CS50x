import os
import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///insurance.db")

@app.route("/")
@login_required
def index():

    return render_template("calculate.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM clients WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"] # user is logged in

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
      return render_template("register.html")
    else:
        #get all the variables from the user
        username = request.form.get("username")
        if request.form.get("password") == request.form.get("repassword"):
            passwordHash = generate_password_hash(request.form.get("password"))
            print(passwordHash)
        else:
            return apology("400", "invalid passwords")
        first_name = request.form.get("first_name").capitalize()
        last_name = request.form.get("last_name").capitalize()
        birthday = request.form.get("date")
        street = request.form.get("street")
        housenumber = request.form.get("housenumber")
        city = request.form.get("city")
        zipcode = request.form.get("zip")
        gender = request.form.get("gender")
        email = request.form.get("email")

        #check if username is already taken
        rows = db.execute("SELECT username FROM clients WHERE username = :username", username=username)
        if len(rows) != 0:
            return apology("Username taken", 400)

        #check if email is already taken
        rows = db.execute("SELECT email FROM clients WHERE email = :email", email=email)
        print(rows)
        if len(rows) != 0:
            return apology("Email taken", 401)


        #now insert into DB
        db.execute("INSERT INTO clients (username, hash, first_name, last_name, geb_date, gender, street, housenumber, zip_code, city, email) VALUES (:username, :passwordHash, :first_name, :last_name,:birthday, :gender,  :street, :housenumber, :zipcode, :city, :email)", username=username, passwordHash=passwordHash, first_name=first_name, last_name=last_name, birthday=birthday, street=street, housenumber=housenumber, city=city, zipcode=zipcode, gender=gender, email=email)


    return redirect("/")


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "GET":
      return render_template("calculate.html")

    else:
        return apology("400", "400")