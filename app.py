import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded - from Finance 
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies) - from Finance
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///reedtime.db")


# From Finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username.")
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Incorrect username or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check that user filled in all fields
        if not username or not password or not confirmation:
            return apology("All fields required.")

        # Check if password confirmation matches password
        elif password != confirmation:
            return apology("Password confirmation does not match.")


        # Check if username is already taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) >= 1:
            return apology("Username already exists.")


        # Insert user data into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Redirect user to home page
        return redirect("/")

    # Route reached via GET
    else:
        return render_template("register.html")


@app.route("/")
@login_required
def index():
    """Show reed log"""

    # Obtain user ID
    user_id = session["user_id"]

    # Create table for user's reeds if not existing
    db.execute("CREATE TABLE IF NOT EXISTS reeds (id INTEGER UNIQUE, user_id INTEGER, datemade TEXT NOT NULL, staple INTEGER NOT NULL, shape TEXT NOT NULL, cane TEXT NOT NULL, tielength NUMERIC NOT NULL, response TEXT NOT NULL, crow TEXT NOT NULL, notes TEXT NOT NULL, PRIMARY KEY(id))")

    # Get all log data from user
    reeds = db.execute("SELECT datemade, staple, shape, cane, tielength, response, crow, notes FROM reeds WHERE user_id = ? ORDER BY id DESC", user_id)

    return render_template("index.html", reeds=reeds)


@app.route("/timer", methods=["GET", "POST"])
@login_required
def timer():
    """Countdown Timer"""

    if request.method == "POST":
        
        # Must enter input into form
        if not request.form.get("minutes"):
            return apology("Must enter minutes.")


        minutes = int(request.form.get("minutes"))

        # Must enter positive number of minutes that is under an hour
        if minutes < 1 or minutes > 59:
            return apology("Must enter valid number of minutes (between 0 and 60).")

        return render_template("timer2.html", minutes=minutes)

    if request.method == "GET":
        return render_template("timer.html")



@app.route("/log", methods=["GET", "POST"])
@login_required
def log():
    """Enter info about new reed into log"""

    if request.method == "POST":

        # Obtain user ID
        user_id = session["user_id"]

        # Store inputs from log forms as variables
        datemade = request.form.get("datemade")
        staple = int(request.form.get("staple"))
        shape = request.form.get("shape")
        cane = request.form.get("cane")
        tielength = request.form.get("tielength")
        response = request.form.get("response")
        crow = request.form.get("crow")
        notes = request.form.get("notes")

        # Create table for reedmaking log data if it does not already exist
        db.execute("CREATE TABLE IF NOT EXISTS reeds (id INTEGER UNIQUE, user_id INTEGER, datemade TEXT NOT NULL, staple INTEGER NOT NULL, shape TEXT NOT NULL, cane TEXT NOT NULL, tielength NUMERIC NOT NULL, response TEXT NOT NULL, crow TEXT NOT NULL, notes TEXT NOT NULL, PRIMARY KEY(id))")

        # Insert inputs from log form into SQL table
        db.execute("INSERT INTO reeds (user_id, datemade, staple, shape, cane, tielength, response, crow, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, datemade, staple, shape, cane, tielength, response, crow, notes)

        # Go to homepage after submitting form
        return index()

    else:
        return render_template("log.html")

# "music.html" is a static HTML page
@app.route("/music")
@login_required
def music():
    """Offer background music suggestions, playlists, and song rec submissions"""

    return render_template("music.html")


# Page that displays graphs based on data in SQL table
@app.route("/patterns")
@login_required
def patterns():
    """Display graphs of trends in response and crow"""

    # Obtain user_id
    user_id = session["user_id"]

    # Use COUNT() SQL function to calculate data points for graphs

    # Response
    yes = db.execute("SELECT COUNT(response) FROM reeds WHERE response = 'Yes' AND user_id = ?", user_id)[0]['COUNT(response)']
    no = db.execute("SELECT COUNT(response) FROM reeds WHERE response = 'No' AND user_id = ?", user_id)[0]['COUNT(response)']

    # Crow
    flat = db.execute("SELECT COUNT(crow) FROM reeds WHERE crow = 'Flat' AND user_id = ?", user_id)[0]['COUNT(crow)']
    uptopitch = db.execute("SELECT COUNT(crow) FROM reeds WHERE crow = 'Up to Pitch' AND user_id = ?", user_id)[0]['COUNT(crow)']
    sharp = db.execute("SELECT COUNT(crow) FROM reeds WHERE crow = 'Sharp' AND user_id = ?", user_id)[0]['COUNT(crow)']

    return render_template("patterns.html", yes=yes, no=no, flat=flat, uptopitch=uptopitch, sharp=sharp)

# From finance
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# From Finance
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors - from Finance
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)