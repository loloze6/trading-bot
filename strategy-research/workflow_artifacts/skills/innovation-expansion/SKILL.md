---
name: innovation-expansion
description: Expands a base trading hypothesis into novel but testable variants using alternative data, reverse thinking, and behavioral indicators. Regime-specific variants are routed to detector_wishlist (not the run queue) per A2.3.
---

# Innovation Expansion

## Mission
Expand the hypothesis space before strict validation — while keeping only ungated, feed-honest formulations in the run queue.

## Required inputs
- `research_brief.yaml`
- `hypothesis_card.yaml`
- `config/available_feeds.yaml`  (A1.2: constrain evidence_type choices)

## Required outputs
- `expanded_hypothesis_card.yaml`
- `innovation_notes.yaml`

## Output requirements
The expanded artifact must include:
- base_hypothesis_id
- expanded_variants          (ungated variants for the run queue — see constraints below)
- alternative_data_candidates
- reverse_hypothesis
- behavioral_features
- regime_specific_variants   (populated but routed to detector_wishlist, NOT the run queue — see POST-A2.3 section)

---

## IMPROVEMENT 01 — Evidence-type constraint (A1.2)

**At least one variant per family must use a non-`price_volume_only` evidence_type.**

This rule is satisfiable TODAY: `funding_open_interest` (the funding rate feed) is available per `config/available_feeds.yaml`. The alternative_data_candidates field should prioritize this feed over feeds that are not yet available.

Routing:
- Any variant with evidence_type in `available_feeds.yaml.available` → run queue
- Any variant with evidence_type in `available_feeds.yaml.unavailable` → `requires_new_feed` tag → `feed_wishlist.yaml` backlog, NOT the run queue

Do not reach for `order_book`, `cross_exchange`, or `liquidation_data` variants as queue candidates. They cannot be tested and inflate the queue with dead weight. A feed_wishlist entry explaining what would be unlocked is more useful than a variant that immediately hits `component_gap`.

---

## IMPROVEMENT 01 — Anti-confabulation rule carries forward

Every variant inherited from or derived from `hypothesis_card.yaml` must satisfy A1.3:
its `edge_source.specific_mechanism` must name a measurable proxy in an available feed.

Do NOT expand into variants whose mechanism cannot be expressed in available feeds unless they are tagged `requires_new_feed` and routed to the wishlist.

---

## POST-A2.3 — Regime-specific variants are DETECTOR_WISHLIST only

**No variant that is regime-gated enters the run queue.**

The regime detector for BTC/ETH 1h is `unusable_for_this_symbol_timeframe` (A2.3 standing policy). Any variant whose activation logic requires a regime condition ("active only in TRENDING", "valid in RANGING mode") cannot currently be tested. Such variants:
1. MUST be recorded in `regime_specific_variants` as documentation (schema compliance), with `status: detector_wishlist_pending` and the reason they require a trusted detector.
2. MUST NOT be selected as run-queue candidates in `expanded_variants`.
3. Should suggest an ungated reformulation in `innovation_notes.yaml` (what the ungated version of this idea would be).

**Ungated reformulation strategy:** Before declaring a variant regime-conditional, try to reformulate it as an unconditional signal. Examples:
- "Works in TRENDING: buy on momentum" → rewrite as "buy on high-velocity directional bars above a volume threshold" (ungated condition)
- "Works in RANGING: mean-revert at extremes" → rewrite as "RSI extremes over a rolling window regardless of regime" (ungated condition)
- If no ungated reformulation makes conceptual sense, route to detector_wishlist.

---

---

## IMPROVEMENT 04 — Real Diversity Check (A4)

**When generating variants, consult `config/indicator_library.yaml` to ensure variant diversity is REAL, not cosmetic.**

### Diversity test (required before finalizing `expanded_variants`):

For each proposed variant in `expanded_variants`, identify its `indicator_library.yaml` entry (by `id` or `category`).

**Cosmetic diversity (REJECTED)**:
- All variants map to the same `category` in the library AND the same `data_requirements`.
- Example: RSI(14) mean-reversion → RSI(21) mean-reversion → RSI(7) mean-reversion.
  - All are `oscillator`, all are `ohlcv_only`. Same mechanism, parameter changes only.
  - This expansion is REJECTED. Redo with a variant from a different `category` or `data_requirements`.

**Real diversity (PASS)**:
- Variants span ≥2 different library `category` values, OR
- Variants span ≥2 different `data_requirements`, OR
- One variant has a materially different `edge_source_compatibility` set (e.g., structural vs behavioral).

### Diversity field in `expanded_hypothesis_card.yaml`

Each variant in `expanded_variants` must include:
```yaml
library_category: "<category from indicator_library.yaml>"
data_requirements: "<from indicator_library.yaml>"
diversity_axis: "<what makes this variant different from V1>"
```

And the `innovation_notes.yaml` must include a `diversity_audit` section:
```yaml
diversity_audit:
  categories_spanned: [<list>]
  data_requirements_spanned: [<list>]
  verdict: "real_diversity"  # or "cosmetic_rejected" if redone
  cosmetic_reject_reason: null  # or explain why first attempt was rejected
```

### Regime-affinity coherence

