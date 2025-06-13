from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
import httpx
from fastapi import Form

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Simulated starting balance
portfolio = {
    "USD": 10000.00,
    "BTC": 0.0,
    "ETH": 0.0,
    "SOL": 0.0,
    "ADA": 0.0,
    "XRP": 0.0,
}


@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    url = "https://min-api.cryptocompare.com/data/pricemulti"
    symbols = "BTC,ETH,SOL,ADA"
    target_currency = "USD"
    api_key = os.getenv("CRYPTOCOMPARE_API_KEY")

    headers = {
        "authorization": f"Apikey {api_key}"
    }

    params = {
        "fsyms": symbols,
        "tsyms": target_currency
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        data = response.json()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse("home.html", {
        "request": request,
        "prices": data,
        "timestamp": timestamp
    })

@router.get("/portfolio", response_class=HTMLResponse)
async def view_portfolio(request: Request):
    return templates.TemplateResponse("portfolio.html", {
        "request": request,
        "portfolio": portfolio
    })


@router.get("/buy", response_class=HTMLResponse)
async def buy_form(request: Request):
    return templates.TemplateResponse("buy.html", {"request": request})

@router.post("/buy", response_class=HTMLResponse)
async def buy_crypto(request: Request, coin: str = Form(...), amount: str = Form(...)):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        return templates.TemplateResponse("buy.html", {
            "request": request,
            "message": "Invalid amount. Please enter a positive number."
        })

    # Fetch live price
    url = f"https://min-api.cryptocompare.com/data/price"
    api_key = os.getenv("CRYPTOCOMPARE_API_KEY")

    headers = {
        "authorization": f"Apikey {api_key}"
    }

    params = {
        "fsym": coin,
        "tsyms": "USD"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        price_data = response.json()
        price = price_data.get("USD", None)

    if price is None:
        message = f"Error: Unable to fetch price for {coin}."
    else:
        quantity = amount / price
        if portfolio["USD"] >= amount:
            portfolio[coin] += quantity
            portfolio["USD"] -= amount
            message = f"Bought {quantity:.6f} {coin} for ${amount:.2f}."
        else:
            message = "Error: Not enough USD in portfolio."

    return templates.TemplateResponse("buy.html", {
        "request": request,
        "message": message
    })


@router.get("/sell", response_class=HTMLResponse)
async def sell_form(request: Request):
    return templates.TemplateResponse("sell.html", {"request": request})

@router.post("/sell", response_class=HTMLResponse)
async def sell_crypto(request: Request, coin: str = Form(...), quantity: str = Form(...)):
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
    except ValueError:
        return templates.TemplateResponse("sell.html", {
            "request": request,
            "message": "Invalid quantity. Please enter a positive number."
        })

    # Check if user has enough of the coin
    if portfolio.get(coin, 0.0) < quantity:
        return templates.TemplateResponse("sell.html", {
            "request": request,
            "message": f"Not enough {coin} to sell."
        })

    # Fetch current price
    url = "https://min-api.cryptocompare.com/data/price"
    api_key = os.getenv("CRYPTOCOMPARE_API_KEY")

    headers = {
        "authorization": f"Apikey {api_key}"
    }

    params = {
        "fsym": coin,
        "tsyms": "USD"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        price_data = response.json()
        price = price_data.get("USD", None)

    if price is None:
        message = f"Could not retrieve price for {coin}."
    else:
        usd_amount = quantity * price
        portfolio[coin] -= quantity
        portfolio["USD"] += usd_amount
        message = f"Sold {quantity:.6f} {coin} for ${usd_amount:.2f}."

    return templates.TemplateResponse("sell.html", {
        "request": request,
        "message": message
    })


