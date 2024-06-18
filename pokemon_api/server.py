from fastapi import FastAPI
from routes import images_router
server = FastAPI()

server.include_router(images_router.router)
