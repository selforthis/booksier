"""Configuration file of the application"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # class variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

