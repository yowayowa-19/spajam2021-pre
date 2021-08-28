# from typing import Optional
from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import APIRouter


router = APIRouter()


class MacAddress(BaseModel):
    mac_address: str


class UserRegistration(BaseModel):
    mac_address: str
    user_name: str


class Pairing(BaseModel):
    mac_address: str
    phrase: str


@dataclass
class Ranking:
    name: str
    score: int
    rank: int
    hand: str
    isMe: bool


rank_result: list[Ranking] = [{"name": "りあ", "score": 300, "rank": 1,
                               "hand": "フルハウス", "isMe": True},
                              {"name": "Chika", "score": 299, "rank": 2,
                               "hand": "ワンペア", "isMe": False},
                              {"name": "Riko", "score": 287, "rank": 3,
                               "hand": "ワンペア", "isMe": False},
                              {"name": "Kanan", "score": 296, "rank": 4,
                               "hand": "ワンペア", "isMe": False},
                              {"name": "Daiya", "score": 295, "rank": 5,
                               "hand": "ワンペア", "isMe": False},
                              {"name": "You", "score": 294, "rank": 6,
                                  "hand": "ワンペア", "isMe": False},
                              {"name": "Yoshiko", "score": 293, "rank": 7,
                               "hand": "ワンペア", "isMe": False},
                              {"name": "Hanamaru", "score": 292, "rank": 8,
                               "hand": "ワンペア", "isMe": False},
                              {"name": "Mari", "score": 291, "rank": 9,
                               "hand": "ワンペア", "isMe": False},
                              {"name": "Ruby", "score": 290, "rank": 10, "hand": "ワンペア", "isMe": False}]


@router.post("/mobile/register/")
async def register(user: UserRegistration):
    return {"succeed": True}


@router.post("/mobile/checksend/")
async def check_send(mac_address: MacAddress):
    return {"succeed": True}


@router.post("/mobile/ranking")
async def ranking(mac_address: MacAddress) -> list[Ranking]:
    return rank_result


@router.post("/mobile/me")
async def me(mac_address: MacAddress) -> Ranking:
    return {"name": "りあ", "score": 300, "rank": 1, "hand": "フルハウス", "isMe": True}


@router.post("/mobile/stop")
async def stop(mac_address: MacAddress):
    return {"succeed": True}


@router.post("/mobile/pairing")
async def pairing(pairing_data: Pairing):
    return {"succeed": True}
