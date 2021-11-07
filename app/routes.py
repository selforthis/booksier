from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def hello_world():
    user = {'username': 'Lola'}
    books = [
        {
            "title": "Grinberg - The New And Improved Flask Mega-Tutorial (2017)",
            "total_pages": 496
        },
        {
            "title": "Lott - Modern Python Cookbook (2020)",
            "total_pages": 789
        },
    ]
    return render_template('index.html', title='Home', user=user, books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'
              .format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign in', form=form)
