from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, LoginForm, RegistrationForm, User, Book


@app.route('/')
@app.route('/index')
@login_required
def index():
    books = Book.query.all()
    return render_template('index.html', title='Home', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', title='Sign in', form=form)
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', title='Register', form=form)
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, {}, you are now a registered user!'.format(user.username))
    return redirect(url_for('login'))


@app.route('/user/<username>')
@login_required
def user(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query.filter_by(user=user)
    return render_template('user.html', user=user, books=books)
