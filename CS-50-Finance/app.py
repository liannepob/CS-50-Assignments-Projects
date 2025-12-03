import os
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
# makes a whole new table for the user stocks and its profile
db.execute("""
CREATE TABLE IF NOT EXISTS user_portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price REAL NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deal TEXT NOT NULL
)
""")
# using 3 quotes to organize SQL query, using CREATE TABLE IF NOT EXISTS from cs50 duck to prevent runtime error


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    current_user = session["user_id"]
    # will get the current user through session
    portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM user_portfolio WHERE user_id = ? GROUP BY symbol HAVING shares > 0",
        current_user
    )
    # will create a variable called portfolio and select the data from the user_portfolio table at the current user's value

    user_showcase = []  # will create an empty array for the user's data that needs to be rendered
    total_stock = 0  # will create a total stock value

    # now i need to loop through the portfolio dictionaries to find the ones for the user
    for stock in portfolio:
        info = lookup(stock["symbol"])  # now will loop through all and get the info for each stock
        if info:
            price = info["price"]
            total = stock["shares"] * price
            user_showcase.append({
                "symbol": stock["symbol"],
                "shares": stock["shares"],
                "price": price,
                "total": total
            })
            total_stock += total

    row = db.execute("SELECT cash FROM users WHERE id = ?", current_user)
    cash = row[0]["cash"]
    # then will get the cash balance of the current user
    final_total = total_stock + cash
    # this will get the total value of the po4rtfolio + cash

    return render_template(
        "index.html",
        user_showcase=user_showcase,
        cash=cash,
        total_stock=total_stock,
        final_total=final_total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # makes the symbol uppercase to prevent duplicates
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not shares or not shares.isdigit() or int(shares) < 1:
            return apology("please provide a valid number of shares", 400)
        shares = int(shares)
        # gets 2 variables, symbol and stock(turns shares into an int)

        if not symbol:
            return apology("must provide a stock symbol", 400)
        # check for input

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol", 400)
        # checks if the stock is valid

        current_user = session["user_id"]
        price = stock["price"]
        stock_price = shares * price

        cash = db.execute("SELECT cash FROM users WHERE id = ?", current_user)[0]["cash"]
        if stock_price > cash:
            return apology("sorry, you don't have enough funds", 400)
        # gets the cash amt of the user and checks for funds

        db.execute("INSERT INTO user_portfolio (user_id, symbol, shares, price, deal) VALUES (?, ?, ?, ?, ?)",
                   current_user,
                   symbol,
                   shares,
                   price,
                   "bought"
                   )

        # Update cash
        updated_cash = cash - stock_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, current_user)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    current_user = session["user_id"]
    data = db.execute("SELECT * FROM user_portfolio WHERE user_id = ?", current_user)
    return render_template("history.html", data=data)
    # displays an HTML table sum of all user's transactions (row/row and each buy/sell)
    # each row should be clear if it was bought & incl. stock symbol(purchase/sale), number of shares sold, & time/date at the transaction


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide a stock symbol", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol", 400)

        return render_template("quoted.html",
                               name=stock["name"],
                               price=stock["price"],
                               symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate input
        if not username:
            return apology("please enter a username", 400)
        if not password:
            return apology("please enter a password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        # Check if username exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Hash password and insert into DB
        hashed_pass = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, hashed_pass)

        # Log in user
        userID = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = userID

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    current_user = session["user_id"]

    if request.method == "POST":
        # Get form input
        stock_name = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate input
        if not stock_name:
            return apology("must provide a stock symbol", 400)
        if not shares or int(shares) < 1:
            return apology("must provide a valid number of shares", 400)

        stock_shares = int(shares)

        # Check user owns enough shares
        owned = db.execute(
            "SELECT SUM(shares) AS total FROM user_portfolio WHERE user_id = ? AND symbol = ?",
            current_user, stock_name
        )[0]["total"]

        if owned is None or owned < stock_shares:
            return apology("not enough shares", 400)

        # Get current stock price
        current_price = lookup(stock_name)["price"]

        # Insert negative shares to record sale
        db.execute(
            "INSERT INTO user_portfolio (user_id, symbol, shares, price, deal) VALUES (?, ?, ?, ?, ?)",
            current_user, stock_name, -stock_shares, current_price, "sold"
        )

        # Update user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", current_user)[0]["cash"]
        updated_cash = cash + (stock_shares * current_price)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, current_user)

        return redirect("/")

    else:
        # GET request: show form with user's stocks
        user_stock = db.execute(
            "SELECT symbol FROM user_portfolio WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            current_user
        )
        return render_template("sell.html", user_stock=user_stock)

# personal touch feature


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_pass():

    current_user = session["user_id"]

    if request.method == "POST":
        old_pass = request.form.get("old_password")
        new_pass = request.form.get("new_password")

        if not old_pass:
            return apology("please enter the current password", 403)
        # check to make sure a current password was entered
        if not new_pass:
            return apology("please enter a new password", 403)
        # check to make sure a new password was entered

        current = db.execute("SELECT hash FROM users WHERE id = ?", current_user)
        if not check_password_hash(current[0]["hash"], old_pass):
            return apology("invalid password, try again", 403)

        new_hashed = generate_password_hash(new_pass)
        # new hashed pass for the user
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hashed, current_user)
        return redirect("/")
    else:
        return render_template("change_password.html")
