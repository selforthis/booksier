from flask import render_template
from app import app


@app.route('/')
def hello_world():
    user = {'username': 'Lola'}
    return render_template('index.html', title='Home', user=user)
