# jinder (tinder4jobs)
# Copyright (C) 2018 Salvo "LtWorf" Tomaselli
#
# jinder (tinder4jobs) is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

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
