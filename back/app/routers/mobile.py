from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import APIRouter

from controller import users
from controller.users import Users

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


@router.post("/mobile/register/")
async def register(user: UserRegistration):
    result = Users().register(user.mac_address, user.user_name)
    return {"succeed": result}


@router.post("/mobile/checksend/")
async def check_send(mac_address: MacAddress):
    mac_addr = mac_address.mac_address
    return {"succeed": users.is_sending(mac_addr)}


@router.post("/mobile/ranking")
async def ranking(mac_address: MacAddress) -> list[Ranking]:
    []
    return users.ranking(mac_address)


@router.post("/mobile/me")
async def me(mac_address: MacAddress) -> Ranking:
    return users.me(mac_address)
   
@router.post("/mobile/stop")
async def stop(mac_address: MacAddress):
    mac_addr = mac_address.mac_address
    print("/mobile/stop")
    users.Users().stop_phrase(mac_addr)
    return {"succeed": True}


@router.post("/mobile/pairing")
async def pairing(pairing_data: Pairing):
    result = users.Users().pairing(pairing_data.mac_address, pairing_data.phrase)
    return {"succeed": result}
