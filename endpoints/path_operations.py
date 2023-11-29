"""
This module contains endpoint functions aka path operations
"""

# 3rd party packages
from fastapi import APIRouter, HTTPException, Request, Depends
# Project Packages
from analytics.tops import get_top_anime, get_rated_by_user
from data_models import TopAnime, RatedAnime
from endpoints.literals import AnimeGenres, AnimeType
from authentication import authenticate


async def authentorize(user_id: int, request: Request) -> None:
    """
    Authenticates and provides authorization for users
    with x-username and x-key credentials
    :param user_id: ID of user
    :param request: Request object
    :return: None
    """

    # Extracting provided credentials from request headers
    username = request.headers.get("x-username", "")
    user_key = request.headers.get("x-key", "")

    # If authenticated, returns user ID and role, if not, returns False
    user = authenticate(username, user_key)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # If user's role is not admin, she or he can't see other users' activities
    if user.role != "admin" and user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

# Adding router-wide dependency for authentication and authorization to all user related endpoints
router_user = APIRouter(prefix="/api/v1/user", dependencies=[Depends(authentorize)], tags=["User-related Tops"])

router_top = APIRouter(prefix="/api/v1/top", tags=["Public Tops"])


@router_user.get("/{user_id}/top_rated/{top_number}", response_model=list[RatedAnime])
async def top_rated_anime_by_user(user_id: int, top_number: int) -> list[dict]:
    """
    Lists top-rated <top_number> anime by user <user_id>\n
    **param** user_id: ID of user\n
    **param** top_number: Number of top anime\n
    **return** List of anime with description
    """

    return get_rated_by_user(user_id, top_number, True)


@router_user.get("/{user_id}/less_rated/{number}", response_model=list[RatedAnime])
async def less_rated_anime_by_user(user_id: int, number_of: int) -> list[dict]:
    """
    Lists less rated <number_of>  anime by user <user_id>\n
    **param** user_id: ID of user\n
    **param** number_of: Number of less rated anime\n
    **return** List of anime with description
    """

    return get_rated_by_user(user_id, number_of, False)


@router_top.get("/by_rating/{top_number}",  response_model=list[TopAnime])
async def top_anime_by_rating(top_number: int,
                              anime_type: AnimeType = "",
                              genre: AnimeGenres = "") -> list[dict]:
    """
    Lists top-rated <top_number> anime by rating\n
    **param** top_number: Number of top anime\n
    **param** anime_type: Type of anime\n
    **param** genre: Genre of anime\n
    **return** List of anime with description
    """
    return get_top_anime(anime_type,
                         genre,
                         top_number,
                         criteria=["rating", "members"])


@router_top.get("/by_community/{top_number}",  response_model=list[TopAnime])
async def top_anime_by_community(top_number: int,
                                 anime_type: AnimeType = "",
                                 genre: AnimeGenres = "") -> list[dict]:
    """
    Lists top-rated <top_number> anime by community size\n
    **param** top_number: Number of top anime\n
    **param** anime_type: Type of anime\n
    **param** genre: Genre of anime\n
    **return** List of anime with description
    """

    return get_top_anime(anime_type,
                         genre,
                         top_number,
                         criteria=["members", "rating"])


@router_top.get("/by_episodes/{top_number}",  response_model=list[TopAnime])
async def top_anime_by_episodes(top_number: int,
                                anime_type: AnimeType = "",
                                genre: AnimeGenres = "") -> list[dict]:
    """
    Lists top-rated <top_number> anime by number of episodes\n
    **param** top_number: Number of top anime\n
    **param** anime_type: Type of anime\n
    **param** genre: Genre of anime\n
    **return** List of anime with description
    """

    return get_top_anime(anime_type,
                         genre,
                         top_number,
                         criteria=["episodes", "rating"])
