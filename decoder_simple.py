#!/usr/bin/env python3
"""
Simple Nebuchadnezzar’s Tongue decoder.
Expands JSON into full message.
"""

import json
import sys

def load_codebook(path):
    with open(path, 'r') as f:
        return json.load(f)

def decode(encoded_json, codebook):
    if isinstance(encoded_json, str):
        encoded = json.loads(encoded_json)
    else:
        encoded = encoded_json
    code = encoded["code"]
    slots = encoded.get("slots", {})
    template = codebook["codes"].get(code)
    if not template:
        return f"[Unknown code: {code}]"
    result = template
    for key, value in slots.items():
        result = result.replace(f"{{{key}}}", value)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python decoder_simple.py <codebook.json> <encoded.json>")
        sys.exit(1)
    codebook = load_codebook(sys.argv[1])
    with open(sys.argv[2], 'r') as f:
        encoded = json.load(f)
    print(decode(encoded, codebook))