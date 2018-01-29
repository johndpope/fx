import os

from kazoo.client import KazooClient


def init_default():
    if 'ZkServer' not in os.environ:
        os.environ['ZkServer'] = '172.104.110.189:2181'

    if 'ZkBasePath' not in os.environ:
        os.environ['ZkBasePath'] = 'fx.dev1'

init_default()

zk = KazooClient(hosts=os.environ['ZkServer'])
zk.start()
monitor_path = os.path.join(os.environ['ZkBasePath'], "tasks")


def delete_all_task():
    """
    Xóa tất cả các task
    :return:
    """
    for v in zk.get_children(monitor_path):
        zk.delete(os.path.join(monitor_path, v), recursive=True)
        print('deleted : ' + v)


def upload_task(path=__file__):
    """
    Upload các task
    :return:
    """
    for v in [x for x in os.listdir(os.path.dirname(path)) if x.endswith(".zip")]:
        for l in range(0, 5000):
            with open(v, 'rb') as f:
                full_path = os.path.join(monitor_path, v) + '_' + str(l)
                if zk.exists(full_path):
                    continue
                print('upload:' + full_path)
                zk.create(full_path, f.read(), ephemeral=False, makepath=True)

upload_task()