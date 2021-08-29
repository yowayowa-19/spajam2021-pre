from controller.users import Users
from fastapi import APIRouter
from libs.phrase import generate
from pydantic import BaseModel

router = APIRouter()

COUNT = 0


class MacAddress(BaseModel):
    mac_address: str


@router.post("/hard/sendphrase")
async def send_string(mac_address: MacAddress):
    hard_mac_addr = mac_address.mac_address.replace(":", "")
    # print(f'{hard_mac_addr=}')

    previous_stop_flag = Users().is_sending_h(hard_mac_addr)

    Users().start_phrase(hard_mac_addr)
    stop_flag = Users().is_sending_h(hard_mac_addr)

    # print(previous_stop_flag)
    # print(stop_flag)
    # if previous_stop_flag != stop_flag:
    #     return {"phrase": "0"+phrase}

    # stop_flag = int(not bool(stop_flag))
    # print(f'{stop_flag=}')
    phrase = generate()
    Users().set_phrase_and_score(hard_mac_addr, phrase)

    # stop_flag = stop_flag[0] if isinstance(stop_flag, tuple) else stop_flag
    # print(str(int(stop_flag))+phrase)
    # global COUNT
    # COUNT += 1
    # if COUNT >= 5:
    #     return {"phrase": "0"+phrase}
    # 1か0を付与する

    if previous_stop_flag != stop_flag:
        return {"phrase": "0"+phrase}
    return {"phrase": "1"+phrase}
