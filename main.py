from fastapi import FastAPI
from routes import home, portfolio, history
from dotenv import load_dotenv



load_dotenv()

app = FastAPI()
app.include_router(home.router)
app.include_router(portfolio.router)
app.include_router(history.router)