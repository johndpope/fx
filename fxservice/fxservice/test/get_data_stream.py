import requests

start = '2017-08-01T10-38-00Z'
end = '2017-09-02T10-38-00Z'
chunk_size = '4'

url = 'http://localhost:9000/get_data_stream?chunk={2}&start={0}&end={1}'.format(start, end, chunk_size)
response = requests.get(url, stream=True)
for chunk in response.iter_lines():
    if chunk:
        print(chunk)
