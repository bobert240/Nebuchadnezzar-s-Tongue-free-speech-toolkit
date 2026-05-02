#!/usr/bin/env python3
"""
Intelligence‑Driven Dialectical Simulator (IDDS) v1.0
Synthesises OSINT weighting, consciousness dynamics (γ, Ψ, H),
Processual Dialectics metrics (PCFA, TPP, RVAE, SEK),
and counter‑Palantir deception.

Input: JSON state vector from OSINT v4.0 Lite (or compatible)
Output: JSON with consciousness trajectory, PD metrics, and counter‑measures log.
"""

import json
import datetime
import math
import random
import numpy as np
from scipy.stats import norm
from typing import Dict, List, Tuple

# -------------------------------------------------------------------
# 1. OSINT weighting (copied from osint_weighting_engine for self‑containment)
# -------------------------------------------------------------------
def base_weight(signal_key: str, confidence: str) -> float:
    type_map = {"price":1.0, "ais":1.0, "vix":1.0, "brent":1.0, "airlift":0.9, "kinetic":0.9}
    t = 0.8
    for k, v in type_map.items():
        if k in signal_key.lower():
            t = v
            break
    conf_map = {"H":1.0, "M":0.75, "L⚠":0.5}
    return t * conf_map.get(confidence, 0.5)

def recency_weight(timestamp_str: str) -> float:
    try:
        ts = datetime.datetime.fromisoformat(timestamp_str.replace("Z", ""))
    except:
        return 1.0
    hours = (datetime.datetime.utcnow() - ts).total_seconds() / 3600.0
    if hours <= 12:
        return 1.0
    if hours <= 36:
        return 0.7
    if hours <= 72:
        return 0.4
    return 0.2

def detect_regime(osint: Dict) -> str:
    flow = osint.get("FLOW", {})
    if "closed" in str(flow.get("hormuz", "")).lower():
        return "CRISIS"
    ais = flow.get("ais", "")
    if "(-" in ais:
        try:
            pct = int(ais.split("(")[1].split("%")[0])
            if pct <= -30:
                return "CRISIS"
        except:
            pass
    fin = osint.get("FINANCIAL", {})
    vix = fin.get("vix", "")
    try:
        if float(vix.split()[0]) > 25:
            return "FIN_STRESS"
    except:
        pass
    return "NORMAL"

def context_multiplier(domain: str, regime: str) -> float:
    tbl = {
        "NORMAL": {"FLOW":1.0, "ENERGY":1.0, "FINANCIAL":1.0, "MILITARY":1.0},
        "CRISIS": {"FLOW":1.6, "ENERGY":1.3, "FINANCIAL":1.2, "MILITARY":1.5},
        "FIN_STRESS": {"FLOW":0.9, "ENERGY":1.3, "FINANCIAL":1.6, "MILITARY":1.0}
    }
    return tbl.get(regime, tbl["NORMAL"]).get(domain, 1.0)

def cross_reinforcement(osint: Dict) -> float:
    flags = 0
    ais = osint.get("FLOW", {}).get("ais", "")
    if "(-" in ais:
        try:
            if int(ais.split("(")[1].split("%")[0]) <= -25:
                flags += 1
        except:
            pass
    if "rising" in str(osint.get("MARITIME", {}).get("shadow", "")).lower():
        flags += 1
    brent = osint.get("ENERGY", {}).get("brent", "")
    if "Δ" in brent:
        try:
            if float(brent.split("Δ")[1].split("%")[0]) > 5:
                flags += 1
        except:
            pass
    if "up" in str(osint.get("FINANCIAL", {}).get("war_risk", "")).lower():
        flags += 1
    return 1.3 if flags >= 2 else 1.0

def compute_signal_weight(signal_key, confidence, timestamp, domain, osint) -> float:
    B = base_weight(signal_key, confidence)
    R = recency_weight(timestamp)
    regime = detect_regime(osint)
    C = context_multiplier(domain, regime)
    X = cross_reinforcement(osint)
    return B * R * C * X

