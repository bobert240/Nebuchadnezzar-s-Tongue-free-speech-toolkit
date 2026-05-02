#!/usr/bin/env python3
"""
Batch runner for Logos‑Lens – processes multiple text files or chunks.
"""

import argparse
import json
import requests
import sys
from pathlib import Path

SYSTEM_PROMPT = open("logos_lens_system_prompt.txt").read()  # or embed

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
    parser.add_argument("--input_dir", help="Directory of .txt files")
    parser.add_argument("--input_file", help="Single file")
    parser.add_argument("--output", default="logos_results.json")
    parser.add_argument("--api_url", default="https://api.deepseek.com/v1/chat/completions")
    parser.add_argument("--api_key", required=True)
    parser.add_argument("--model", default="deepseek-chat")
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    files = []
    if args.input_dir:
        files = list(Path(args.input_dir).glob("*.txt"))
    elif args.input_file:
        files = [Path(args.input_file)]

    results = []
    for f in files:
        text = f.read_text(encoding='utf-8')
        if args.dry_run:
            print(f"DRY RUN: {f.name} ({len(text)} chars)")
            continue
        output = call_api(text, args.api_url, args.api_key, args.model)
        results.append({"file": str(f), "analysis": json.loads(output)})

    if not args.dry_run:
        with open(args.output, 'w') as out:
            json.dump(results, out, indent=2)
        print(f"Saved to {args.output}")

if __name__ == "__main__":
    main()