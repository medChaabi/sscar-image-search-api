# Packages
from fastapi import Form, File, UploadFile, Request, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from typing import List
from pydantic import BaseModel
import uuid
import os
from PIL import Image
from DeepImageSearch import SearchImage
import json
from bson.json_util import dumps


#to use collection from mongodb
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
    images: List[UploadFile] = File(...),
    ):

    #get new listing data from request
    id = get_uuid_id()

    #save images into folder
    listing_path = f'sscar/cars/{id}/'
    save_images_into_folder(listing_path,images)

    #new object
    new_listing = CarInformation(
        id=id,
        name=name,
        price=price, 
        images= [listing_path+file.filename for file in images]
    )
    #save new object to collection
    save_data_to_mongodb(new_listing)

    return {
        "Ok! car add to sscar" : new_listing,
    }

#search algo
@app.post('/search')
async def search_by_img(image: UploadFile):
    #save image
    path = save_image(image)
    #get similar image ids
    car_ids=get_similar_result(path,10)
    #get cars information from mongodb
    result = get_data_from_mongodb(car_ids)
    print(result)
    return {"result":result}
    
##functions
def save_images_into_folder(listing_path,images):
    os.mkdir(listing_path)
    for image in images:
        img = Image.open(image.file)
        path = listing_path+image.filename
        img.save(path)
    # indexing listing

def save_data_to_mongodb(new_listing):    
    collection.insert_one(jsonable_encoder(new_listing))

def save_image(image):
    queryImagesPath = f'sscar/query/'
    img = Image.open(image.file)
    path = queryImagesPath+image.filename
    img.save(path)
    return path

def get_similar_result(path,nbr_of_image):
    img_list = SearchImage().get_similar_images(image_path=path,number_of_images=nbr_of_image)
    imge_links = [img_list[id] for id in img_list.keys()]
    cars = [car.split('/')[2] for car in imge_links]
    cars = list(set(cars)) #remove duplicate ids
    return cars

def get_data_from_mongodb(ids):
    result = collection.find({"id":{"$in":ids}})
    return json.loads(dumps(result))

if __name__ == '__main__':
    app.run(debug=True)
