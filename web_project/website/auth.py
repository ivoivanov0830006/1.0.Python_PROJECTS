from flask import Blueprint, render_template, request

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template("index.html", bolean=True)

@auth.route('/register', methods=["GET", "POST"])
def register():
    data = request.form
    print(data)
    # return render_template("register.html")

# Add more authentication routes as needed
