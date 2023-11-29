"""
This module includes functions which creates top lists for endpoints using pandas
"""
import pandas as pd
from pandas import DataFrame

# Load files into dataframes
anime_df = pd.read_csv("./data/anime.csv")
rating_df = pd.read_csv("./data/rating.csv")

# Optimizes column type
anime_df["episodes"] = anime_df["episodes"].replace("Unknown", "-1")
anime_df["episodes"] = anime_df["episodes"].astype("int")

# Fills missing values
anime_df["genre"] = anime_df["genre"].fillna("")
anime_df["type"] = anime_df["type"].fillna("")


def sort_and_top(dataframe: DataFrame, top_number: int, *, criteria: list) -> list[dict]:
    """
    Sorts given dataframe by provided criteria
    and returns top <top number> rows as list of dict
    :param dataframe: A source dataframe
    :param top_number: Number of top rows to be listed
    :param criteria: List of rows by which dataframe must be sorted
    :return: Top <top number> rows as list of dict
    """
    tops = (
        dataframe
        .sort_values(by=criteria, ascending=[False, False])
        .head(top_number)
        [["name", "genre", "type", "episodes", "rating", "members"]]
    )

    tops["genre"] = tops["genre"].map(lambda x: x.split(", "))
    return tops.to_dict(orient='records')


def get_top_anime(anime_type: str, genre: str, top_number: int, *, criteria: list) -> list[dict]:
    """
    Filters anime dataframe by provided anime type and genre
    and calls sort_and_top function for filtered dataframe
    :param anime_type: Type of anime
    :param genre: Genre of anime
    :param top_number: Number of top rows to be listed
    :param criteria: List of rows by which dataframe must be sorted
    :return: Top <top number> rows as list of dict
    """
    anime_df_filtered = anime_df.loc[(anime_df["genre"].str.contains(genre)) &
                                     (anime_df["type"].str.contains(anime_type))]
    return sort_and_top(anime_df_filtered, top_number, criteria=criteria)


def get_rated_by_user(user_id: int, number_of: int, top: bool) -> list[dict]:
    """
    Finds and lists top or bottom rated anime by specific user
    :param user_id: ID of user
    :param number_of: Number of top rows to be listed
    :param top: Flag describing whether top or bottom list needed
    :return: Top <top number> rows as list of dict
    """

    rating_sorted = (
        rating_df
        .loc[(rating_df["user_id"] == user_id) & (rating_df["rating"] != -1)]
        .sort_values(by=["rating"], ascending=(not top))
        .head(number_of)
    )

    top_users = (
        anime_df
        .set_index("anime_id")
        .loc[rating_sorted["anime_id"]]
        [["name", "genre"]]
    )

    top_users["genre"] = top_users["genre"].map(lambda x: x.split(", "))
    top_users["user_rating"] = rating_sorted["rating"].values

    return top_users.to_dict(orient='records')
