from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class MacAddress(BaseModel):
    mac_address: str


@router.post("/hard/sendstring")
async def send_string(self):
    return {"string": "1nyarn"}