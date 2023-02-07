from flask import Blueprint, render_template

auth = Blueprint('ath', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<h1> Logout </h1>"

@auth.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")