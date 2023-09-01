import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def is_password_match(entered_password, stored_hash):
    
    entered_hash = hashlib.md5(entered_password.encode()).hexdigest()

    return entered_hash == stored_hash