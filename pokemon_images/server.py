import gridfs
from fastapi import FastAPI
import pymongo
import io
from fastapi.responses import StreamingResponse

server = FastAPI()
MONGO_DETAILS = "mongodb://mongodb:27017/"

mongodb = pymongo.MongoClient(MONGO_DETAILS)


#ditto 132

@server.get("/pokemon_images/{pokemon_name}")
def get_pokemon_image(pokemon_name: str):
    db = mongodb["pokemons"]
    fs = gridfs.GridFS(db)
    file_ids = [file._id for file in fs.find()]
    print("******************************************",file_ids)
    # return StreamingResponse(fs.get(132))
