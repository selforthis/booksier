from flask import render_template
from app import app


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
