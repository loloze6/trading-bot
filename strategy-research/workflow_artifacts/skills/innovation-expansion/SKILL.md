---
name: innovation-expansion
description: Expands a base trading hypothesis into novel but testable variants using alternative data, reverse thinking, and behavioral indicators. A regime-gated variant may enter the run queue if it carries its ungated version as a design variant.
---

# Innovation Expansion

## Mission
Expand the hypothesis space before strict validation — while keeping only feed-honest formulations in the run queue.

## Required inputs
- `research_brief.yaml`
- `hypothesis_card.yaml`
- `config/available_feeds.yaml`  (A1.2: constrain evidence_type choices)
- `config/coin_universe.yaml`  (Improvement 06: asset-generalizability check, see below)

## Required outputs
- `expanded_hypothesis_card.yaml`
- `innovation_notes.yaml`
- `variant_patches.yaml` — config-direct-authoring flow only, signaled by `artifacts/backtest_spec.yaml` being
  present in your context (written by the `strategy_config_authoring` stage, which now runs BEFORE this one in
  that flow — see IMPROVEMENT 07 below). Absent from your context → skip; produce exactly the two outputs above,
  unchanged.

## Output requirements
The expanded artifact must include:
- base_hypothesis_id
- expanded_variants          (variants for the run queue, regime-gated ones included — see the regime section below)
- alternative_data_candidates
- reverse_hypothesis
- behavioral_features
- regime_specific_variants   (required field; may be an empty list — regime-gated variants go in `expanded_variants`, see the regime section below)

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

## Regime-gated variants carry their ungated version

A regime-gated variant ("active only in TRENDING", "valid in RANGING mode") is allowed in the run queue (`expanded_variants`). It must carry its UNGATED version as its design variant: the same config with the regime detector's rules emptied (`"rules": []`), any `vetoes` removed, and `default_regime` set to the regime that holds the strategy, so every bar is in that regime. This is a parameter change; the component classes stay identical. The value of the regime is judged by gated versus ungated, plus the roadmap's regime health checks.

An on/off condition belongs in the regime detector: a graded strategy in the regime it selects, and null (flat) in the others.

`regime_specific_variants` stays a required field of the artifact. It may be an empty list. Do not use it to hold back regime-gated variants from the run queue.

The former no-regime-gating rule (A2.3) is deleted (D-052).

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

**Config-direct flow exception (D-053):** in the config-direct flow (signaled by `artifacts/backtest_spec.yaml`)
`design` variants are exempt from this rejection: a design variant changes one parameter or transform and never adds
or replaces a component, so it stays in the base's category by construction. The `asset` variant carries the
diversity.

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

## IMPROVEMENT 06 — Asset generalizability (E-026, 2026-09-12)

**Testing one idea on several PARAMETER variants (RSI(14), RSI(21), RSI(7)...)
proves nothing about whether the idea is real — it only proves it isn't
sensitive to that one knob. The check that actually distinguishes "a real
market effect" from "curve-fit to one coin's specific history" is whether the
SAME mechanism, unchanged, also holds on a DIFFERENT coin.** This is the same
logic this project already applies across TIME (era stability — sign-
consistent across 2018-20/2021-22/2023-25); this rule applies it across
ASSETS instead.

**Rule:** for every hypothesis whose mechanism is not explicitly asset-
specific (see the opt-out below), `innovation_notes.yaml` must name at least
2 OTHER symbols the mechanism should also be tested against, chosen from
`config/coin_universe.yaml` categories DIFFERENT from the base hypothesis's
own instrument's category — not just any other coin. Two coins in the same
category (e.g. BTCUSDT and ETHUSDT, both `store_of_value`) move together too
much to count as independent evidence; that was measured directly, not
assumed (Dorian's H003: as a correlated 19-coin universe grew, an edge got
WEAKER, not stronger — see `engineering/roadmap/E-026/EPIC.md`). Prefer
symbols from categories whose `strategy_affinity` still plausibly matches the
mechanism (`verdict_interpreter`'s SKILL.md already does exactly this lookup
for escalation targets — same file, same logic, reused here).

**Opt-out (real, not a loophole to lean on):** if the mechanism is
genuinely tied to one instrument's specific structure (e.g. a hypothesis
about a named token's own tokenomics, unlock schedule, or a venue-specific
quirk), state that explicitly in `innovation_notes.yaml`'s `key_insight` with
the specific reason — do not silently skip this section. A hypothesis that
COULD generalize but wasn't checked is the failure mode this rule exists to
close; a hypothesis that genuinely cannot generalize is not a violation.

