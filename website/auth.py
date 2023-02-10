from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import models, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

import re

auth = Blueprint('auth', __name__)

regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
regexPassword = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$' 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            user = models.User.query.filter_by(email=email).first_or_404()
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password!", category='error')
        except:
            flash("This email does not exist!", category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = models.User.query.filter_by(email=email)
        
        if re.fullmatch(regexEmail, email) == None:
            flash("Invalid email address!", category='error')
        elif user is not None:
            flash("This email address already exists in the database!", category='error')
        elif len(firstName) < 2:
            flash("Your first name must be at least 2 characters!", category='error')
        elif len(lastName) < 2:
            flash("Your last name must be at least 2 characters!", category='error')
        elif password2 != password1:
            flash("Confirm password don\'t match!", category='error')
        elif len(password1) < 2:    # re.fullmatch(regexPassword, password1) == None:
            flash("Your password is too short!", category='error')
        else:
            new_user = models.User(email=email, first_name=firstName.strip(), last_name=lastName.strip(), password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account was created successfully!", category='success') 
            return redirect(url_for('views.home'))
            
    return render_template("sign-up.html", user=current_user)