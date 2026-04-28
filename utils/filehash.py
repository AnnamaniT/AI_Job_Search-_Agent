# file_hash.py ################################
import hashlib

def get_file_hash(file_path: str) -> str:
    hasher = hashlib.md5()

    with open(file_path, "rb") as f:
        hasher.update(f.read())

    return hasher.hexdigest()