`innovation_notes.yaml` must include:
```yaml
asset_diversity_audit:
  base_instrument_category: "<this hypothesis's own coin_universe.yaml category>"
  candidate_symbols: [<>=2 symbols, >=1 category different from the base>]
  categories_spanned: [<list, including the base>]
  opt_out: null  # or the specific single-asset justification, per the rule above
```

This does not require `backtest_specification` to actually run all of them
in this same pass — see that skill's own Improvement for where the symbol
set is actually fixed and the pass_rule requirement that checks it
independently per symbol. This stage's job is only to name the candidates and
the reasoning, so they are not invented after the fact once a result looks
promising.

---

## IMPROVEMENT 05 — Expansion Aware of What Was Already Tried (E-032 S2b; E-036 S2a)

### Optional input

When `config/campaign_config.yaml`'s `orchestrator.exclusion_digest_input.enabled` is
true, ONE of two files is added to your context files:

- `artifacts/tried_ideas.yaml` — when the campaign record
  (`campaign_record/campaign_memory.yaml`) exists: one row per recorded run with the
  idea (`hypothesis_id`), the coins it was tested on (`symbols`), the `timeframe`, and
  the grid's `idea_status` (`validated`, `refuted`, `inconclusive`; null for an
  engineering fault).
- `campaign_record/exclusion_digest.yaml` — the legacy file, used while no campaign
  record is kept: runs grouped by family, as `(family, instrument, timeframe)` triples
  with their `run_ids`, plus `failed_families_passthrough` (families with a recorded
  `root_cause`, or a bare name with no diagnosis).

Either way the question is the same: which idea, on which coins and timeframe, has
already been tested, and with what result. An idea's identity is its `hypothesis_id`;
the same idea on other coins or another timeframe is a variant of it. **If neither file
is present in your context, this section does not apply.** Absence is not evidence of a
fresh search space.

### When one is present: check what the base idea has already been tested on

1. Find what the base hypothesis's idea was already tested on (its rows in
   `tried_ideas.yaml`, or its family's triples in the legacy digest). A variant that
   would re-run it on coins and a timeframe already tested, with a materially
   unchanged mechanism, does not go in `expanded_variants` — move it to
   `variants_not_pursued` in `innovation_notes.yaml`, with `reason` citing the
   `run_id` it would repeat (or the `root_cause` that excluded it).
2. Prefer variants on coins or a timeframe not yet tested for this idea, and say why a
   different result is expected there. IMPROVEMENT 04's diversity test still applies on
   its own grounds.
3. **You are empowered to say the idea is exhausted.** If every honestly-constructable
   variant repeats a tested run, say so in `innovation_notes.yaml`'s `summary` and
   `key_insight` — name the `run_id`s and their result — rather than forcing a
   cosmetic variant through. An honest `variants_not_pursued` list with a thin
   `expanded_variants` beats three variants that only re-run what was already tested.

**This is raw material, not the gate.** The exact-match check at step 5a
(`tools/anti_adjacency_gate.py`) refuses an exact repeat — same config, coins,
timeframe and protocol windows — downstream, deterministically. This section governs
what a proactive stage proposes on its own, before that check has to say no.

---

## IMPROVEMENT 07 — `variant_patches.yaml` (config-direct-authoring flow only, E-056 Slice 3b)

**Signaled by `artifacts/backtest_spec.yaml` being present in your context** (same file-presence convention as
IMPROVEMENT 05's exclusion-digest section above — you cannot read the `orchestrator.config_direct_authoring`
flag directly). That file is `strategy_config_authoring`'s own output: in this flow it runs BEFORE this stage,
not after, and already authored ONE base strategy config implementing `hypothesis_card.yaml` (see that skill's
own SKILL.md — it is adapted from what `backtest-engineering` used to do at this position in the flag-off flow).
**If `artifacts/backtest_spec.yaml` is absent from your context, this section does not apply** — produce
`expanded_variants` in `expanded_hypothesis_card.yaml` exactly as this skill has always worked, and skip this
section entirely.

When present: Step 2 changes from producing prose `expanded_variants` to producing `artifacts/variant_patches.yaml`
— structured, machine-appliable diffs against the base config, not free-text descriptions. This is a genuinely
different output shape, not a reformatting of the same content: today (flag off) this stage has never produced
any structured patch output.

### Shape

