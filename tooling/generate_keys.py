"""
Tooling script to generate RS256 private and public key pairs in Base64 PEM format.
Used for:
- JWT_PRIVATE_KEY_B64 (FastAPI backend signing)
- JWT_PUBLIC_KEY_B64 (Vercel Routing Middleware verification)
"""
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_b64 = base64.b64encode(private_pem).decode('ascii')
    public_b64 = base64.b64encode(public_pem).decode('ascii')

    return private_b64, public_b64

if __name__ == "__main__":
    priv, pub = generate_keys()
    print("=== Generated RS256 Keypair (Base64 PEM) ===")
    print(f"JWT_PRIVATE_KEY_B64={priv}\n")
    print(f"JWT_PUBLIC_KEY_B64={pub}\n")
