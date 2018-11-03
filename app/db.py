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


conn = sqlite3.connect('db')
sessions = {}


def create():
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
            username TEXT UNIQUE
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


def get_question(user_id: int) -> Optional[Question]:
    """
    Returns a question that the user has not answered to
    """
    cursor = conn.cursor()
    q = cursor.execute('''
        SELECT *
        FROM questions
        WHERE questions.id NOT IN (
            SELECT qid FROM seekers_replies WHERE uid = ?
        )
        LIMIT 1
    ''', (user_id,)).fetchone()
    cursor.close()
    if q:
        return Response(q)
    return q


def save_response(user_id: int, response: Response) -> None:
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO seekers_replies
        VALUES (?, ?, ?, ?)
    ''', (user_id, ) + tuple(response))
    cursor.close()
