# Review brief — round 1 — external attack review (operator's second AI)

Material: cigarette-butts | Version under review: site v0.8.4 (M-plans v0.1–v0.5, INV-01 v0.1) | Date: 2026-11-28
Reviewer: external AI designated by the operator; MUST have web access (Wayback/CDX and ResearchGate strongly helpful). Mandate is ADVERSARIAL: attack the claims, do not polish them.

## Scope (read ONLY these)
- The public site: https://abdo2048.github.io/recycling-empire/ — everything under the cigarette-butts material (ranking, action plans M-01…M-08, registry, inventions/INV-01, final reports, sources index, charter, glossary, state, log).
- Canonical text: `materials/cigarette-butts/` in github.com/abdo2048/recycling-empire (markdown is the source of truth).
- Archive originals behind every source claim: github.com/abdo2048/butt-lab → `sources/<slug>/document.pdf` (+ `text.md` AI-readable conversions).

## Mission 1 — attack review (primary)
1. **Claim-vs-source**: pick the load-bearing claims (ranking Tables A/B/C one-line justifications, each M-plan's disclosed numbers, INV-01's five-stream mass balance and falsifier ledger) and verify each against the cited source. Report every mismatch, overstatement, or citation that does not support the sentence it rides on.
2. **Numeric audit — recompute**: INV-01 midpoint closure (5.25 + 1.2 + 0.5 = 6.95 of 10 kg), water 8.3 L/kg → 83 L first cycle, NaOAc 0.47–0.94 kg/cycle vs NaOH 0.23–0.46 kg, brigade mass (261,000 lb = 118.4 t reported; 0.20 g/butt × ~260 M units ≈ 52 t corrected), capture rate ≈0.016% of ~135 M lb/yr, 150,000 butts/pallet vs those bases. Flag any figure that does not reproduce or lacks a stated basis.
3. **Label audit**: every `source_supported` / `ai_inference` / `ai_proposal` / `parameter_not_located` must match the charter definitions. Flag labels that overclaim — especially any `source_supported` without a checkable URL/section, and anything product-facing that ignores the metals stop-condition.
4. **Contradiction hunt**: cross-page contradictions (ranking vs M-plans vs registry vs INV-01 vs sources INDEX vs STATE/LOG).
5. **Site QA (bounded)**: broken internal/external links, citation superscripts pointing at the wrong source, `[S#]` numbers that do not resolve on their own page, tooltip/codemap wrongness (wrong name, wrong target). Visual/style is OUT of scope — three design rounds are already closed.

## Mission 2 — two standing desk hunts (both currently open)
a) **The full PE INTERNATIONAL report behind the 2013 LCA deck.** The deck "Flick It or Ship It — Comparative LCA of Cigarette Waste Disposal Routes with a Focus on Toxicity Impacts" (2013-09-05, 17 slides; shelf: `sources/montalbo-lca-disposal-routes/`) is presentation-level: no inventory tables, no concentration data. The full report would carry the LCIA inventory including the Cd/Pb/As/Hg concentrations — the ONLY desk-level path to the metals data (the charter stop-condition binds all product-facing work until then). Search the AUTHORS, not generic search: Trisha Montalbo, Christoph Koffler, Takuma Ono (PE INTERNATIONAL, now Sphera) — ResearchGate / LinkedIn / conference pages / personal sites; Ernel ("Ernie") Simpson (TerraCycle VP R&D); Wayback of `pe-international.com` and `five-winds.com` case-study pages 2012–2014; attachments of TerraCycle's Reg A+ circular. A documented "does not exist publicly" verdict WITH the list of what you tried is an acceptable result.
b) **Keep America Beautiful CLPP grantee weight reports — due 2026-12-15.** The $1/lb TerraCycle donation flows into KAB's Cigarette Litter Prevention Program; grantee weight reports for the 2026 cycle would give the first WEIGHED cigarette-stream tonnage (closing the units-vs-tonnes gap). Check kab.org + Wayback shortly after 2026-12-15; report figure, basis, and URL if published.

## Hard constraints — do NOT redo closed work
- Do NOT re-hunt gamma dose/dwell in public documents (firm negative: zero patents, zero filing mentions — withheld by design).
- Do NOT re-attempt the Belmont CA 2021 article (triple-verified dead end: CMS removal + 403 bot wall + empty archive sweep).
- Do NOT read the 2013 deck's "(measured by TerraCycle)" line as concentrations — it names analytes only (Cd, Pb, As, Hg, Sb, Ba, Cr, Se, Cu…).
- Never publish the brigade tonnage bare: carry BOTH 118.4 t reported and ~52 t corrected (0.20 g/butt divisor, three converging routes).
- No product-facing recommendations while Cd/Pb/As/Hg are uncharacterized (charter stop-condition).

## Questions (bounded; answer all)
1. Which 10 load-bearing claims did you attack, and the verdict per claim (held / wobbled / broke)?
2. Which numeric claims did you recompute, and which reproduce?
3. Which evidence labels are misapplied, and what should each be?
4. What did the two standing hunts yield — a finding, or a documented dead end?

## Output format (findings.md)
Numbered items, each with: type (challenge | correction | addition), severity (high | medium | low), the exact claim/file/section (or URL) affected, evidence (citation or explicitly labeled reasoning), and a proposed fix. Hunt results go in a separate final section. Keep findings under ~2 pages plus the hunt section.

## Rules
Read-only: reviewers never edit material files and never receive private copies — the public site and the two public repos are the whole corpus. Every finding needs evidence or explicitly labeled reasoning; no reformatting or style comments; a label disagreement must propose the corrected label. INV-01 § 10 (red-team verdicts) is intentionally EMPTY and waits for this round's accepted findings.

## Handback
Paste findings.md back to the operator. The owner arbitrates accepted/rejected; accepted items merge into the material, the version bumps in STATE.md, and this folder receives accepted.md.
