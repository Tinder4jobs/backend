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

from typing import *
import sqlite3

from typedload import load, dump


class Question(NamedTuple):
    id: int
    text: str
    category_id: int
    image: str


class Response(NamedTuple):
    id: int
    response: bool
    relevance: float


class User(NamedTuple):
    id: int
    username: str


class Company(NamedTuple):
    id: int
    username: str
    image: str
    description: str
    location: str


sessions = {}


def create():
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies
        (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            image TEXT,
            description TEXT,
            location TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies_replies
        (
            cid INTEGER,
            qid INTEGER,
            reply INTEGER
        )
    ''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS questions
            (
                id INTEGER PRIMARY KEY,
                text TEXT,
                category_id INTEGER,
                image TEXT
            )
        ''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS seekers_replies
            (
                uid INTEGER,
                qid INTEGER,
                reply INTEGER,
                relevance REAL
            )
        ''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS companies_replies
            (
                cid INTEGER,
                qid INTEGER,
                reply INTEGER
            )
        ''')
    cursor.close()


def login(username: str, password: str) -> Optional[str]:
    '''
    Returns a session token for a login
    '''
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    u = cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username, )).fetchone()
    if u:
        user = User(u)
        token
        sessions[token] = user.id
        return token
    return None


def get_user_from_token(token: str) -> int:
    return 1
    return sessions[token]


def get_question(user_id: int) -> List[Question]:
    """
    Returns a question that the user has not answered to
    """
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    q = cursor.execute('''
        SELECT *
        FROM questions
        WHERE questions.id NOT IN (
            SELECT qid FROM seekers_replies WHERE uid = ?
        )
        LIMIT 10
    ''', (user_id,)).fetchall()
    cursor.close()
    return [Question(*i) for i in q]


def clear() -> None:
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM seekers_replies')
    conn.commit()
    cursor.close()


def save_response(user_id: int, response: Response) -> None:
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO seekers_replies
        VALUES (?, ?, ?, ?)
    ''', (user_id, ) + tuple(response))
    conn.commit()
    cursor.close()


def get_matches(user_id: str) -> List[Company]:
    conn = sqlite3.connect('db')
    cursor = conn.cursor()

    c = cursor.execute('''
        SELECT id, username, image, description, location
        FROM companies, (
            SELECT cid, sum(q) as compatibility
            FROM (
                SELECT *,
                (
                    relevance * (CASE (companies_replies.reply = seekers_replies.reply) WHEN 1 THEN 1 WHEN 0 THEN -1 END)
                ) AS q
                FROM seekers_replies, companies_replies
                WHERE seekers_replies.qid = companies_replies.qid AND seekers_replies.uid = ?
            )
            GROUP BY cid
            ORDER BY compatibility DESC
        )
        WHERE id=cid
        LIMIT 10
        ;
    ''', (user_id,)).fetchall()
    cursor.close()
    print(c)
    return [Company(*i) for i in c]
