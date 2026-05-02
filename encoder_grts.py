#!/usr/bin/env python3
"""
GRTS + Nebuchadnezzar’s Tongue Encoder
Encodes GRTS function calls or arbitrary messages into neutral JSON using a codebook.
"""

import json
import sys
from pathlib import Path

DEFAULT_CODEBOOK = {
    "version": "1.0",
    "name": "GRTS + Nebuchadnezzar’s Tongue",
    "codes": {
        "γ": "gc_consciousness",
        "Ψ": "alienation_idx",
        "Rθ": "rev_potential",
        "δ": "stochastic_leap_mag"
    },
    "templates": {
        "simulate_consciousness": {
            "code": "sim_cons",
            "slots": ["γ0", "Ψ", "t_max", "events"]
        },
        "vanguard_leap": {
            "code": "van_leap",
            "slots": ["vanguard_factor", "event_magnitude"]
        }
    }
}

def load_codebook(path=None):
    if path and Path(path).exists():
        with open(path, 'r') as f:
            return json.load(f)
    return DEFAULT_CODEBOOK

def encode_function(function_name, params, codebook=None, metadata=None):
    cb = load_codebook(codebook)
    template = cb.get("templates", {}).get(function_name)
    if not template:
        raise ValueError(f"Unknown function: {function_name}")
    required = set(template["slots"])
    provided = set(params.keys())
    if not required.issubset(provided):
        missing = required - provided
        raise ValueError(f"Missing slots: {missing}")
    encoded = {
        "code": template["code"],
        "slots": {k: params[k] for k in template["slots"]},
        "metadata": metadata or {"source": "grts_encoder", "timestamp": "2025-08-11T20:00:00Z"}
    }
    return encoded

if __name__ == "__main__":
    # Example
    params = {"γ0": 0.48, "Ψ": 0.93, "t_max": 6, "events": [(0,0.18),(3,0.22)]}
    encoded = encode_function("simulate_consciousness", params)
    print(json.dumps(encoded, indent=2))