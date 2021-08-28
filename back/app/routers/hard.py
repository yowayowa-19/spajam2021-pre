from app.controller.users import Users
from fastapi import APIRouter
from libs.phrase import generate
from pydantic import BaseModel

router = APIRouter()


class MacAddress(BaseModel):
    mac_address: str


@router.post("/hard/sendphrase")
async def send_string(mac_address: MacAddress):
    stopFlag = Users().is_sending(mac_address)
    phrase = generate()
    # 1か0を付与する
    return {"phrase": str(int(stopFlag))+phrase}
