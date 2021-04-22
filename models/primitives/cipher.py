"""Docstring."""
import getpass
import os
from Crypto.Cipher import AES


def decrypt(encrypted_file, line_number):  # encrypted_file is a path and must be relative (start with ../ 
    """Expects passwdir a file of format: 

        str_11 ... str_n1 newline
        ...
        str_m1 ... str_nm 

    Outputs: [str_1i, ..., str_ni]
        """

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, encrypted_file)
    key = getpass.getpass('Password:').encode('utf-8')

    with open(file_path, 'rb') as f:
        nonce, tag, ct = [f.read(x) for x in (16, 16, -1)]
    # file_in = open(passwdir, "rb")
    # try:
    #     nonce, tag, ct = [file_in.read(x) for x in (16, 16, -1)]
    # finally:
    #     file_in.close()

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ct, tag).decode('utf-8').split('\n')[line_number].split(' ')

    return (part for part in data)


if __name__ == '__main__':
    pass
