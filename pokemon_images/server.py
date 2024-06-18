import io
import gridfs
import requests
from fastapi import FastAPI, HTTPException
import pymongo
from fastapi.responses import StreamingResponse

server = FastAPI()
MONGO_DETAILS = "mongodb://mongodb_container:27017/"  # Ensure this matches your Docker Compose configuration

mongodb = pymongo.MongoClient(MONGO_DETAILS)


@server.get("/pokemon_images/{id}")
async def get_pokemon_image(id: int):
    try:
        db = mongodb["pokemons"]
        fs = gridfs.GridFS(db)
        file_object = fs.find_one({"_id": id})
        if file_object:
            file_content = file_object.read()
            return StreamingResponse(io.BytesIO(file_content), media_type="image/png")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@server.post("/pokemon_images/{id}")
async def add_pokemon_image(id: int):
    try:
        db = mongodb["pokemons"]
        fs = gridfs.GridFS(db)
        file_object = fs.find_one({"_id": id})
        if not file_object:
            image = requests.get(f'http://api_service:8003/pokemon_images/{id}')
            fs.put(image.content, _id=id)
            return {"message": "Image added successfully"}
        raise HTTPException(status_code=409, detail="Image already exists")
    except HTTPException as e:
        return e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
