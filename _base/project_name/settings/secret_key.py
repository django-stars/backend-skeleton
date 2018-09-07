import os
import stat
import string

from django.utils.crypto import get_random_string


def get_secret_key(length):
    """
    keep secret key in file and uniq for each instance
    """
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'secret_key.txt'
    )

    # read if exists
    if os.path.exists(path):
        with open(path, 'r') as fl:
            secret_key = fl.read().strip()

        if len(secret_key) < length:
            raise ValueError(
                'SECRET_KEY too short, should be {} characters'.format(length)
            )

    # generate a new key
    else:
        secret_key = get_random_string(
            length=length,
            allowed_chars=string.printable
        )
        with open(path, 'w') as fl:
            fl.write(secret_key)

    # only owner should have access
    mode = stat.S_IMODE(os.stat(path).st_mode)
    only_owner_mode = mode & ~stat.S_IRWXO & ~stat.S_IRWXG
    if mode != only_owner_mode:
        print('[WARNING] fix SECRET_KEY file permissions')
        os.chmod(path, only_owner_mode)

    return secret_key


SECRET_KEY = get_secret_key(96)
