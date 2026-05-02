#!/usr/bin/env python3
"""
GRTS + Nebuchadnezzar’s Tongue Decoder
Decodes neutral JSON back to function name and parameters.
"""

import json
import sys
from pathlib import Path

DEFAULT_CODEBOOK = {
    "version": "1.0",
    "name": "GRTS + Nebuchadnezzar’s Tongue",
    "templates": {
        "simulate_consciousness": {"code": "sim_cons", "slots": ["γ0", "Ψ", "t_max", "events"]},
        "vanguard_leap": {"code": "van_leap", "slots": ["vanguard_factor", "event_magnitude"]}
    }
}

def load_codebook(path=None):
    if path and Path(path).exists():
        with open(path, 'r') as f:
            return json.load(f)
    return DEFAULT_CODEBOOK

def decode(encoded_json, codebook=None):
    cb = load_codebook(codebook)
    if isinstance(encoded_json, str):
        encoded = json.loads(encoded_json)
    else:
        encoded = encoded_json
    code = encoded.get("code")
    slots = encoded.get("slots", {})
    function_name = None
    for name, tmpl in cb.get("templates", {}).items():
        if tmpl.get("code") == code:
            function_name = name
            break
    if not function_name:
        raise ValueError(f"Unknown code: {code}")
    required = cb["templates"][function_name]["slots"]
    params = {slot: slots.get(slot) for slot in required}
    return function_name, params

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        encoded = json.load(f)
    func, params = decode(encoded)
    print(f"Function: {func}\nParameters: {params}")