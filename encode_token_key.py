import base64

def xor_encrypt_decrypt(data, key="my_secret_key"):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

# Your GitHub token
original_token = input("Enter Token>> ")

# Encrypt and encode in Base64
encrypted_token = xor_encrypt_decrypt(original_token)
encoded_token = base64.b64encode(encrypted_token.encode()).decode()

print(f"Encrypted Token: {encoded_token}")  # Save this for later use
