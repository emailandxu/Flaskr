import hashlib

def passwdMd5(data):
    md5_value = data
    if data:
        md5_value = hashlib.md5(data.encode('utf-8')).hexdigest()
    return md5_value