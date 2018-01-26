import os

from kazoo.client import KazooClient

os.environ['ZkServer'] = '172.104.110.189:2181'
os.environ['ZkBasePath'] = 'fx.dev'

zk = KazooClient(hosts=os.environ['ZkServer'])
zk.start()
monitor_path = os.path.join(os.environ['ZkBasePath'], "tasks")

for v in [x for x in os.listdir(os.path.dirname(__file__)) if x.endswith(".zip")]:
    for l in range(0,200):
        with open(v, 'rb') as f:
            full_path = os.path.join(monitor_path, v) + '_' + str(l)
            if zk.exists(full_path):
                continue
            print('upload:' + full_path)
            zk.create(full_path, f.read(), ephemeral=False, makepath=True)
