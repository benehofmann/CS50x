import os
import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #get the the user_id
    user_id = session["user_id"]
    #get the current user_cash
    user_cash_data = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
    userCash = round(user_cash_data[0].get("cash"),2)
    #get all the stocks the user is holding
    #1 iterate over transactions to get all the transactions for the user and  copy into list
    stockData = db.execute("SELECT DISTINCT symbol from transactions WHERE user_id = :user_id", user_id=user_id)
    stockSymbols = []
    for row in stockData:
        stockSymbols.append(row.get("symbol"))
    #get the sum of all bought and sold stocks and put them in seperate dicts
    userBought = {}
    userSold = {}
    for i in stockSymbols:
        boughtStocks = db.execute("SELECT sum(amount) AS bought FROM transactions WHERE user_id = :user_id AND transaction_type = 'buy' AND symbol = :i", i=i, user_id=user_id)
        soldStocks = db.execute("SELECT sum(amount) AS sold FROM transactions WHERE user_id = :user_id AND transaction_type = 'sell' AND symbol = :i", i=i, user_id=user_id)
        userBought[i] = boughtStocks[0].get("bought")
        userSold[i] = soldStocks[0].get("sold")
        #check if stock has been sold
        if userSold[i] == None:
            userSold[i] = 0 # set to 0 to secure arithmetic operations

    userStocks = {} #to save how many share of a stocks the user owns
    stockValues = {} #to save the value of each stock
    valueOfAllStocks = 0
    #create the difference of both dicts userBought and userSold and generate a dict with the correct stock values
    #TODO
    for key in userBought:
       #difference of buy AND sell
        difference = userBought[key] - userSold[key]
        #create
        userStocks[key] = difference
       #create the dict with the correct values
        stockValues[key] = round((lookup(key).get("price") * difference), 2)
        valueOfAllStocks += round((lookup(key).get("price") * difference), 2)

     #TODO renders the template with your current portfolio
    return render_template("index.html", userStocks = userStocks, stockValues = stockValues, userCash = userCash, valueOfAllStocks = valueOfAllStocks) # need to implement


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        #get initialize import variables
        symbol = request.form.get("symbol")
        quote =  lookup(symbol)
        if not quote:
            return apology("No such stock", 401)
        timestamp = str(datetime.datetime.now())
        user_id = session["user_id"]
        price = round(quote["price"],2)
        shares = int(request.form.get("shares"))
        userData = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)
        currentCash = userData[0].get('cash')
        cashNeeded = shares * price
        newCash = currentCash - cashNeeded

        #price for current cash to high
        if cashNeeded > currentCash:
            return apology("402", "You are too poor to buy so much")

        #write into purchase history

        db.execute("INSERT INTO transactions (user_id, symbol, amount, transaction_type, price_per_stock, timestamp) VALUES(:user_id, :symbol, :shares, :transaction_type, :price_per_stock, :timestamp)", user_id=user_id, symbol=symbol, shares=shares, transaction_type='buy', price_per_stock = price, timestamp = timestamp)
        #update user Data in database
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=newCash, user_id=user_id)
        flash("Bought successfull!")
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    history = db.execute("SELECT symbol, amount, transaction_type, price_per_stock, timestamp from transactions where user_id = :user_id", user_id = user_id)



    return render_template("history.html", history = history) # need to implement


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("No such stock", 401)

        return render_template("quoted.html", stock = stock)






@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
      return render_template("register.html")
    else:
      name = request.form.get("name") # via the html name tag "name"
      if not name: # no name typed
         return render_template("apology.html")
         #check of passwords are equal and hash the password
      if request.form.get("password") == request.form.get("repassword"):
          passwordHash = generate_password_hash(request.form.get("password"))
          #check if the username is already taken
          rows = db.execute("SELECT * FROM users WHERE username = :name", name=name)
          if len(rows) != 0:
              return apology("Username taken", 400)
      # Username free, now inserting in the DB
      db.execute("INSERT INTO users (username, hash) VALUES (:name, :passwordHash)", name=name, passwordHash=passwordHash)
      return redirect("/")







@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        #get initialize import variables
        symbol = request.form.get("symbol")
        quote =  lookup(symbol)
        if not quote:
            return apology("No such stock", 401)
        timestamp = str(datetime.datetime.now())
        user_id = session["user_id"]
        price = round(quote["price"],2)
        shares = int(request.form.get("shares"))
        userData = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)
        currentCash = userData[0].get('cash')
        cashForSell = shares * price
        newCash = currentCash + cashForSell

        #check if user has enough stocks to sell
        boughtStocks = db.execute("SELECT sum(amount) as bought from transactions WHERE user_id = :user_id and transaction_type = 'buy' AND symbol = :symbol", user_id = user_id, symbol = symbol)
        if boughtStocks[0].get("bought") == None:
            return apology("You don't have that stock", "400")
        soldStocks = db.execute("SELECT sum(amount) as sold from transactions WHERE user_id = :user_id and transaction_type = 'sell' and symbol = :symbol", user_id = user_id, symbol = symbol)

        #user doesn't own that stock
        currentStocks = 0
        if soldStocks[0].get("sold") == None:
            soldStocks["sold"] = 0;

        currentStocks = boughtStocks[0].get("bought") - soldStocks[0].get("sold")
        if currentStocks < shares:
            return apology("not enough stocks to sell", "400")
        else:
            #write into purchase history
            db.execute("INSERT INTO transactions (user_id, symbol, amount, transaction_type, price_per_stock, timestamp) VALUES(:user_id, :symbol, :shares, :transaction_type, :price_per_stock, :timestamp)", user_id=user_id, symbol=symbol, shares=shares, transaction_type='sell', price_per_stock = price, timestamp = timestamp)
            #update user Data
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=newCash, user_id=user_id)
            flash("Sell successfull!")
            return render_template("sell.html")




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
