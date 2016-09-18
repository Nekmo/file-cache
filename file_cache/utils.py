import os


def makedirs(path, mode=0o777, exist_ok=False):
    if exist_ok and os.path.exists(path):
        return
    os.makedirs(path, mode)