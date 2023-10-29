import secrets
secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal secret key
print(secret_key)
