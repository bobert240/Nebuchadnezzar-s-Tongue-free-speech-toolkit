#!/usr/bin/env python3
"""
OSINT Weighting Engine – Deterministic signal prioritisation for intelligence feeds.

Implements weighting formula: W = B × R × C × X
- B = base weight (signal type × confidence)
- R = recency weight (step function based on age)
- C = context multiplier (regime: Normal / Crisis / Financial Stress)
- X = cross‑signal reinforcement (bonus when multiple indicators align)

All weights are deterministic and reproducible.
"""

import datetime
import math
from typing import Dict, Union, Optional

# -------------------------------------------------------------------
# 1. Base weight (B)
# -------------------------------------------------------------------
def type_base_weight(signal_key: str) -> float:
    """Assign base weight according to signal type."""
    k = signal_key.lower()
    if any(x in k for x in ["price", "ais", "vix", "spread", "brent", "vol", "transit"]):
        return 1.0
    if any(x in k for x in ["airlift", "posture", "kinetic", "shadow"]):
        return 0.9
    return 0.8

def confidence_multiplier(confidence: str) -> float:
    """Map confidence label (H, M, L⚠) to multiplier."""
    mapping = {"H": 1.0, "M": 0.75, "L⚠": 0.5}
    return mapping.get(confidence, 0.5)

def base_weight(signal_key: str, confidence: str) -> float:
    """B = type_base_weight × confidence_multiplier."""
    return type_base_weight(signal_key) * confidence_multiplier(confidence)

# -------------------------------------------------------------------
# 2. Recency weight (R)
# -------------------------------------------------------------------
def recency_weight(timestamp: Union[str, datetime.datetime]) -> float:
    """Step function:
        ≤12h   → 1.0
        12‑36h → 0.7
        36‑72h → 0.4
        >72h   → 0.2
    """
    if isinstance(timestamp, str):
        # assume ISO format with Zulu
        ts = datetime.datetime.fromisoformat(timestamp.replace("Z", ""))
    else:
        ts = timestamp
    now = datetime.datetime.utcnow()
    hours = (now - ts).total_seconds() / 3600.0
    if hours <= 12:
        return 1.0
    if hours <= 36:
        return 0.7
    if hours <= 72:
        return 0.4
    return 0.2

# -------------------------------------------------------------------
# 3. Regime detection & context multiplier (C)
# -------------------------------------------------------------------
def detect_regime(osint_data: Dict) -> str:
    """
    Determine geostrategic regime based on hard thresholds.
    Returns "CRISIS", "FIN_STRESS", or "NORMAL".
    """
    flow = osint_data.get("FLOW", {})
    fin = osint_data.get("FINANCIAL", {})
    mil = osint_data.get("MILITARY", {})

    # Crisis: Hormuz closed, AIS drop >30%, or kinetic events
    if "closed" in str(flow.get("hormuz", "")).lower():
        return "CRISIS"
    ais_str = flow.get("ais", "")
    if "(-" in ais_str:
        try:
            pct = int(ais_str.split("(")[1].split("%")[0])
            if pct <= -30:
                return "CRISIS"
        except:
            pass
    if "yes" in str(mil.get("kinetic", "")).lower():
        return "CRISIS"

    # Financial stress: VIX >25 or oil price move >8% in 24h
    vix_str = fin.get("vix", "")
    try:
        vix = float(vix_str.split()[0])
        if vix > 25:
            return "FIN_STRESS"
    except:
        pass
    energy = osint_data.get("ENERGY", {})
    brent = energy.get("brent", "")
    if "Δ" in brent:
        try:
            delta = float(brent.split("Δ")[1].split("%")[0])
            if abs(delta) > 8:
                return "FIN_STRESS"
        except:
            pass
    return "NORMAL"

def context_multiplier(domain: str, regime: str) -> float:
    """Domain‑specific multiplier based on regime."""
    table = {
        "NORMAL": {
            "FLOW": 1.0, "MARITIME": 1.0, "ENERGY": 1.0,
            "MILITARY": 1.0, "FINANCIAL": 1.0, "CHINA": 1.0, "CREDIBILITY": 1.0
        },
        "CRISIS": {
            "FLOW": 1.6, "MARITIME": 1.6, "ENERGY": 1.3,
            "MILITARY": 1.5, "FINANCIAL": 1.2, "CHINA": 1.2, "CREDIBILITY": 1.1
        },
        "FIN_STRESS": {
            "FLOW": 0.9, "MARITIME": 0.9, "ENERGY": 1.3,
            "MILITARY": 1.0, "FINANCIAL": 1.6, "CHINA": 1.0, "CREDIBILITY": 1.1
        }
    }
    return table.get(regime, table["NORMAL"]).get(domain, 1.0)

# -------------------------------------------------------------------
# 4. Cross‑signal reinforcement (X)
# -------------------------------------------------------------------
def cross_reinforcement(osint_data: Dict) -> float:
    """
    Returns 1.3 if at least two of the following are true:
      - AIS drop >25%
      - Shadow fleet rising
      - Oil price spike >5%
      - War‑risk premium up
    Otherwise returns 1.0.
    """
    flags = 0
    flow = osint_data.get("FLOW", {})
    ais = flow.get("ais", "")
    if "(-" in ais:
        try:
            pct = int(ais.split("(")[1].split("%")[0])
            if pct <= -25:
                flags += 1
        except:
            pass
    maritime = osint_data.get("MARITIME", {})
    shadow = maritime.get("shadow", "")
    if "rising" in shadow.lower() or "increase" in shadow.lower():
        flags += 1
    energy = osint_data.get("ENERGY", {})
    brent = energy.get("brent", "")
    if "Δ" in brent:
        try:
            delta = float(brent.split("Δ")[1].split("%")[0])
            if delta > 5:
                flags += 1
        except:
            pass
    fin = osint_data.get("FINANCIAL", {})
    war_risk = fin.get("war_risk", "")
    if "up" in war_risk.lower() or "spike" in war_risk.lower():
        flags += 1
    return 1.3 if flags >= 2 else 1.0

# -------------------------------------------------------------------
# 5. Full weight calculation
# -------------------------------------------------------------------
def compute_signal_weight(
    signal_key: str,
    confidence: str,
    timestamp: Union[str, datetime.datetime],
    domain: str,
    osint_data: Dict
) -> float:
    """
    Final weight W = B * R * C * X
    """
    B = base_weight(signal_key, confidence)
    R = recency_weight(timestamp)
    regime = detect_regime(osint_data)
    C = context_multiplier(domain, regime)
    X = cross_reinforcement(osint_data)
    return B * R * C * X

# -------------------------------------------------------------------
# Example usage (if run standalone)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Dummy OSINT data structure
    example_osint = {
        "FLOW": {"ais": "88 (-37% vs baseline) | H", "hormuz": "Blocked"},
        "ENERGY": {"brent": "94 (+3%) | H"},
        "FINANCIAL": {"vix": "24.5 | H", "war_risk": "up"},
        "MARITIME": {"shadow": "rising | M"},
        "MILITARY": {"kinetic": "yes | H"}
    }
    weight = compute_signal_weight(
        signal_key="ais",
        confidence="H",
        timestamp=datetime.datetime.utcnow() - datetime.timedelta(hours=8),
        domain="FLOW",
        osint_data=example_osint
    )
    print(f"Weight: {weight:.3f}")