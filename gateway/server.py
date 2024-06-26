from fastapi import FastAPI
from routes import pokemon_router,trainer_router

server = FastAPI()

server.include_router(pokemon_router.router)
server.include_router(trainer_router.router)
