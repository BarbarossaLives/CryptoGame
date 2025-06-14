from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.transactions import get_transaction_history

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    transactions = get_transaction_history()
    return templates.TemplateResponse("history.html", {
        "request": request,
        "transactions": transactions
    })
