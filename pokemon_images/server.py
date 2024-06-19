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
            return HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        return (HTTPException(status_code=500, detail=str(e)))


@server.post("/pokemon_images/{pokemon_name}")
async def add_pokemon_image(pokemon_name: str):
    try:
        db = mongodb["pokemons"]
        fs = gridfs.GridFS(db)

        info_response = requests.get(f'http://pokemon_container:8001/pokemons/{pokemon_name}')
        info_json = info_response.json()
        id = info_json[0]
        if fs.exists({"_id": id}):
            return {"message": "Image already exists"}

        image_response = await get_pokemon_image(id)

        if image_response.status_code == 404:
            image = requests.get(f'http://api_service:8003/pokemon_api/images/{id}')
            if image.status_code == 200:
                fs.put(image.content, _id=id)
                return {"message": "Image added successfully"}
            else:
                raise HTTPException(status_code=image.status_code, detail="Failed to fetch image from external service")

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

