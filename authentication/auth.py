"""
This module contains function, which provides authentication and authorization
"""

import pandas as pd
from data_models import User

# Reading user credentials database
user_keys = pd.read_csv("./data/userauth.csv")


def authenticate(username: str, user_key: str) -> User | bool:
    """
    Checks username and key into the database,
    if they exist, returns matching user id and user role
    :param username: Username provided by user
    :param user_key: Key provided by user
    :return: Returns user ID and role or returns False if authentication fails
    """
    user = user_keys[(user_keys["username"] == username) & (user_keys["user_key"] == user_key)]

    if user.empty:
        return False

    user = user[["user_id", "role"]].to_dict(orient='records')[0]

    try:
        user = User(**user)
    except Exception as ex:
        print(str(ex))
        return False
    return user
