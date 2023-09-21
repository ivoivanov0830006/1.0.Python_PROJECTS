from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from .models import User  # Import the User model
from flask_bcrypt import Bcrypt

# Create the authentication blueprint
auth = Blueprint("auth", __name__)

# SQLite database setup (You can use a more robust database like SQLAlchemy)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a table to store user information if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

# Initialize bcrypt
bcrypt = Bcrypt()


def authenticate_user(username, password):
    # Print all users in the database (before the query)
    all_users = User.query.all()
    print("All users in the database:")
    for user in all_users:
        print(f"Username: {user.username}, Password: {user.password}")

    print(f"Authenticating user: {username}")
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"User found: {user.username}")
        if user.password == password:
            print("Password matches")
            return user
        else:
            print("Password does not match")
    else:
        print("User not found")

    # Print all users in the database (after the query)
    all_users = User.query.all()
    print("All users in the database after query:")
    for user in all_users:
        print(f"Username: {user.username}, Password: {user.password}")

    return None

@auth.route('/indexLoginR')
def index_login():
    return render_template("indexLoginR.html")


@auth.route('/indexRegisterR')
def index_register():
    return render_template("indexRegisterR.html")


@auth.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("views.home"))  # Redirect to the home page after logout


@auth.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"Username: {username}, Password: {password}")
        user = authenticate_user(username, password)

        if user:
            # Store user ID in the session to keep the user logged in
            session['user_id'] = user.id
            flash("Login successful", "success")
            print("Login successful")
            return redirect(url_for("auth.index_login"))  # Redirect to the dashboard or a protected page
        else:
            flash("Login failed. Invalid credentials.", "danger")

    return render_template("index.html")


@auth.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Create a new database connection and cursor for this request
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))  # Store the plain text password
            conn.commit()
            flash("Registration successful. You can now log in.", "success")
            print("Register successful")
            return redirect(url_for("auth.index_register"))
        except sqlite3.Error as e:
            # Handle any potential database errors here
            flash(f"Error: {str(e)}", "danger")
        finally:
            # Close the database connection and cursor
            cursor.close()
            conn.close()
    return render_template("index.html")