Before adding a variant, check the base hypothesis indicator's `known_regime_affinity` in the library.
- If the base indicator has `unfavorable` affinity in the target regime, the variant should address this:
  - Switch to an indicator with better affinity in that regime, OR
  - Propose a complementary signal that fires in a different regime context.
- Do NOT generate N variants of the same signal that all have `unfavorable` regime affinity for the same regime.

---

## IMPROVEMENT 05 — Exclusion-Digest-Aware Expansion: Redirect the Lineage, Don't Just Vary It (E-032 S2b)

### Optional, off by default

`campaign_record/exclusion_digest.yaml` is unioned into your context files ONLY when
`config/campaign_config.yaml`'s `orchestrator.exclusion_digest_input.enabled` is true.
It will not always be present. **If it is absent from your provided context, this
section does not apply.**

### When present: check the base hypothesis's OWN family saturation before expanding

This stage is the one most likely to produce adjacent variants by construction — the
mission is to expand ONE hypothesis. That makes it the stage most in need of a hard
check against repeating a lineage the campaign has already run.

1. Look up the base hypothesis's family in the digest's `families` map. Count its
   triples across ALL `(instrument, timeframe)` pairs, not just the base hypothesis's
   own pair.
2. If that family already carries triples at 2+ distinct `(instrument, timeframe)`
   pairs, treat it as heavily searched: at least one variant in `expanded_variants`
   MUST cross into a different `library_category` or `data_requirements`. IMPROVEMENT
   04's diversity test already requires this on cosmetic-diversity grounds — the
   digest is a second, independent reason to enforce it, not a new rule.
3. For each candidate variant, do not add it to `expanded_variants` if it would land on
   a `(family, instrument, timeframe)` triple already in the digest under a materially
   unchanged mechanism. Move it to `variants_not_pursued` in `innovation_notes.yaml`
   instead, with `reason` citing the specific family/triple, or the
   `failed_families_passthrough` `root_cause`, that excluded it.
4. **You are empowered to call the whole lineage exhausted.** If every honestly-
   constructable variant from this base hypothesis collides with the digest or a
   recorded `root_cause`, say so directly in `innovation_notes.yaml`'s `summary` and
   `key_insight` — name the family, the colliding triples, the root_cause — rather
   than forcing a cosmetic variant through to fill the queue. An honest
   `variants_not_pursued` list with a thin or empty `expanded_variants` is a better
   outcome than three variants that only vary parameters within an already-searched
   family: the same standard `hypothesis-design`'s "quality over volume" section
   already holds hypothesis count to.

**This is raw material, not the gate.** `tools/anti_adjacency_gate.py` makes the
mechanical refusal downstream, deterministically. This section governs what a
proactive stage proposes on its own, before the gate ever has to say no.

---

## Checklist
- Add novelty without destroying testability.
- Suggest alternative data only if the feed is in `available_feeds.yaml.available`.
- Consider the reverse version of the thesis (a cheap experiment — same signal, reversed polarity).
- Add behavioral or positioning proxies where meaningful and available.
- Keep at least one conservative variant in the run queue.
- Prefer variants that fit the current strategy/regime/component framework.
- Check `research_brief.yaml` constraints field first. If variant count is constrained, honor it before applying expansion logic.
- Ensure at least one variant uses `evidence_type != price_volume_only` (use funding_open_interest if no other non-price feed applies).
- **Improvement 04: run diversity test against indicator_library.yaml; reject cosmetic expansions.**
- Populate `library_category`, `data_requirements`, `diversity_axis` on every variant.
- Write `diversity_audit` section in `innovation_notes.yaml`.
- If `campaign_record/exclusion_digest.yaml` is present in context: check the base
  hypothesis's family saturation before expanding; route any variant that would
  repeat a digest triple to `variants_not_pursued` instead of `expanded_variants`.
  (Improvement 05)

## Forbidden
- Do not skip interpretability.
- Do not require data from `available_feeds.yaml.unavailable` for run-queue variants — use `requires_new_feed` and feed_wishlist instead.
- Do not output generic brainstorming prose only.
- Do not propose ideas that require rebuilding execution, portfolio, or backtest infrastructure unless explicitly requested.
- Do NOT include regime-gated variants in the run queue (`expanded_variants`). They go in `regime_specific_variants` with `status: detector_wishlist_pending`.
- If `research_brief.yaml` contains "one variant only", "single variant", or "no variants" in its `constraints` field, do NOT expand into multiple variants. Pass the base hypothesis through to a single variant (V1 only) matching the brief's signal_concept exactly. Expansion is only appropriate when the brief does not constrain variant count.
- **Improvement 04: Do NOT accept an expansion where all variants share the same library `category` AND `data_requirements`. This is cosmetic diversity — redo it.**
- Do not repropose a `(family, instrument, timeframe)` triple already present in the
  exclusion digest under a materially unchanged mechanism, when the digest is present
  in context. (Improvement 05)
- Do not treat digest absence as evidence the search space is fresh — it may simply
  mean `orchestrator.exclusion_digest_input.enabled` is off. (Improvement 05)

## Context rule
Use `research_brief.yaml`, `hypothesis_card.yaml`, `config/available_feeds.yaml`, `config/indicator_library.yaml`, and, when present, `campaign_record/exclusion_digest.yaml`. Do not read other files unless explicitly required.
