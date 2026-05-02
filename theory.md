```markdown
# Mathematical Foundation of the Consistency Testing Engine

## 1. Core Idea

The toolkit transforms qualitative warnings from George Washington’s Farewell Address (1796) into a **deterministic, falsifiable consistency test** for political actors. It then generalises this logic to **censorship‑resistant messaging** (Nebuchadnezzar’s Tongue), **local image generation** (Finkelstein’s Stylus), and **dialectical simulation** (GRTS/IDDS).

All tools share a common mathematical skeleton:

- Extract **prohibition patterns** from an authoritative source.
- Define a **neutral action schema** that strips emotional/gilded words.
- Use a **matching relation** to test whether an action violates a pattern.
- **Output only verdicts** (or codes), hiding reasoning from keyword filters.
- **Expand offline** using a local codebook.

---

## 2. Prohibition Patterns (from Washington’s Farewell Address)

Let $\mathcal{A}$ be the set of predicates derived verbatim from the 1796 text:

- $\alpha_1$: *Adopts antagonist of external agent without independent justification*
- $\alpha_2$: *Grants unequal benefit to external agent causing self‑harm*
- $\alpha_3$: *Justifies self‑harm using righteous language*
- $\alpha_4$: *Transfers own community resources without reciprocal benefit*
- $\alpha_{4b}$: *Actor personally benefits from resource transfer*

Each $\alpha_i$ is a Boolean function over a structured action object $x$.

---

## 3. Neutral Action Schema

An observable action $x$ is represented as a JSON object with the following fields (no evaluative terms):

```
{
  "agent": "string",
  "action_code": "adopt_antagonist | grant_privilege | defend_harm | other",
  "external_entity": "string",
  "justification_provided": true/false,
  "self_harm_metric": 0..10,
  "righteous_language_used": true/false,
  "personal_benefit": true/false,
  "benefit_type": "campaign_finance|popularity|media_praise|political_cover|null"
}
```

**Gilding‑stripping**: Before an action is passed to the matcher, all words from a predefined list (e.g., `heroic`, `defend democracy`, `corrupt`, `betrayal`) are removed. This ensures that only structural, non‑emotional features are tested.

---

## 4. Consistency Predicate

Let $p$ be an agent (e.g., a politician).  
Define $\text{claim}(p) \in \{\text{true},\text{false}\}$ as the agent’s assertion of adherence to the authority (e.g., a public oath to “protect American interests”).

Let $a(p)$ be the set of observable actions performed by $p$ (each is a neutral action object).

Define the matching relation $M \subseteq \mathcal{X} \times \mathcal{A}$ where $(x,\alpha) \in M$ iff the structural pattern of $x$ instantiates the prohibition pattern $\alpha$.

**Consistency predicate**:

\[
\text{Consistent}(p) \;\equiv\; \neg \big( \text{claim}(p) \;\land\; \exists \alpha \in \mathcal{A},\; \exists x \in a(p): (x,\alpha) \in M \big)
\]

If $\text{claim}(p)$ is true and at least one action matches a prohibition pattern, the agent is **inconsistent** (“Washingtonian evil”).

**Exposure**:

\[
\text{Exposed}(p) \;\equiv\; \text{claim}(p) \;\land\; \bigcup_{x \in a(p)} \{\alpha \in \mathcal{A} \mid (x,\alpha) \in M\} \neq \emptyset
\]

**Verdict** (as output by the assistant):

- `"consistent"` if $\text{Consistent}(p)$ is true.
- `"inconsistent (patterns: {α1, α2})"` if $\text{Exposed}(p)$.
- `"no_claim"` if $\text{claim}(p)$ is false.

---

## 5. Function‑Call Wrapping (Platform Safety)

The assistant does **not** output its reasoning or the matching steps. Instead, it declares a function (e.g., `run_crucible_evaluation`) that receives the neutral action schema and returns only the verdict JSON. The platform’s content moderation inspects the assistant’s output – which is a harmless JSON string – and cannot see the internal pattern matching.

---

## 6. Offline Codebooks (Nebuchadnezzar’s Tongue)

For censorship‑resistant **text messaging**, we replace the full message with a compact code:

**Codebook** (shared offline):

```json
{
  "γ1": "The official named {X} is corrupt.",
  "γ2": "Policy {Y} harms citizens because {Z}."
}
```

**Encoded message** (transmitted over the platform):

```json
{
  "code": "γ1",
  "slots": {"X": "Senator Jones"},
  "metadata": {"timestamp": "2025-08-11T12:00Z"}
}
```

The platform sees only the JSON – no banned words. The recipient expands it locally using the same codebook.

**Censorship cost**: To block such messages, a platform would have to:

- Ban **all** JSON (breaking many applications), or
- Perform **semantic analysis** on the code and slots (costly, error‑prone).

Thus, the method raises the expense of censorship from cheap keyword matching to expensive semantic interpretation.

---

## 7. Generalisation to Other Domains

The same mathematical structure applies to:

| Domain | Authority | Prohibition Patterns |
|--------|-----------|----------------------|
| Economic analysis (ECSAF) | Marx, Baran & Sweezy | Overaccumulation, fictitious capital, exploitation |
| Medical ethics | Hippocratic Oath | Withholding treatment, non‑consensual experimentation |
| Environmental compliance | Clean Air Act | Discharge exceeding limit, missing certification |

For each domain, one extracts a small set of patterns, defines a neutral action schema, strips gilding, and outputs only verdicts.

---

## 8. Consciousness Dynamics (GRTS / IDDS Extension)

For dialectical simulation, we add differential equations:

- $\gamma$: class consciousness (0‑1)
- $\Psi$: alienation index (0‑1)
- $H$: hysteresis memory (persistence of false consciousness)

**Core equations**:

\[
\frac{d\gamma}{dt} = -\Psi_{\text{eff}} \cdot \gamma - D(t) + \mathcal{N}(0,\delta^2)
\]

\[
\frac{dH}{dt} = \kappa \Psi - \beta \gamma H
\]

where $D(t)$ is ideological apparatus damping, $\kappa=0.7$, $\beta=0.3$, and $\delta=0.25$ (stochastic leap magnitude).

These models are fed by **real‑time OSINT weights** $W = B \times R \times C \times X$, linking material conditions to consciousness evolution.

---

## 9. Summary of Key Equations

| Concept | Formula |
|---------|---------|
| Consistency | $\text{Consistent}(p) \equiv \neg( \text{claim}(p) \land \exists \alpha \exists x: (x,\alpha)\in M)$ |
| Gilding‑stripping | $x' = \text{strip}(x, \text{wordlist})$ |
| Codebook encoding | $\text{encoded} = (\text{code}, \text{slots})$ |
| OSINT weight | $W = \text{type\_weight} \times \text{conf\_mult} \times \text{recency} \times \text{context} \times \text{cross}$ |
| Consciousness decay | $\dot{\gamma} = -\Psi_{\text{eff}} \gamma - D + \eta$ |
| Hysteresis | $\dot{H} = 0.7\Psi - 0.3\gamma H$ |

All are implemented in the provided Python scripts and system prompts.

---

**End of Theory Document**
```