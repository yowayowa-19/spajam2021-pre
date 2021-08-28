from fastapi import APIRouter
from pydantic import BaseModel

from libs.phrase import generate

router = APIRouter()


class MacAddress(BaseModel):
    mac_address: str


@router.post("/hard/sendphrase")
async def send_string(mac_address: MacAddress):
    stopFlag = True #! 停止フラグをmobileからもらってくる
    phrase = generate()
    # 1か0を付与する
    return {"phrase": str(int(stopFlag))+phrase}
