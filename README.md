# x590schema
A JSON Schema for X.590, the ITU-T standard for a _JSON Signature Scheme (JSS)_.

This version supports ITU-T X.590 (10/2023), which is available from ITU for free at https://www.itu.int/rec/T-REC-X.590-202310-I

## About X.590
From the X.590 Introduction:
> This Recommendation introduces a method for digitally signing data expressed in the JavaScript object notation (JSON) [IETF RFC 8259] notation. For interoperability and security reasons this Recommendation requires JSON objects to be in the I-JSON [IETF RFC 7493] subset and uses the JSON canonicalization scheme (JCS) [IETF RFC 8785] for canonicalization. This method enables signed JSON objects to be kept in JSON format and is referred to as JSON signature scheme (JSS).

Explanation: 
* RFC 8259 is JSON
* RFC 7493 is "I-JSON", a subset of JSON which requires, for example, UTF-8 coding, numbers no larger or more precise than IEEE 754-2008 binary64 (double precision), etc.
* RFC 8785 describes reordering, whitespace handling, etc., to generate a canonical version of the JSON (yielding the ability to have apples-to-apples comparisons of hashs generated across JSON data).

## Usage:

### Option 1:

As a sibling to "properties", add `$ref` to `[location of x590signatures.json]`.  The `$ref`  will expand to an array of X.590 signature objects, see the example below.

    {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "example-subschema.json",
        "title": "JSS Schema Sample Usage",
        "properties": {
            "name": {
                "type": "object",
                "properties": {
                    "first": {
                        "type": "string",
                        "$comment": "First name of the person"
                    },
                    "last": {
                        "type": "string",
                        "$comment": "Last name of the person"
                    }
                },
                "required": [ "first", "last" ]
            }
        },
        "$ref": "x590signatures.json",
        "required": [ "name" ]
    }

Then, `signatures` are added in instances like this:

    {
        "name": {
            "first": "John",
            "last": "Doe"
        },
        "signatures": [
            {
                "hash_algorithm": "sha-256",
                "algorithm": "Ed25519",
                "public_key": "MCowBQYDK2VwAyEAubMonBfU9pvIbj5RCiWQLD45Jvu6mKr+kQXjvjW8ZkU",
                "value": "CoRbqNeXGLWZ5q3c8KxSdKKbjuMUXzOUI_9ZHSL9qalZbbdEyVse4EURUtE_TaubCAMCPZIKTCEpvGGjwz1nBg"
            }
        ]
    }


Note that multiple signatures can be attached (via the array), and signatures can be signed as well.  See X.590 for details.

### Option 2: 

Instead of using `x509signatures.json` to insert properties/signatures/array of signatures, do it directly in the source code:

    {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "example-subschema.json",
        "title": "JSS Schema Sample Usage",
        "properties": {
            "name": {
                "type": "object",
                "properties": {
                    "first": {
                        "type": "string",
                        "$comment": "First name of the person"
                    },
                    "last": {
                        "type": "string",
                        "$comment": "Last name of the person"
                    }
                },
                "required": [ "first", "last" ]
            },
            "signatures": {
                "type": "array",
                "items": {
                    "$ref": "x590schema.json"
                }
            }
        },
        "required": [ "name" ]
    }

And signatures are added in the same manner as Option 1.