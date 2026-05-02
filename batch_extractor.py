#!/usr/bin/env python3
"""
Batch extractor using Hardened SEA‑Freespeak.
Processes multiple files and outputs structured components.
"""

import argparse
import json
import requests
from pathlib import Path

SYSTEM_PROMPT = open("hardened_sea_freespeak_system_prompt.txt").read()

def call_api(text, api_url, api_key, model):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.0
    }
    resp = requests.post(api_url, json=payload, headers=headers)
    return resp.json()["choices"][0]["message"]["content"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output", default="extracted.json")
    parser.add_argument("--api_url", default="https://api.deepseek.com/v1/chat/completions")
    parser.add_argument("--api_key", required=True)
    parser.add_argument("--model", default="deepseek-chat")
    args = parser.parse_args()

    results = []
    for f in Path(args.input_dir).glob("*.txt"):
        text = f.read_text(encoding='utf-8')
        output = call_api(text, args.api_url, args.api_key, args.model)
        results.append({"file": str(f), "extracted": json.loads(output)})

    with open(args.output, 'w') as out:
        json.dump(results, out, indent=2)

if __name__ == "__main__":
    main()