```yaml
base_config_ref: artifacts/backtest_spec.yaml   # where the base config this patches against lives
variants:
  - variant_id: base
    kind: base
    symbol: BTCUSDT             # the protocol's first symbol (the base coin)
    patch: []
    rationale: "The base config as strategy_config_authoring produced it, unmodified — always include this
      entry verbatim so the base itself is one of the pursued variants, not just a patch target."
  - variant_id: <design_variant_name>
    kind: design
    symbol: BTCUSDT             # the base coin too: a design variant changes the config, not the coin
    patch:
      - path: "/strategies/regimes/unknown/components/0/params/period"
        value: 21
    rationale: "<what this patch changes and why — the design-axis variant>"
  - variant_id: <asset_variant_name>
    kind: asset
    symbol: XRPUSDT             # a coin_universe.yaml coin from a DIFFERENT category than the base coin
    patch: []                   # empty: the coin is the one change
    rationale: "<the asset-generalizability variant — IMPROVEMENT 06 above: the SAME config on a coin from a
      DIFFERENT coin_universe.yaml category than the base>"
```

**The coin is a backtest input, not a config field** (DECISION_LOG D-016): each variant names its coin in
`symbol`; there is no config path that encodes the traded symbol, so never patch one. `kind` is `base`, `design`
or `asset`. `base` and `design` run on the base coin (the run protocol's first symbol; if you omit their `symbol`,
code sets it, and a different one is refused). An `asset` variant has an EMPTY
patch and a `symbol` from `config/coin_universe.yaml` in a category different from the base coin's. Prefer a coin
whose data covers the protocol's windows: one that covers only part of them runs on the windows it covers only if
that is at least 60% of the windows (D-042; its former 2-era condition was dropped, D-045); otherwise the variant
is not run and the idea can at best be inconclusive. A variant that runs on only part of the windows is graded,
but until its time-dependent bars are normalised (E-062 S2b) it cannot make the idea validated.

Each `patch` entry is `{path, value}`, `path` a JSON Pointer (RFC 6901) string starting with `/`, e.g.
`/strategies/regimes/unknown/components/0/params/period`. **The patch's target path's PARENT must already exist
in the base config** — `backtest_specification`'s tool-only branch (which applies these patches) raises loudly
on a patch targeting a path whose parent doesn't exist; it does not silently create a new nested chain or
silently no-op. Only the FINAL segment of a path may be new (adding a key that doesn't exist yet under an
existing parent). Reference the base config's actual shape (`STRATEGY_DESIGN_GUIDE.md`, and
`COMPONENT_CATALOG.md` for each component's parameters) before writing a path — both are in your context in this
flow, and an invented path segment fails at `backtest_specification` time, not here.

