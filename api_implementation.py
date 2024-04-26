import json
import requests

url = 'http://127.0.0.1:8000/image_prediction'

files = {
    'file': open(r'52424_1_MN.jpg', 'rb'),
}

response = requests.post(url, files=files)
print(response)