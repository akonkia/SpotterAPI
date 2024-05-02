
This is an API for finding the most similar images from the database of SpotterQuest to an image being newly uploaded.

See Jupyter notebook for a visual example of the process of finding similar images.

Use requirements file to build the environment.

File ml_api.py contains all elements to run a fastapi server. Start the server with: uvicorn ml_api:app

File api_implementation.py takes in a filename (path) as argument and send it to the uvicorn service.

Model for inference could not be uploaded to the repository due to size limit. Therefore, it was cut into parts and is re-created with ml_api.py. 

For simplicity, the resulting model file can be accessed directly and the steps to concatenate removed.

Checking for similar images requires a new image is added to the index. To avoid problems arising with time, e.g. multiple queries adding the same image to index, a fresh copy of the model and index is loaded before inference.
