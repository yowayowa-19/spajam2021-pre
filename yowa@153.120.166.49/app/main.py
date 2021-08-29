from controller.hard_devices import HardDevices
from fastapi import FastAPI
import uvicorn

from routers import hard, mobile

app = FastAPI()

app.include_router(mobile.router)
app.include_router(hard.router)


@app.get('/')
async def ping():
    return {"ping": "pong"}


if __name__ == '__main__':
    HardDevices()
    uvicorn.run(app, host="0.0.0.0", port=8000)
