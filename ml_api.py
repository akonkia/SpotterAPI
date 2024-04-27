from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pickle
import DeepImageSearch
import json
from tempfile import NamedTemporaryFile

import sys
import requests

from zipfile import ZipFile
zf = ZipFile('prediction_model.sav.zip', 'r')
zf.extractall()
zf.close()


app= FastAPI()

class model_input(BaseModel):
    file: UploadFile = File()

import uuid

#load model
st = pickle.load(open('prediction_model.sav', 'rb'))

# @app.post('/image_prediction')
# async def image_pred(file: UploadFile = File()):
#     file.filename = f"{uuid.uuid4()}.jpg"
#     #contents = await file.read()  # <-- Important!
#     new_image = file.filename 
#     st.add_images_to_index([new_image])
#     prediction = st.get_similar_images(new_image, number_of_images=4)
#     return(prediction)

@app.post('/image_prediction')
async def image_pred(file: UploadFile = File(...)):
    file_suffix = "".join(file.filename.partition(".")[1:])
    with NamedTemporaryFile(mode="w+b", suffix=file_suffix) as file_on_disk:
        file_contents = await file.read()
        file_on_disk.write(file_contents)
        image_path = file_on_disk.name
        print(image_path)
        new_image = image_path 
        st.add_images_to_index([new_image])
        prediction = st.get_similar_images(new_image, number_of_images=4)
        print(prediction)
        return(prediction)

# app = FastAPI()


# @app.post("/images/")
# async def create_upload_file(file: UploadFile = File(...)):

#     file.filename = f"{uuid.uuid4()}.jpg"
#     contents = await file.read()  # <-- Important!

#     #db.append(contents)

#     return {"filename": file.filename}



# @app.post("/upload")
# def upload(file: UploadFile = File(...)):
#     try:
#         contents = file.file.read()
#         with open(file.filename, 'wb') as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()

#     return {"message": f"Successfully uploaded {file.filename}"}