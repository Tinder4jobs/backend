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
