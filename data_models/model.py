"""
This module contains all data models used in project
"""

from pydantic import BaseModel, Field


# Anime model
class TopAnime(BaseModel):
    name: str
    genre: list[str]
    type_of: str = Field(..., alias="type")
    episodes: int
    rating: float
    community: int = Field(..., alias="members")


# User model
class User(BaseModel):
    user_id: int
    role: str


# Anime model with user rating
class RatedAnime(BaseModel):
    name: str
    genre: list[str]
    user_rating: int


# Event log model
class RequestLog(BaseModel):
    timestamp: str = ""
    client_ip: str = "0.0.0.0"
    client_port: int = 0
    url: str = ""
    method: str = ""
    user_agent: str | None = ""
    username: str | None = ""
    user_key: str | None = ""
    response_code: int = 0
