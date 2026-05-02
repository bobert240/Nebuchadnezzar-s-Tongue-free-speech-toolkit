#!/usr/bin/env python3
"""
Generates a codebook from a list of concepts using a local LLM (Ollama).
"""

import argparse
import json
import requests
import sys

def query_ollama(prompt, model="llama3.2:1b"):
    resp = requests.post("http://localhost:11434/api/generate",
                         json={"model": model, "prompt": prompt, "stream": False})
    return resp.json()["response"].strip()

def generate_template(concept, slots, model):
    slots_str = ", ".join([f"{{{s}}}" for s in slots]) if slots else "none"
    prompt = f"Write a short image prompt (max 20 words) for: {concept}. Use slots: {slots_str}. Output only the prompt."
    return query_ollama(prompt, model)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concepts", required=True, help="File with one concept per line, optionally 'concept|slot1,slot2'")
    parser.add_argument("--output", default="codebook.json")
    parser.add_argument("--model", default="llama3.2:1b")
    args = parser.parse_args()

    entries = []
    with open(args.concepts) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if '|' in line:
                concept, slots_str = line.split('|', 1)
                slots = [s.strip() for s in slots_str.split(',')]
            else:
                concept, slots = line, []
            entries.append((concept, slots))

    codes = {}
    templates = {}
    for i, (concept, slots) in enumerate(entries):
        code = f"ν{i+1}"
        template = generate_template(concept, slots, args.model)
        codes[code] = template
        templates[code] = slots
        print(f"{code}: {template}")

    codebook = {
        "version": "1.0",
        "name": "Finkelstein's Stylus Generated Codebook",
        "codes": codes,
        "templates": templates
    }
    with open(args.output, 'w') as f:
        json.dump(codebook, f, indent=2)
    print(f"Saved {args.output}")

if __name__ == "__main__":
    main()