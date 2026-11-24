# M-XX — <Method name> — Action plan

```
id: M-XX
name: ""
family: mechanical | thermal | wet-chemical | solvent | supercritical-fluid | biological | construction-material | polymer-processing | other
priority: true
status: draft | review | frozen
version: v0.x
sources: [source-ids]
```
(Keep the block above as the file's metadata; the site builder reads it.)

## 0. Summary card
One paragraph: what it makes, the mechanism, who operates it (company / inventor / university), and why it is priority. Reused on the site's directory card.

## 1. What the sources disclose — step by step
Numbered protocol steps. Every step ends with its citation [S1], [S2]. Use disclosed numbers with units and mass basis. Where a step has no disclosed parameter, write `parameter_not_located: <what exactly>` — do not guess silently.

## 2. Equipment
List with scale notes (batch size, vessels, temperatures, pressures — from sources where possible).

## 3. Gap-fill table — labeled expert estimates

| # | Gap | Estimate (labeled) | Reasoning | Falsifier — how the team tests it |
| --- | --- | --- | --- | --- |

Every estimate row is labeled `ai_proposal` or `ai_inference` and contains concrete numbers. "Unknown" is not an estimate — use `parameter_not_located` and say what to measure.

## 4. Safety notes
Chemicals, emissions, residues, pressure — per step, with the qualified-facility requirements for each step that needs one. Material stop-conditions from material.yaml apply here.

## 5. What the team must verify in lab
Ordered list. Each item: the measurement, the acceptance criterion, and which gap-fill (row # in section 3) it confirms or kills.

## 6. Sources
[S1] full citation + URL + section/figure references.
