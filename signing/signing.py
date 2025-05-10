
# Sign using X.590 JSS, using example Ed25519 private key from the standard (details follow):
#
# Restrictions:
# 1. There may be zero or one signature object in the input JSON
# 2. The signature (if present) must be at the outermost level of the JSON object
#
#   Appendix II 
# Ed25519 keys for examples
# (This appendix does not form an integral part of this Recommendation.)
# 
# This appendix contains the public and private keys that are used in the various examples in this Recommendation and are included here to assist with replication, testing, and verification.
# NOTE – The following keys use the Ed25519 algorithm for illustrative purposes. Implementations SHOULD use quantum safe options.
# II.1 Ed25519 public key
# This is a PEM holding a Ed25519 public key.
# -----BEGIN PUBLIC KEY-----
# MCowBQYDK2VwAyEAubMonBfU9pvIbj5RCiWQLD45Jvu6mKr+kQXjvjW8ZkU=
# -----END PUBLIC KEY-----
# 
# II.2 Ed25519 private key
# This is a PEM holding a Ed25519 private key.
# -----BEGIN PRIVATE KEY-----
# MC4CAQAwBQYDK2VwBCIEIDnZ5bPmXnB3OfU/5fNVfxfr7iRZtqH06AZ3b6c6liTL
# -----END PRIVATE KEY-----


import json
import argparse
import sys
import canonicaljson
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import base64


def print_json_fields(data, prefix=""):
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            print_json_fields(value, new_prefix)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_prefix = f"{prefix}[{index}]"
            print_json_fields(item, new_prefix)
    else:
        print(f"{prefix}: {data}")

def find_key(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        for k, v in data.items():
            result = find_key(v, key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, key)
            if result is not None:
                return result
    return None

def add_obj_to_field(obj, field, value_obj):
    if not isinstance(obj, dict):
        return
    if field not in obj or not isinstance(obj[field], list):
        obj[field] = []
    obj[field].append(value_obj)

def main():
    parser = argparse.ArgumentParser(description="Add a field to a JSON file or stream.")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file path or '-' for stdin")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file path or '-' for stdout")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print each field and value in the JSON")

    args = parser.parse_args()

    # Verbose output
    if args.verbose:
        print("Verbose mode enabled.")

    # Verbose output
    if args.verbose:
        print(f"Input file: {args.input}")
        print(f"Output file: {args.output}")
        print()

    # Read JSON from file or stdin
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        with open(args.input, 'r') as infile:
            data = json.load(infile)

    # Verbose output
    if args.verbose:
        print("(Input) Verbose JSON field listing:")
        print_json_fields(data)
        print()

    signatures = find_key(data, "signatures")
    cnt = len(signatures) if signatures is not None else 0

    if args.verbose:
        print(f"Number of signature objects: {cnt}")
        print()

    if cnt != 0 and cnt != 1:
        print("Error: Expected exactly one signature object.")
        sys.exit(1)

    # Check if the signatures already exists, remove it if it does
    sig = find_key(data, "signatures") 
    if sig is not None:
        savedsig = data.pop("signatures")
    else:
        savedsig = None
    if args.verbose:
        print(f"Signature found: {sig}")
        print(f"Signature removed: {savedsig}")
        print()

    # add  new signature object
    newsig = {
        "hash_algorithm": "sha-256",
        "algorithm": "Ed25519",
        "public_key": "MCowBQYDK2VwAyEAubMonBfU9pvIbj5RCiWQLD45Jvu6mKr+kQXjvjW8ZkU"
    }
    if args.verbose:
        print(f"Adding new signature: {newsig}")
        print()
    
    # Add the new signature object to the field
    add_obj_to_field(data, "signatures", newsig)
    if args.verbose:
        print(f"New signature parameters added: {newsig}")
        print()
        print_json_fields(data)
        print()
    

    # Canonicalize JSON
    #print(canonicaljson.encode_canonical_json(json.load(sys.stdin)).decode());
    Cdata = canonicaljson.encode_canonical_json(data).decode()

    # Verbose output
    if args.verbose:
        print("\n(Canonical) Verbose JSON:")
        print(Cdata)
        print()


    # Calculate the hash of the canonicalized JSON
    hash_value = hashlib.sha256(Cdata.encode()).hexdigest()   

    # Verbose output
    if args.verbose:
        print(f"Hash of canonicalized JSON: {hash_value}")
        print()

    # Your PKCS#8 PEM-encoded private key
    pem = b"""-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIDnZ5bPmXnB3OfU/5fNVfxfr7iRZtqH06AZ3b6c6liTL
-----END PRIVATE KEY-----"""

    # Load the private key
    private_key = serialization.load_pem_private_key(pem, password=None)

    # Sign the hash value using Ed25519    
    message = hash_value.encode('ascii')
    signature = private_key.sign(message)

    # Verbose output
    if args.verbose:
        print("\nEd25519 Signature:")
        print(f"b64: ", base64.b64encode(signature).decode('utf-8').replace("=", ""))
        print()

    # Add singature value to signature field
    newsig = {"value": base64.b64encode(signature).decode('utf-8').replace("=", "")} 
    if args.verbose:
        print(f"New signature value: {newsig}")
        print()

    # add signature value to the first signature object
    data["signatures"][0]["value"] = base64.urlsafe_b64encode(signature).decode('utf-8').replace("=", "")

    # Verbose output
    if args.verbose:
        print("\n(Output) Verbose JSON field listing:")
        print_json_fields(data)
        print()

    # Write JSON to file or stdout
    if args.output == "-":
        json.dump(data, sys.stdout, indent=4)
        sys.stdout.write('\n')
    else:
        with open(args.output, 'w') as outfile:
            json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    main()