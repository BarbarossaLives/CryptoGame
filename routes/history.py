from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/history", response_class=HTMLResponse)
async def view_history(request: Request):
    transactions_file = "data/transactions.json"
    
    if os.path.exists(transactions_file):
        with open(transactions_file, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history
    })
