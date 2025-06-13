from fastapi import FastAPI
from routes import home
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(home.router)
