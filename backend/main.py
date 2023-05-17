from fastapi import FastAPI
from routers import cards, transfers

app = FastAPI()

app.include_router(cards.router)
app.include_router(transfers.router)
