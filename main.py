# Packages
from fastapi import Form, File, UploadFile, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from typing import List
from pydantic import BaseModel
import uuid
import os
from PIL import Image
from sscar import Search_Setup,Load_Data # Our custom script base on DeepImageSearch library
import json
from bson.json_util import dumps


# Import the MongoDB collection that we will use to store information
from mongoDB.mongodb import collection

#Generate unique ID to identify listing
def get_uuid_id():
    return str(uuid.uuid4())

#APP
app = FastAPI()
app.mount("/sscar", StaticFiles(directory="sscar"), name="sscar")


#Model of the information that we need to store
class CarInformation(BaseModel):
    id: str
    name: str
    price: int
    images: List[str]
   

# Save multiple images into one single folder named with ID
def save_images_into_folder(listing_path,images):
    os.mkdir(listing_path)
    for image in images:
        img = Image.open(image.file)
        path = listing_path+image.filename
        img.save(path)

# Save information and images path in MongoDB
def save_data_to_mongodb(new_listing):    
    collection.insert_one(jsonable_encoder(new_listing))

# Get Data from MongoDB that match id
def get_data_from_mongodb(ids):
    result = collection.find({"id":{"$in":ids}})
    return json.loads(dumps(result))

# Save the query image into a folder
def save_image(image):
    queryImagesPath = f'sscar/query/'
    img = Image.open(image.file)
    path = queryImagesPath+image.filename
    img.save(path)
    return path

# Find cars ids that match the query
def get_similar_result(path,nbr_of_image):
    img_list = st.get_similar_images(image_path=path,number_of_images=nbr_of_image)
    imge_links = [img_list[id] for id in img_list.keys()]
    cars = [car.split('/')[2] for car in imge_links[:-1]]
    cars = list(set(cars))
    return cars

# Setup image search
image_list = Load_Data().from_folder(["sscar/cars/logo"])
st = Search_Setup(image_list=image_list, image_count=2)
st.run_index()

# Add new car Algorithm
@app.post("/car")
async def add_new_listing(
    name: str = Form(...),
    price: float = Form(...),
    images: List[UploadFile] = File(...),
    ):

    # 1 - Generate a unique ID
    id = get_uuid_id()

    # 2 - Generate a path to save new listing images init
    new_listing_path = f'sscar/cars/{id}/'
    
    # 3 - Generate a specific path for each image (this list we save it in Mongodb)
    image_list = [new_listing_path+file.filename for file in images]


    # 4 - Save images into the folder
    save_images_into_folder(new_listing_path,images)
    
    # 5 - Extract features and index images 
    st.add_images_to_index(image_list)

    # 6 - Create an object that we save in Mongodb
    new_listing = CarInformation(
        id=id,
        name=name,
        price=price, 
        images= image_list
    )

    # 7 - Save object into MongoDB
    save_data_to_mongodb(new_listing)

    # 8 - Return the object as a response
    return {
        "Ok! Car add to sscar" : new_listing,
    }

# Search using image algorithm
@app.post('/search')
async def search_by_img(image: UploadFile):
    # 1 - Get and save the query image into the path
    path = save_image(image)
    # 2 - Get cars id that matches query image
    car_ids = get_similar_result(path,3)
    # 3 - Get information using id from Mongodb
    result = get_data_from_mongodb(car_ids)
    # 4 - Return results
    return {"result": result}

if __name__ == '__main__':
    app.run(debug=True)