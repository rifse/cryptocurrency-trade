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

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ct, tag).decode('utf-8').split('\n')[line_number].split(' ')

    # return [part for part in data]
    return list(data)

def encrypt(file_out_name, file_in_name):

    with open(file_in_name, 'r') as file_in:
        data = file_in.read().encode('utf-8')

    key = getpass.getpass('Choose password:').encode('utf-8')
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    with open(file_out_name, 'wb') as file_out:
        [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]


if __name__ == '__main__':
    ff = decrypt('_j.bin', 2)
    print(ff)
