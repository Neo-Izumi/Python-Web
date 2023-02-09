from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import models, db
from werkzeug.security import generate_password_hash, check_password_hash

import re

auth = Blueprint('ath', __name__)

regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
regexPassword = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$' 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<h1> Logout </h1>"

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if re.fullmatch(regexEmail, email) == None:
            flash("Invalid email address !!!", category='error')
        elif len(firstName) < 2:
            flash("Your first name must be at least 2 characters", category='error')
        elif len(lastName) < 2:
            flash("Your last name must be at least 2 characters", category='error')
        elif password1 != password2:
            flash("Confirm password don\'t match", category='error')
        elif len(password1) < 2:    # re.fullmatch(regexPassword, password1) == None:
            flash("Your password is too short", category='error')
        else:
            new_user = models.User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account was created successfully", category='success') 
            return redirect(url_for('.login'))
        
    return render_template("sign-up.html")