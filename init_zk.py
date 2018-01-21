import json

from kazoo.client import KazooClient

zk = KazooClient(hosts='172.104.110.189:2181')
zk.start()

root_path = "fx1.dev"


def set(path, data):
    if zk.exists(path):
        zk.delete(path)
    zk.create(path, json.dumps(data, indent=4).encode(), makepath=True)


set('/{}/fxservice'.format(root_path),
    {
        "OandaKey": "5155f61a12f50401aed005d121b524f3-b9a736e4104e81e450556ad1345520c1",
        "DbHost": "influxdb",
        "DbPort": "8086",
        "DbUser": "root",
        "DbPass": "root",
        "DbName": "ticks"
    })
set('/{}/crawler'.format(root_path),
    {
        "OandaKey": "c59ac783885ec75d0b147e730f820997-17fc99e689f2edb65ecb07060a914e71",
        "AccountId": "101-011-6388580-001",
        "DataService": "http://fxservice:9000",
        "BatchSize": "5000",
        "DelayTime": 10
    })