# -------------------------------------------------------------------
# 2. GRTS consciousness dynamics (γ, Ψ, H)
# -------------------------------------------------------------------
class ConsciousnessDynamics:
    def __init__(self, γ0: float, Ψ0: float, apparatus_strength: float = 0.15,
                 δ_leap: float = 0.25, hysteresis_beta: float = 0.8):
        self.γ = γ0
        self.Ψ = Ψ0
        self.α = apparatus_strength
        self.δ = δ_leap
        self.β = hysteresis_beta
        self.H = 0.0
        self.Ψ_history = []

    def state_apparatus_damping(self, t: float) -> float:
        return self.α * (1 + 0.3 * math.sin(2 * math.pi * t / 10))

    def stochastic_leap(self) -> float:
        return np.random.normal(0, self.δ**2)

    def update(self, t: int, dt: float = 1.0) -> None:
        self.Ψ_history.append(self.Ψ)
        if len(self.Ψ_history) > 20:
            self.Ψ_history.pop(0)
        if self.Ψ_history:
            weights = [self.β ** (len(self.Ψ_history)-1-i) for i in range(len(self.Ψ_history))]
            Ψ_eff = np.average(self.Ψ_history, weights=weights)
        else:
            Ψ_eff = self.Ψ
        damping = self.state_apparatus_damping(t)
        dγ = -Ψ_eff * self.γ - damping + self.stochastic_leap()
        self.γ += dγ * dt
        self.γ = max(0.0, min(1.0, self.γ))
        dH = 0.7 * Ψ_eff - 0.3 * self.γ * self.H
        self.H += dH * dt
        self.H = max(0.0, min(1.0, self.H))

    def external_update(self, stress_factor: float) -> None:
        self.Ψ += 0.05 * stress_factor
        self.Ψ = max(0.0, min(1.0, self.Ψ))

    def vanguard_intervention(self, strength: float) -> None:
        self.γ += strength * (1 - self.Ψ) * 0.3
        self.γ = min(1.0, self.γ)
        self.H *= 0.95

# -------------------------------------------------------------------
# 3. Processual Dialectics Metrics (PCFA, TPP, RVAE, SEK)
# -------------------------------------------------------------------
def pcfa_coherence(adj_matrix: np.ndarray) -> float:
    n = len(adj_matrix)
    if n < 2:
        return 0.0
    edges = np.sum(adj_matrix > 0)
    max_edges = n * (n-1)
    delta = edges / max_edges if max_edges > 0 else 0.0
    degree = np.sum(adj_matrix, axis=1)
    ent = 0.0
    for d in degree:
        if d > 0:
            p = d / np.sum(degree)
            ent -= p * np.log(p + 1e-10)
    max_ent = np.log(n) if n > 1 else 1.0
    es = ent / max_ent if max_ent > 0 else 0.0
    return max(0.0, min(1.0, 0.6 * delta - 0.4 * es))

def tpp_legitimacy(cd_pre: float, cd_post: float, delta_i: float) -> Tuple[bool, str]:
    if cd_pre <= 0.4:
        return False, "Insufficient initial coherence"
    if cd_post >= 0.9 * cd_pre:
        return False, "Inadequate coherence reduction"
    if delta_i <= 0:
        return False, "Negative systemic improvement"
    return True, "Legitimate transformation"

def rvae_triad(ontological: float, epistemic: float, systemic: float) -> Dict:
    distortion = 1.0 - (ontological * 0.4 + epistemic * 0.3 + (1 - systemic) * 0.3)
    return {"ontological_value": ontological, "epistemic_recognition": epistemic,
            "systemic_distortion": distortion, "overall_health": 1.0 - distortion}

def sek_fidelity(claim_evidence_prob: float, centrality: float, delta_i: float) -> float:
    return 0.4 * claim_evidence_prob + 0.35 * centrality + 0.25 * delta_i

