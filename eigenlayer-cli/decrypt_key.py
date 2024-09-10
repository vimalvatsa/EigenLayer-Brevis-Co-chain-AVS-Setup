from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import HMAC, SHA256
import json
import base64
import sys

def decrypt_key(json_file, password):
    with open(json_file, 'r') as f:
        key_data = json.load(f)

    # Extract encryption details
    ciphertext = base64.b16decode(key_data['crypto']['ciphertext'].upper())
    iv = base64.b16decode(key_data['crypto']['cipherparams']['iv'].upper())
    salt = base64.b16decode(key_data['crypto']['kdfparams']['salt'].upper())
    kdf_params = key_data['crypto']['kdfparams']
    mac = base64.b16decode(key_data['crypto']['mac'].upper())

    # Define scrypt parameters
    dklen = kdf_params['dklen']
    n = kdf_params['n']
    r = kdf_params['r']
    p = kdf_params['p']

    # Derive key from password
    derived_key = scrypt(password.encode(), salt, dklen, n, r, p)

    # Verify MAC
    mac_check = HMAC.new(derived_key[:16], ciphertext, SHA256).digest()
    if not HMAC.compare_digest(mac_check, mac):
        raise ValueError("MAC check failed")

    # Decrypt the ciphertext
    cipher = AES.new(derived_key[16:32], AES.MODE_CTR, iv=iv)
    decrypted_key = cipher.decrypt(ciphertext)

    return decrypted_key

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 decrypt_key.py <json_file> <password>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    password = sys.argv[2]
    
    try:
        decrypted_key = decrypt_key(json_file, password)
        with open('decrypted_key.pem', 'wb') as f:
            f.write(decrypted_key)
        print("Key decrypted successfully and saved to decrypted_key.pem")
    except Exception as e:
        print(f"Error: {e}")