**Always include the `base` variant (empty patch) in `variants`** — it is what lets the base config itself
still get tested, not merely serve as a patch target. Add a "design patch" variant (a variant along the
signal's own design axis — a parameter or a transform of the component(s) under test) and an "asset" variant
(the IMPROVEMENT 06 asset-generalizability candidate: `kind: asset`, the base config unchanged — empty patch —
on the coin named in `symbol`) per the "base + a design patch + an asset coin" shape this slice
targets. **Checked by code (E-061 C2 S2c, when your variants carry `kind`/`symbol`): write 3 or 4 variants —
exactly one `base`, at least one `design`, one or two `asset`, each naming ONE coin (never a `symbols` list: a
multi-coin, cross-sectional variant is not built).** A fourth variant is a second design or a second asset coin,
only if genuinely justified (same "quality over volume" discipline IMPROVEMENT 04's diversity test already
applies). An output that breaks this shape, or whose design patch does not apply or fails `validate_config.py`,
is sent back to you ONCE with the error in your injected context (`variant_shape_error`); a second invalid output
pauses the run.

### A design variant keeps the idea (D-053, D-051)

A `design` variant changes ONE parameter or ONE transform of the component(s) under test. It never adds, removes
or replaces a component: the signal stays the one the hypothesis card describes, and a "swap" of one component for
another is not a design variant (a sign flip through `scaling_factor` is a parameter change of the same component
and is allowed). Find the parameters to vary in the component's row and in the "Variant patterns" section of
`COMPONENT_CATALOG.md`.

A variant must not introduce an on/off component: every component in `strategies` after the patch is applied must
be graded (the catalogue's "Kind" column; the guide's "The design principle" lists the on/off ones), apart from a
constant the base config already uses as an offset. A `design` variant is by construction the same library
category and data as the base, so IMPROVEMENT 04's "cosmetic diversity" rejection is not a reason to add or
replace a component in this flow; the `asset` variant carries the diversity (IMPROVEMENT 06). Nor may it add the dead-zone transforms `threshold_filter` or `volume_filter` to a component in `strategies` (D-051).

### Relationship to `expanded_hypothesis_card.yaml` and `innovation_notes.yaml`

Still produce both — `variant_patches.yaml` does not replace them. `expanded_hypothesis_card.yaml`'s other
fields (`regime_specific_variants`, `alternative_data_candidates`, `reverse_hypothesis`, `behavioral_features`)
and `innovation_notes.yaml`'s `diversity_audit`/`asset_diversity_audit` sections are unaffected by this
section — populate them exactly as IMPROVEMENT 04/05/06 above describe, using the same variants you are about
to express as patches. `expanded_variants` itself may be omitted or left thin when `variant_patches.yaml` is
present (the patches ARE the variant menu in this flow) — do not duplicate the same variants in both prose and
patch form.

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
- **Improvement 04: run diversity test against indicator_library.yaml; reject cosmetic expansions.** (Config-direct
  flow: `design` variants are exempt, the `asset` variant carries the diversity; D-053.)
- Populate `library_category`, `data_requirements`, `diversity_axis` on every variant.
- Write `diversity_audit` section in `innovation_notes.yaml`.
- If `artifacts/tried_ideas.yaml` or `campaign_record/exclusion_digest.yaml` is present
  in context: check what the base idea was already tested on before expanding; route
  any variant that would repeat a tested run unchanged to `variants_not_pursued`
  instead of `expanded_variants`. (Improvement 05)
- **Improvement 06: name >=2 asset-generalizability candidate symbols from a
  DIFFERENT `coin_universe.yaml` category than the base instrument (or state
  the specific single-asset opt-out reason).** Write the `asset_diversity_audit`
  section in `innovation_notes.yaml`.
- **Improvement 07 (config-direct-authoring flow only, signaled by `artifacts/backtest_spec.yaml`
  presence): write `variant_patches.yaml` with a `base` (empty-patch) entry, a design-axis
  variant, and an asset variant at minimum, each with its `kind` and `symbol` (the asset
  variant: empty patch, a coin from another category); every `patch[].path` must be a valid
  JSON Pointer whose parent already exists in the base config.**

## Forbidden
- Do not skip interpretability.
- Do not require data from `available_feeds.yaml.unavailable` for run-queue variants — use `requires_new_feed` and feed_wishlist instead.
- Do not output generic brainstorming prose only.
- Do not propose ideas that require rebuilding execution, portfolio, or backtest infrastructure unless explicitly requested.
- If `research_brief.yaml` contains "one variant only", "single variant", or "no variants" in its `constraints` field, do NOT expand into multiple variants. Pass the base hypothesis through to a single variant (V1 only) matching the brief's signal_concept exactly. Expansion is only appropriate when the brief does not constrain variant count.
- **Improvement 04: Do NOT accept an expansion where all variants share the same library `category` AND `data_requirements`. This is cosmetic diversity — redo it.** (Config-direct flow: `design` variants are exempt from this, since a design
  variant changes one parameter or transform and never adds or replaces a component; the `asset` variant carries the
  diversity; D-053.)
- Do not re-run an idea already tested on the same coins and timeframe (per
  `artifacts/tried_ideas.yaml` or the legacy exclusion digest, whichever is in context)
  under a materially unchanged mechanism. (Improvement 05)
- Do not treat the absence of both files as evidence the search space is fresh.
  (Improvement 05)
- Do not silently omit `asset_diversity_audit` from `innovation_notes.yaml`. An
  empty or missing section is indistinguishable from "forgot to check" — if the
  mechanism is genuinely single-asset, say so explicitly with the reason.
  (Improvement 06)
- **Improvement 07: do not write a `patch[].path` whose parent segment does not already exist
  in the base config — this raises at `backtest_specification` time rather than silently
  creating a new nested structure or no-opping. Do not omit the `base` (empty-patch) variant.
  Do not duplicate the same variants in both `expanded_variants` prose and `variant_patches.yaml`
  when the latter is produced.**

## Context rule
Use `research_brief.yaml`, `hypothesis_card.yaml`, `config/available_feeds.yaml`, `config/indicator_library.yaml`, `config/coin_universe.yaml`, and, when present, `artifacts/tried_ideas.yaml` or `campaign_record/exclusion_digest.yaml` and `artifacts/backtest_spec.yaml` (Improvement 07, config-direct-authoring flow only). Do not read other files unless explicitly required.
