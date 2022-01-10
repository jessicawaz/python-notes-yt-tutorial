from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# name blueprint
auth = Blueprint('auth', __name__)

# -- routes --

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Filter users by email
        user = User.query.filter_by(email=email).first()
        # if user w/ email exists, check if password is correct
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # log user in, and remember that the user is loggin in
                login_user(user, remember=True) 
                # send user to homepage after successful login
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect password. Try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # get data from sign up form
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Get user by email
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        # check if all fields are valid
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category="error")
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category="error")
        else:
            # create new user to add to db
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            # add new user to db
            db.session.add(new_user)
            # Log user in after signing up
            login_user(user, remember=True)
            db.session.commit()

            flash('Account Created!', category="success")

            # redirect user to home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# -- end routes --