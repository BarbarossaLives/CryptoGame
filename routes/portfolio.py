from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from data.portfolio import PORTFOLIO
from utils.prices import get_prices

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/portfolio", response_class=HTMLResponse)
async def view_portfolio(request: Request):
    coins = list(PORTFOLIO.keys())
    current_prices = get_prices(coins)  # {'BTC': {'USD': 43000}, ...}

    roi_data = {}

    for coin, data in PORTFOLIO.items():
        purchase_price = data["purchase_price"]
        amount = data["amount"]
        current_price = current_prices[coin]["USD"]

        roi = ((current_price - purchase_price) / purchase_price) * 100

        roi_data[coin] = data.copy()
        roi_data[coin]["current_price"] = current_price
        roi_data[coin]["roi"] = roi

    return templates.TemplateResponse("portfolio.html", {
        "request": request,
        "portfolio": PORTFOLIO,
        "roi_data": roi_data
    })
