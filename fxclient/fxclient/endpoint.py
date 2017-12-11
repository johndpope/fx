def endpoint(url, method="GET", stream=False):
    def dec(obj):
        obj.endpoint = url
        obj.method = method
        obj.stream = stream
        return obj

    return dec
