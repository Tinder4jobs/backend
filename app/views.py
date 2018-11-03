import struct
import json
from typing import *

from typedload import load, dump
from flask import request

from app import app, db


@app.route('/')
def index() -> str:
    return 'People suck!'


@app.route('/login', methods=('POST',))
def login():
    token = db.login(**json.load(request.stream))
    if token:
        return token
    raise('Invalid login')


@app.route('/question/<token>', methods=('GET',))
def get_question(token: str) -> str:
    q = db.get_question(db.get_user_from_token(token))
    return stuff2str(q)


@app.route('/clear', methods=('POST',))
def clear():
    db.clear()
    return ''


@app.route('/response/<token>', methods=('POST',))
def set_question(token: str) -> str:
    response = load(json.load(request.stream), db.Response)
    db.save_response(db.get_user_from_token(token), response)
    return ''

@app.route('/matches/<token>', methods=('GET',))
def best_matches(token: str) -> str:
    q = db.get_matches(db.get_user_from_token(token))
    return stuff2str(q)


def stuff2str(stuff: Any):
    return json.dumps(dump(stuff))
