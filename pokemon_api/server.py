from fastapi import FastAPI
from routes import images_router,pokemon_router
server = FastAPI()

server.include_router(images_router.router)
server.include_router(pokemon_router.router)