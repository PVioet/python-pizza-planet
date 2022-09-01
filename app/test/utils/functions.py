import random
import string
from datetime import datetime
from typing import Any, Union


def get_random_string() -> str:
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    return ''.join(letters[:10])


def get_random_choice(choices: Union[tuple, list]) -> Any:
    return random.choice(choices)


def get_random_sample(iterable: Union[tuple, list], length: int = 10) -> list:
    return random.sample(iterable, length)


def get_random_price(lower_bound: float, upper_bound: float) -> float:
    return round(random.uniform(lower_bound, upper_bound), 2)


def shuffle_list(choices: list) -> list:
    choice_copy = choices.copy()
    random.shuffle(choice_copy)
    return choice_copy


def get_random_email() -> str:
    return f"{get_random_string()}@{get_random_choice(['hotmail.com', 'gmail.com', 'test.com'])}"


def get_random_sequence(length: int = 10) -> str:
    digits = list(map(str, range(10)))
    sequence = [digits[random.randint(0, 9)] for _ in range(length)]
    return ''.join(sequence)


def get_random_phone() -> str:
    return get_random_sequence(10)


def get_random_date(start=datetime(1970, 1, 1), end=datetime.now()) -> datetime:
    return datetime.utcfromtimestamp(random.uniform(start.timestamp(), end.timestamp()))
