import requests

response = requests.get('http://localhost:9000/data_stream', stream=True)
for chunk in response.iter_lines():
    if chunk:
        print(chunk)
