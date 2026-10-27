"""
Generate RSA-2048 keypair encoded in Base64 for SST Study Platform RS256 JWT auth.
Outputs private and public key values ready to paste into .env.
"""
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys() -> tuple[str, str]:
    """Generates an ephemeral RSA-2048 keypair returned as Base64-encoded strings."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    
    priv_b64 = base64.b64encode(private_pem).decode("ascii")
    pub_b64 = base64.b64encode(public_pem).decode("ascii")
    return priv_b64, pub_b64

def generate_keypair():
    priv_b64, pub_b64 = generate_keys()
    print("\n=== GENERATED RS256 KEYPAIR ===")
    print("\nJWT_PRIVATE_KEY_B64=" + priv_b64)
    print("\nJWT_PUBLIC_KEY_B64=" + pub_b64)
    print("\nCopy the above variables to your .env file or Vercel Environment Variables.")

if __name__ == "__main__":
    generate_keypair()
