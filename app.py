from Project2 import db, app
from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_user, logout_user, login_required
from Project2.models import User
from Project2.forms import LoginForm, RegistrationForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out!")
    return redirect(url_for('home'))


@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in succesfully!')

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('welcome_user')

            return redirect(next)

    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.email.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Registration Successfull!")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


app.run(debug=True)
