# Packages
from fastapi import Form, File, UploadFile, Request, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from typing import List
from pydantic import BaseModel
import uuid
import os
from PIL import Image

#import collection (table from mongodb)
from mongoDB.mongodb import collection

#generate listing id
def get_uuid_id():
    return str(uuid.uuid4())


#app
app = FastAPI()
app.mount("/sscar", StaticFiles(directory="sscar"), name="sscar")

class CarInformation(BaseModel):
    id: str
    name: str
    price : int
    images: List[str]
   

# add new car algo
@app.post("/car")
async def add_new_listing(
    name: str = Form(...),
    price: float = Form(...),
    files: List[UploadFile] = File(...),
    ):
    
    #get new listing data from request
    id = get_uuid_id()

    #upload file to "sscar/cars/{listing id}"
    listingPath = f'sscar/cars/{id}/'
    os.mkdir(listingPath)
    for image in files:
        img = Image.open(image.file)
        path = listingPath+image.filename
        img.save(path)

    #save data to a mongodb database
    newListing = CarInformation(
        id=id,
        name=name,
        price=price, 
        images= [listingPath+file.filename for file in files]
    )
    
    #save to collection
    collection.insert_one(jsonable_encoder(newListing))

    return {
        "Ok! car add to sscar" : newListing,
    }

#search algo
@app.post('/search')
async def search_by_img(image: UploadFile):
    try:
        return {"Your Image":image.filename, "Result":"ok!"}
    except:
        return {"some error here try later!"}

if __name__ == '__main__':
    app.run(debug=True)
