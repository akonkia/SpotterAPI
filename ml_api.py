from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pickle
import DeepImageSearch
import json
from tempfile import NamedTemporaryFile

import sys
import requests

def concatenate_files(input_files, output_file):
    with open(output_file, 'wb') as output:
        for input_file in input_files:
            with open(input_file, 'rb') as f:
                output.write(f.read())

input_files = ['model_chunk_0', 'model_chunk_1', 'model_chunk_2',
               'model_chunk_3','model_chunk_4','model_chunk_5','model_chunk_6',
               'model_chunk_7'] 
output_file = 'prediction_model.sav'  # Name of the concatenated output file

concatenate_files(input_files, output_file)

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
        # st.add_images_to_index([new_image])
        # prediction = st.get_similar_images(new_image, number_of_images=4)
        prediction=image_path
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
    

# import os

# def split_file(input_file, output_prefix, chunk_size):
#     with open(input_file, 'rb') as f:
#         chunk_num = 0
#         while True:
#             chunk = f.read(chunk_size)
#             if not chunk:
#                 break
#             with open(f'{output_prefix}_{chunk_num}', 'wb') as chunk_file:
#                 chunk_file.write(chunk)
#             chunk_num += 1

# input_file = 'prediction_model.sav'  # Replace 'your_input_file.txt' with the path to your input file
# output_prefix = 'model_chunk'  # Output file prefix
# chunk_size = 25 * 1024 * 1024  # 100 MB chunk size

# split_file(input_file, output_prefix, chunk_size)


