from DeepImageSearch import Index, LoadData
import os

## we will run this one in 3 day of 4 to make update in ower data base

folder = 'static/cars/'
def default():
    listOfDir=list()
    for car in os.listdir(folder):
        listOfDir.append(folder+car)
    imge_list = LoadData().from_folder(listOfDir)
    Index(imge_list).Start()
    # print(listOfDir)

default()