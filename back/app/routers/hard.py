from controller.users import Users
from fastapi import APIRouter
from libs.phrase import generate
from pydantic import BaseModel

router = APIRouter()


class MacAddress(BaseModel):
    mac_address: str


@router.post("/hard/sendphrase")
async def send_string(mac_address: MacAddress):
    hard_mac_addr = mac_address.mac_address.replace(":", "")
    previous_stop_flag = Users().is_sending_h(hard_mac_addr)

    Users().start_phrase(hard_mac_addr)
    stop_flag = Users().is_sending_h(hard_mac_addr)
    phrase = generate()
    Users().set_phrase_and_score(hard_mac_addr, phrase)

    if previous_stop_flag != stop_flag:
        return {"phrase": "0"+phrase}
    return {"phrase": "1"+phrase}
