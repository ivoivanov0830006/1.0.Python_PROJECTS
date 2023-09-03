from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/contacts')  # Define a route for the contacts page
def contacts():
    return render_template("contacts.html")

@views.route('/shop')  # Define a route for the shop page
def shop():
    return render_template("shop.html")
