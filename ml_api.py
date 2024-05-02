from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pickle
import DeepImageSearch
import json
from tempfile import NamedTemporaryFile
import re
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
import copy 
import shutil

input_files = ['model_chunk_0', 'model_chunk_1', 'model_chunk_2',
               'model_chunk_3','model_chunk_4','model_chunk_5','model_chunk_6',
               'model_chunk_7'] 
output_file = 'prediction_model.sav'  # Name of the concatenated output file
concatenate_files(input_files, output_file)

# Add a route handler for the root path
@app.get('/')
async def root():
    return {"message": "Welcome to the image prediction API fpr SpotterQuest!"}


@app.post('/image_prediction')
async def image_pred(file: UploadFile = File(...)):
    #get the clean index, without newly added features from parsed files
    shutil.copy("./metadata-files/inception_v4.tf_in1k/image_data_features0.pkl","./metadata-files/inception_v4.tf_in1k/image_data_features.pkl")
    shutil.copy("./metadata-files/inception_v4.tf_in1k/image_features_vectors0.idx","./metadata-files/inception_v4.tf_in1k/image_features_vectors.idx")
    fresh = pickle.load(open('prediction_model.sav', 'rb'))
    st = copy.deepcopy(fresh)
    print("Loaded model")
    print("Parsing file...")
    file_suffix = "".join(file.filename.partition(".")[1:])
    with NamedTemporaryFile(mode="w+b", suffix=file_suffix) as file_on_disk:
        file_contents = await file.read()
        file_on_disk.write(file_contents)
        image_path = file_on_disk.name
        new_image = image_path 
        st.add_images_to_index([new_image])
        prediction = st.get_similar_images(new_image, number_of_images=10)
        print(str(prediction))
        integers_list = [int(match.group()) for match in re.finditer(r'\b\d+\b', str(prediction))]
        id_dict = pickle.load(open('id_list.pkl', 'rb'))
        found_ids = []
        # Check each integer in the list
        for integer in integers_list:
            if integer in id_dict:
                found_ids.append(id_dict[integer])

        return(found_ids)

#uvicorn ml_api:app   - use to start the server with api