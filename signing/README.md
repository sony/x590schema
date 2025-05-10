# Example X.590 (JSS) signing code

Sign using X.590 JSS, using example Ed25519 private key from the standard (details follow):

Requirements:
 1. canonicaljson - `pip install canonicaljson`
 2. cryptography - `pip install cryptography`

Restrictions:
 1. There may be zero or one signature objects in the input JSON
 2. The signature (if present) must be at the outermost level of the JSON object
 3. The X.590 example public/private key pair is hard-coded.

 This is a PEM holding a Ed25519 public key.

    -----BEGIN PUBLIC KEY-----
    MCowBQYDK2VwAyEAubMonBfU9pvIbj5RCiWQLD45Jvu6mKr+kQXjvjW8ZkU=
    -----END PUBLIC KEY-----
 
 
 This is a PEM holding a Ed25519 private key.
 
    -----BEGIN PRIVATE KEY-----
    MC4CAQAwBQYDK2VwBCIEIDnZ5bPmXnB3OfU/5fNVfxfr7iRZtqH06AZ3b6c6liTL
    -----END PRIVATE KEY-----
