from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from routers import default_router
from prices import crypto_price


app = FastAPI(
    title="Off chain service",
    description="",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(default_router)

@app.get("/")
async def root() -> dict:
    return {"message": ""}

@app.on_event("startup")
@repeat_every(seconds=30)
async def fetch_latest_prices() -> None:
    crypto_price.save_latest_price()
