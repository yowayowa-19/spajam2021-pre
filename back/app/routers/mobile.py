from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import APIRouter

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
    "ユーザー登録する"
    result = Users().register(user.mac_address, user.user_name)
    return {"succeed": result}


@router.post("/mobile/checksend/")
async def check_send(mac_address: MacAddress):
    "文字列が送信されているか確認する"
    mac_addr = mac_address.mac_address
    return {"succeed": Users().is_sending(mac_addr)}


@router.post("/mobile/ranking")
async def ranking(mac_address: MacAddress) -> list[Ranking]:
    "ランキングTOP10を返却する"
    mac_addr = mac_address.mac_address
    return Users().get_ranking(mac_addr)


@router.post("/mobile/me")
async def me(mac_address: MacAddress) -> Ranking:
    "自分の順位とスコアを返却する"
    mac_addr = mac_address.mac_address
    return Users().get_me(mac_addr)


@router.post("/mobile/stop")
async def stop(mac_address: MacAddress):
    "文字列送信を止める"
    mac_addr = mac_address.mac_address
    Users().stop_phrase(mac_addr)
    return {"succeed": True}


@router.post("/mobile/pairing")
async def pairing(pairing_data: Pairing):
    "CatUSBとペアリングする"
    result = Users().pairing(pairing_data.mac_address, pairing_data.phrase)
    return {"succeed": result}
