import rsa

public_key, private_key = rsa.newkeys(512)


def encrypt(password):  # For encryption password
    return rsa.encrypt(password.encode(), public_key)


def decrypt(encrypt_password):  # For decryption password
    return rsa.decrypt(encrypt_password, private_key).decode()
