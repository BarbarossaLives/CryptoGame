from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import os
from data.portfolio import PORTFOLIO
from data.transactions import log_transaction

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/buy", response_class=HTMLResponse)
async def buy_crypto(request: Request, coin: str = Form(...), amount: str = Form(...)):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return templates.TemplateResponse("buy.html", {
            "request": request,
            "message": "Invalid amount. Please enter a positive number."
        })

    headers = {"authorization": f"Apikey {os.getenv('CRYPTOCOMPARE_API_KEY')}"}
    async with httpx.AsyncClient() as client:
        res = await client.get("https://min-api.cryptocompare.com/data/price", params={"fsym": coin, "tsyms": "USD"}, headers=headers)
        data = res.json()
        price = data.get("USD")

    if price is None:
        message = f"Could not fetch price for {coin}."
    elif PORTFOLIO["USD"] >= amount:
        qty = amount / price
        PORTFOLIO[coin] += qty
        PORTFOLIO["USD"] -= amount
        log_transaction(coin, "buy", amount, qty, price)
        message = f"Bought {qty:.6f} {coin} for ${amount:.2f}."
    else:
        message = "Not enough USD to complete the transaction."

    return templates.TemplateResponse("buy.html", {"request": request, "message": message})

@router.post("/sell", response_class=HTMLResponse)
async def sell_crypto(request: Request, coin: str = Form(...), quantity: str = Form(...)):
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        return templates.TemplateResponse("sell.html", {
            "request": request,
            "message": "Invalid quantity. Must be a positive number."
        })

    if PORTFOLIO[coin] < quantity:
        return templates.TemplateResponse("sell.html", {
            "request": request,
            "message": f"Not enough {coin} to sell."
        })

    headers = {"authorization": f"Apikey {os.getenv('CRYPTOCOMPARE_API_KEY')}"}
    async with httpx.AsyncClient() as client:
        res = await client.get("https://min-api.cryptocompare.com/data/price", params={"fsym": coin, "tsyms": "USD"}, headers=headers)
        data = res.json()
        price = data.get("USD")

    if price is None:
        message = f"Could not fetch price for {coin}."
    else:
        amount = quantity * price
        PORTFOLIO[coin] -= quantity
        PORTFOLIO["USD"] += amount
        log_transaction(coin, "sell", amount, quantity, price)
        message = f"Sold {quantity:.6f} {coin} for ${amount:.2f}."

    return templates.TemplateResponse("sell.html", {"request": request, "message": message})