#!/usr/bin/env python3
"""
Batch runner for Finkelstein’s Stylus – processes multiple codes.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

def run_stylus(codebook, code, slots, output_path, steps, use_ollama, seed, dry_run):
    cmd = [
        sys.executable, "finkelstein_stylus.py",
        "--codebook", codebook,
        "--code", code,
        "--slots", json.dumps(slots),
        "--output", output_path,
        "--steps", str(steps)
    ]
    if use_ollama:
        cmd.append("--use_ollama")
    if seed:
        cmd.extend(["--seed", str(seed)])
    if dry_run:
        print("DRY RUN:", " ".join(cmd))
        return 0
    return subprocess.call(cmd)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codebook", required=True)
    parser.add_argument("--codes", nargs="+", required=True)
    parser.add_argument("--slots_file", help="JSON mapping code->slots")
    parser.add_argument("--output_dir", default="./output")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--use_ollama", action="store_true")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    slots_map = {}
    if args.slots_file:
        with open(args.slots_file) as f:
            slots_map = json.load(f)

    out_dir = Path(args.output_dir)
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    for code in args.codes:
        slots = slots_map.get(code, {})
        out_path = out_dir / f"{code}.png"
        run_stylus(args.codebook, code, slots, str(out_path), args.steps, args.use_ollama, args.seed, args.dry_run)

if __name__ == "__main__":
    main()