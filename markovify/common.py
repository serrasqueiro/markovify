DEBUG = 0

def dprint(*args, **kwargs):
    if DEBUG <= 0:
        return False
    print(*args, **kwargs)
    return True
