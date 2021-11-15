from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from prices import crypto_price


default_router = APIRouter(
    prefix='',
    tags=[''],
    responses={404: {'description': 'Not Found'}},
)


@default_router.get('/latest')
def get_latest_prices() -> JSONResponse:
    return JSONResponse(content=crypto_price.get_latest_price(), status_code=status.HTTP_200_OK)
