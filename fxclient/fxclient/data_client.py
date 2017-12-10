import json




def get_data(endpoint):
    import requests

    url = endpoint + "/get_data"

    querystring = {"start": "2017-08-01T10:38:00Z", "end": "2017-08-02T10:38:00Z"}

    payload = ""
    headers = {'content-type': 'application/json'}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    obj = json.loads(response.text)
    return obj

