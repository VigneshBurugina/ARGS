import hashlib
from sys import argv

if len(argv) == 2:
    x = hashlib.blake2b(argv[1].encode())
    print(x.hexdigest())
else:
    pas = input('Enter String:')
    x = hashlib.blake2b(pas.encode())
    print(x.hexdigest())

