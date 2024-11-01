from fastapi import FastAPI
from .api import routes

app = FastAPI()

# Connect routes
app.include_router(routes.router)