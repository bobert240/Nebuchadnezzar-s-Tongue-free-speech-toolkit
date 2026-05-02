#!/usr/bin/env python3
"""
Simple Nebuchadnezzar’s Tongue encoder.
Takes a natural language message, a codebook, and outputs JSON.
"""

import json
import sys
import re

def load_codebook(path):
    with open(path, 'r') as f:
        return json.load(f)

def find_best_template(message, codebook):
    # Very simple: return first matching code where the message contains the template's idea
    # For production, use a small LLM or manual selection.
    for code, template in codebook.get("codes", {}).items():
        # Extract slot placeholders
        placeholders = re.findall(r'\{([^}]+)\}', template)
        # crude check: if any word matches a slot name? Not robust
        if placeholders:
            # try to extract values
            slots = {}
            for p in placeholders:
                # find a word that might be the value (e.g., a proper noun)
                words = re.findall(r'\b[A-Z][a-z]+\b', message)
                if words:
                    slots[p] = words[0]
                else:
                    slots[p] = "unknown"
            return code, slots
    return None, {}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python encoder_simple.py <codebook.json> '<message>'")
        sys.exit(1)
    codebook_path = sys.argv[1]
    message = sys.argv[2]
    codebook = load_codebook(codebook_path)
    code, slots = find_best_template(message, codebook)
    encoded = {"code": code, "slots": slots, "metadata": {"source": "simple_encoder"}}
    print(json.dumps(encoded, indent=2))