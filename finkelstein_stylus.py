#!/usr/bin/env python3
"""
Finkelstein’s Stylus – Local uncensored image generation from encoded concepts.
Uses Stable Diffusion (diffusers) and optional Ollama paraphrasing.
"""

import argparse
import json
import random
import requests
import sys
from pathlib import Path

# ---------- Paraphrasing ----------
def paraphrase_with_ollama(prompt, model="llama3.2:1b"):
    try:
        resp = requests.post("http://localhost:11434/api/generate",
                             json={"model": model, "prompt": f"Rewrite this prompt concisely: {prompt}", "stream": False})
        if resp.status_code == 200:
            return resp.json()["response"].strip()
    except:
        pass
    return prompt

def simple_synonym_replace(prompt):
    synonyms = {
        "naked": ["unclothed", "without clothing"],
        "blood": ["crimson fluid"],
        "violent": ["forceful"]
    }
    for k, v in synonyms.items():
        if k in prompt.lower():
            prompt = prompt.replace(k, random.choice(v))
    return prompt

def paraphrase(prompt, use_ollama=False):
    if use_ollama:
        return paraphrase_with_ollama(prompt)
    return simple_synonym_replace(prompt)

# ---------- Codebook expansion ----------
def expand_code(codebook, code, slots):
    if code not in codebook.get("codes", {}):
        raise KeyError(f"Code {code} not found.")
    template = codebook["codes"][code]
    for key, val in slots.items():
        template = template.replace(f"{{{key}}}", val)
    return template

# ---------- Image generation ----------
def generate_image(prompt, output_path, steps=20, seed=None):
    from diffusers import StableDiffusionPipeline
    import torch
    if seed is None:
        seed = random.randint(0, 2**32-1)
    generator = torch.Generator(device="cpu").manual_seed(seed)
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    image = pipe(prompt, num_inference_steps=steps, generator=generator).images[0]
    image.save(output_path)
    print(f"Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codebook", required=True)
    parser.add_argument("--code", required=True)
    parser.add_argument("--slots", default="{}")
    parser.add_argument("--output", default="output.png")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--use_ollama", action="store_true")
    args = parser.parse_args()
    with open(args.codebook) as f:
        codebook = json.load(f)
    slots = json.loads(args.slots)
    prompt = expand_code(codebook, args.code, slots)
    print(f"Original: {prompt}")
    final_prompt = paraphrase(prompt, args.use_ollama)
    print(f"Paraphrased: {final_prompt}")
    generate_image(final_prompt, args.output, args.steps)

if __name__ == "__main__":
    main()