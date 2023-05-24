# SSCar Image Search API V1.0
## Technology stack
**FastAPI | MongoDB**
## Description
SSCar Image Search API is an image search provider that can manage image and index searches.
#### The goal is to have image search incorporated easily into any web application.
### Features:
1. Adding listing information and images.
1. Searching by image.
1. Indexing new listing images.
## Requirement
**In our case SSCar A Graduation Project**
1. User can add car information and images.
1. Users can search by image.
## Installation
1. Clone repo
```bash
    git clone https://github.com/medChaabi/sscar-image-search-api.git
```
2. Go into the repo
```bash
    cd sscar-image-search-API
```
3. Setup virtual environment
```bash
    pip install virtualenv # Install virtual environment
    python3 -m venv venv # Create new virtual environment named venv
    source env/bin/activate # Activate venv
    pip install -r requirements.txt # Install SSCar-image-search-API requirements
```
4. Run the developement server
```bash 
    uvicorn main:app --reload
```
5. Start Making This more exciting [Swagger UI](http://127.0.0.1:8000/docs)
```
http://127.0.0.1:8000/docs
```
## Todo Next
-  Optimize performance.
-  Make it a feature that can any site add it.

##


## If You Can Help | If this API helps you ;)
[Email Me](med.chaabi98@gmail.com) <br>
[SSCar Team]()