# -------------------------------------------------------------------
# 4. Counter‑Palantir detection & deception
# -------------------------------------------------------------------
def detect_palantir_signature(osint: Dict) -> bool:
    fusion = sum(1 for k in ["FLOW", "MARITIME", "MILITARY"] if k in osint and osint.get(k))
    transparency = osint.get("CREDIBILITY", {}).get("transparency", 0.5)
    return fusion >= 2 and transparency < 0.3

def activate_deception() -> Dict:
    return {"action": "data_poisoning", "alibi_broadcast": True, "effect": "γ +0.05, H -20%"}

# -------------------------------------------------------------------
# 5. Main Simulator
# -------------------------------------------------------------------
def run_simulator(osint_json: Dict, generations: int = 10, seed: int = 42) -> Dict:
    random.seed(seed)
    np.random.seed(seed)

    # Extract average stress factor from OSINT weighting
    total_weight = 0.0
    weighted_stress = 0.0
    for domain, fields in osint_json.items():
        if isinstance(fields, dict):
            for key, val_str in fields.items():
                if not isinstance(val_str, str):
                    continue
                conf = "M"
                if "| H" in val_str:
                    conf = "H"
                elif "| L⚠" in val_str:
                    conf = "L⚠"
                ts = osint_json.get("ts", datetime.datetime.utcnow().isoformat())
                w = compute_signal_weight(key, conf, ts, domain, osint_json)
                # stress proxy: numeric if present else 0.5
                stress = 0.5
                total_weight += w
                weighted_stress += w * stress
    avg_stress = weighted_stress / total_weight if total_weight > 0 else 0.5

    # Initialise consciousness
    γ0 = 0.48
    Ψ0 = 0.6 + avg_stress * 0.3
    cd = ConsciousnessDynamics(γ0=γ0, Ψ0=Ψ0, apparatus_strength=0.15)

    γ_traj, Ψ_traj, H_traj = [], [], []
    interventions, deceptions = [], []

    for gen in range(generations):
        cd.external_update(avg_stress)
        cd.update(gen)
        γ_traj.append(cd.γ)
        Ψ_traj.append(cd.Ψ)
        H_traj.append(cd.H)

        if cd.Ψ > 0.7 or cd.H > 0.4:
            strength = 0.5 + 0.3 * (cd.Ψ - 0.7) if cd.Ψ > 0.7 else 0.5
            cd.vanguard_intervention(strength)
            interventions.append({"generation": gen, "strength": strength})

        if detect_palantir_signature(osint_json):
            dec = activate_deception()
            deceptions.append({"generation": gen, "action": dec})
            cd.Ψ = max(0.0, cd.Ψ - 0.1)
            cd.γ = min(1.0, cd.γ + 0.05)

    # PD metrics on final state
    # Simulate a simple adjacency matrix (placeholder – in practice from cross-reinforcement)
    adj = np.random.rand(5,5)
    ci = pcfa_coherence(adj)
    legit, reason = tpp_legitimacy(0.5, ci, (cd.γ - γ0))
    triad = rvae_triad(cd.γ, 1 - cd.Ψ, cd.H)
    fidelity = sek_fidelity(cd.γ, 1 - cd.H, cd.γ - γ0)

    result = {
        "input_regime": detect_regime(osint_json),
        "generations": generations,
        "consciousness_trajectory": {
            "γ": [round(x,4) for x in γ_traj],
            "Ψ": [round(x,4) for x in Ψ_traj],
            "H": [round(x,4) for x in H_traj]
        },
        "interventions": interventions,
        "counter_surveillance": deceptions,
        "pd_metrics": {
            "PCFA_coherence_intensity": round(ci,4),
            "TPP_legitimate": legit,
            "TPP_reason": reason,
            "RVAE_triad": triad,
            "SEK_fidelity": round(fidelity,4)
        },
        "final_state": {"γ": round(cd.γ,4), "Ψ": round(cd.Ψ,4), "H": round(cd.H,4)}
    }
    return result

# -------------------------------------------------------------------
# Command‑line entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python idds_integrated_simulator.py <osint_json_file> [generations]")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    gens = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    output = run_simulator(data, generations=gens)
    print(json.dumps(output, indent=2))