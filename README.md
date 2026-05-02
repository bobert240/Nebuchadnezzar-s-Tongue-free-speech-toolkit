# 🗽 Nebuchadnezzar’s Tongue / WNEP‑Crucible

**Censorship‑resistant toolkit for political accountability, free speech, and empirical‑normative analysis**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Purpose

This suite operationalises **George Washington’s Farewell Address (1796)** as a testable consistency engine for political actors, while providing **encrypted‑like messaging** (via offline codebooks) to bypass keyword‑based censorship. Derived tools include:

- **WNEP v2.0 + Crucible v1.0** – Automated evaluation of politicians’ foreign‑policy rhetoric against Washington’s explicit warnings.
- **Nebuchadnezzar’s Tongue** – Codebook‑based text encoding that forces platforms into expensive semantic analysis.
- **Finkelstein’s Stylus** – Local, uncensored image generation from encoded concepts.
- **Logos‑Lens** – Linguistic narrative deconstruction (propaganda analysis).
- **SEA‑Freespeak** – Specialist extraction assistant with gilding‑stripping and injection resistance.
- **ECSAF** – Empirical comparative economics (Marxist vs mainstream) via neutral schemas.
- **OSINT Weighting Engine & IDDS** – Real‑time material conditions driving dialectical simulation.

**All tools are intended for legal, educational, and journalistic use only.**

---

## 🚨 Legal & Ethical Guardrails

- **No illegal content**: Explicit filters against CSAM, credible threats, incitement to violence, or hate symbols.
- **User responsibility**: You are solely responsible for compliance with your local laws.
- **No personal data collection**: The toolkit does not collect or transmit any data.
- **Political analysis is protected**: Speech that merely criticises or analyses public figures is lawful in most democracies.

> By using this software, you affirm that you will not employ it for activity that violates applicable laws.

---

## 📁 Repository Structure

| Directory / File | Description |
|----------------|-------------|
| `wnp_crucible_system_prompt.txt` | System prompt for LLM‑based political consistency testing (Washington’s Farewell Address). |
| `nebuchadnezzar_tongue/` | Encoder, decoder, web tools, and codebook for censorship‑resistant messaging. |
| `finkelstein_stylus/` | Local Stable Diffusion image generation from codes. |
| `logos_lens/` | Narrative deconstruction system prompt and batch runner. |
| `sea_freespeak/` | Specialised extraction assistants (standard + hardened). |
| `ecsaf/` | Economic neutral schema and theoretical codebook (Marxist / mainstream). |
| `osint_weighting_engine.py` | Deterministic signal weighting (B×R×C×X) for OSINT inputs. |
| `idds_integrated_simulator.py` | Full Intelligence‑Driven Dialectical Simulator (OSINT → GRTS → PD metrics). |
| `theory.md` | Mathematical formalisation (predicate logic, set theory, differential equations). |

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Nebuchadnezzars-Tongue-WNEP-Crucible.git
cd Nebuchadnezzars-Tongue-WNEP-Crucible
2. Install dependencies (most tools use standard library; optional extras)
bash
pip install numpy scipy torch transformers diffusers   # for image generation and simulation
3. Use Nebuchadnezzar’s Tongue (text encoding)
bash
cd nebuchadnezzar_tongue
python encoder.py --message "Senator X is corrupt." --codebook codebook_template.json
# Output: {"code": "γ1", "slots": {"X": "Senator X"}, "metadata": {...}}
Decode on the recipient’s side (same codebook):

bash
python decoder.py --input encoded.json --codebook codebook_template.json
4. Run WNEP political consistency test (via LLM)
Paste the system prompt wnp_crucible_system_prompt.txt into an assistant that supports function calling, then ask it to evaluate a politician’s statement using the neutral action schema.

5. Generate an uncensored image
bash
cd finkelstein_stylus
python finkelstein_stylus.py --codebook economic_diagrams_codebook.json --code δ2 --output overaccumulation.png
🧠 Theory (Brief)
The core insight is to separate meaning from surface form:

Extract prohibition patterns from an authoritative text (e.g., Washington’s four “evils”).

Define a neutral action schema that strips emotional/gilded words.

Run a deterministic consistency test that outputs only a verdict (e.g., "washingtonian_evil").

For messaging, use an offline codebook – only codes travel over the network, forcing platforms into expensive semantic analysis.

Mathematical formulation (see theory.md):

Consistent
(
p
)
≡
¬
(
claim
(
p
)
∧
∃
α
∈
A
,
∃
x
∈
a
(
p
)
:
(
x
,
α
)
∈
M
)
Consistent(p)≡¬(claim(p)∧∃α∈A,∃x∈a(p):(x,α)∈M)
🤝 Contributing
See CONTRIBUTING.md. We welcome:

New prohibition patterns from other historical authorities (e.g., Nuremberg Code, US Constitution).

Additional language codebooks.

Formal verification of the consistency engine.

Bug reports and security issues (see SECURITY.md).

All contributions must adhere to the Code of Conduct.

📜 License
This project is licensed under the GNU Affero General Public License v3.0 – see LICENSE.
This ensures that any network service using these tools must also release its source code.

🙏 Acknowledgements
George Washington, Farewell Address (1796) – for the unassailable authority.

DeepSeek (collaborative assistant) – for co‑developing the mathematical formalisation and code.

The open‑source community – for libraries (numpy, scipy, transformers, diffusers).

🚀 Use these tools to defend free expression, expose hypocrisy, and raise the cost of censorship.

https://github.com/bobert240/Nebuchadnezzar-s-Tongue-free-speech-toolkit