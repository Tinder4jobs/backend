import struct

from flask import request

from app import app

data = {}
screen_mapping = {}

@app.route('/')
def index():
    return 'People suck!'
