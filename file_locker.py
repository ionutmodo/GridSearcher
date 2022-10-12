import os


LOCK_FILE = 'locker.lock'

def lock_acquire():
    while os.path.isfile(LOCK_FILE):
        pass
    open(LOCK_FILE, 'w').close()


def lock_release():
    if os.path.isfile(LOCK_FILE):
        os.remove(LOCK_FILE)
