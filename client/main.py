import requests

url = "http://127.0.0.1:8000/uploadfile/"
file_path = "test.txt"
with open(file_path, 'rb') as f:
    files = {'file': ('test.txt', f, 'text/plain')}
    response = requests.post(url, files=files)
    print(response.json())