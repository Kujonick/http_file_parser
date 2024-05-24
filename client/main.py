import requests

url = "http://127.0.0.1:8000/uploadfile/"
file_path = "test.txt"
with open(file_path, 'rb') as f:
    files = {'file': ('test.txt', f, 'text/plain')}
    response = requests.post(url, files=files)
    response = response.json()

    for k, v in response.items():
        print(k, end = ' ')
        if isinstance(v, dict):
            print('')
            for key, value in v.items():
                print('   ', key , value)
        else:
            print(v)
        