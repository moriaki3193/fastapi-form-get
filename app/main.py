"""FastAPI Form GET
"""
import os
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, FastAPI, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator


STATIC_BASEDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')


router = APIRouter(prefix='/v1')


class ResponseForGetProfit(BaseModel):
    """JSON response schema for `GET /profit`.
    """

    profit: Decimal = Field(..., description='profit = revenue - expense')


@router.get(
    '/profit',
    response_model=ResponseForGetProfit,
    status_code=status.HTTP_200_OK,
)
async def get_profit(
    revenue: Optional[Decimal] = Query(Decimal('0')),
    expense: Optional[Decimal] = Query(Decimal('0')),
) -> JSONResponse:
    """Calculates profit from given income revenue and expense.
    """
    profit = revenue - expense

    content = jsonable_encoder(ResponseForGetProfit(profit=profit))

    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


app = FastAPI(title='FastAPI Form GET', version='1.0.0')

app.include_router(router)
app.mount('', StaticFiles(directory=STATIC_BASEDIR), name='static')
