import requests
import argparse

parser = argparse.ArgumentParser(description='Return a list of most similar images')
parser.add_argument('filename', metavar='file', type=str, nargs='+',
                    help='a filename for parsing')

args = parser.parse_args()

file_path = args.filename[0]

url = 'http://127.0.0.1:8000/image_prediction'

files = {
    'file': open(file_path, 'rb'),
}
    
response = requests.post(url, files=files)
print(response.text)


#usage e.g.: python api_implementation.py '52424_1_MN.jpg'

