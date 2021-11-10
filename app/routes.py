from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, LoginForm, RegistrationForm, BookForm, EditProfileForm, User, Book


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = BookForm()
    books = Book.query.filter_by(user=current_user)
    if not form.validate_on_submit():
        return render_template("index.html", title='Home Page', form=form,
                               books=books)
    book = Book(title=form.title.data, total_pages=form.total_pages.data, user=current_user)
    db.session.add(book)
    db.session.commit()
    flash('A new book was added successfully!')
    return redirect(url_for('index'))


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


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if not form.validate_on_submit():
        if request.method == 'GET':
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', title='Edit Profile',
                               form=form)
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('user', username=current_user.username))
