from typing import *

from typedload import load, dump



class Question(NamedTuple):
    id: int
    text: str
    image: str

class Response(NamedTuple):
    id: int
    response: bool
    relevance: float


def create():
    pass


def get_user_from_token(token: str) -> int:
    return 12

def get_question(user_id: int) -> Question:
    #TODO

    return Question(3, 'Do you like the taste of beer?', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Export_hell_seidel_steiner.png/220px-Export_hell_seidel_steiner.png')

def save_response(user_id: int, response: Response) -> None:
    pass
