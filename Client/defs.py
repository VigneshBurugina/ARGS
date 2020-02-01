import os


cwd = os.getcwd()


def msg(a):
    """Converts binary message data to string"""
    return str(a)[2:-1]


def str_to_list(ex):
    """Converts binary list data to list"""
    ex = ex[1:-1].split(",")
    for i in range(len(ex)):
        ex[i] = ex[i].replace("'", "", 2)
        ex[i] = ex[i].replace(" ", "", 1)
    return ex


def first_check():
    """Performs startup checks"""
    if 'config.vf' not in os.listdir(cwd):
        return -1
    return
