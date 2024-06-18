from fastapi import FastAPI
from routes import pokemon_router

server = FastAPI()

server.include_router(pokemon_router.router)