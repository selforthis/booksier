"""Configuration file of the application"""

import os


class Config(object):
    # class variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
