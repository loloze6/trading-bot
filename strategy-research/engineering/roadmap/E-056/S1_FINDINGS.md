# E-056 S1 — Characterization findings (2026-09-20)

Read-only characterization. No code, config, or backtests were run. Every claim below was
checked directly against the file:line cited; corpus counts were measured with one-off
scripts run and deleted in this session (not committed).

## 0. Worktree note (read this before trusting any commit-hash cross-reference)

This worktree's HEAD (`8bfcd0b6`) is **two commits behind master** (`a20fb7ec`). The dispatch
brief's required reading — `strategy-research/engineering/roadmap_review_2026-09-18.md`,
`delivery_plan_v26.md`, `engineering_roadmap.html` — does **not exist in this working tree**.
It was added by `844e6a17` ("rebuild the roadmap as v27 and add a delivery plan"), which is on
`master` via merge commit `a20fb7ec` but was never merged into this worktree's branch
(`worktree-agent-a372e12a2cc208201`). I read all three files via `git show 844e6a17:<path>`
(read-only, no working-tree write) rather than editing/merging anything — consistent with the
"no code changes" instruction. If a later session edits these files directly in this worktree,
it will be editing a copy that doesn't exist yet on this branch; that edit needs `git merge`
first, which is out of S1's scope.

## 1. Bot-config vocabulary

Primary source: `trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md` (283 lines) is comprehensive
and current — cross-checked line-by-line against the three engine files. It already covers
99% of what a design guide needs. Full table:

| Field | Type | Allowed values | Validator rule | Source |
|---|---|---|---|---|
| `regime_detector.mode` | str | `threshold_rules` (default) \| `score` \| `score_product` | none (unvalidated; unknown mode falls through to `_classify_score`, silently) | `regime_engine.py:27,135-140` |
| `regime_detector.components[]` | list | `{id, class, params}` | V2: veto/rule/regime ids must be declared here; class must import (`_load_class`, raises `ValueError`, not a `validate_config.py` check) | `regime_engine.py:34-39`, `registry.py:11-23` |
| `regime_detector.vetoes[]` | list | `{id, transforms, rules[], result, consecutive_bars}` | V2 (id declared), V3/V4 (transform ops), V7 (`result` in `{trending,mean_reversion,chop,unknown}`) | `validate_config.py:74-89,175-180`; `regime_engine.py:124-133` |
| `regime_detector.rules[]` | list | `{regime, any_of: [[{id, op, value\|low/high}]]}` | V2 (ids), V7 (`regime` valid) | `validate_config.py:81-89,168-173`; `regime_engine.py:148-159` |
| `regime_detector.default_regime` | str | `trending\|mean_reversion\|chop\|unknown`, default `unknown` if key absent | V7 (valid name); V9 (forbidden to alias trending/mean_reversion/chop while `rules` non-empty — bypasses the gate); V10 (fully-ungated config must not point at a null `strategies.regimes` entry) | `validate_config.py:186-257`; `regime_engine.py:70,153` |
| `regime_detector.regimes.<name>` (score/score_product mode only) | dict | `{components: [{id, weight, transforms, divisor?}]}` | V2 (ids), V7 (name) | `regime_engine.py:180-225` |
| `regime_detector.min_score` / `min_margin` | float | default 0.35 / 0.05 | none | `regime_engine.py:28-29` |
| `strategies.warmup` | int | default = engine lookback; legacy-parity value documented as 51 | none directly; effective warmup capped at `min(config.warmup, smallest deque maxlen)` | `strategy_engine.py:79`; `STRATEGY_CONFIG_REFERENCE.md:92` |
| `strategies.min_allocation_change` | float | non-negative; overrides `risk_management.controls.min_allocation_change.threshold` (config.json default 0.2) for this strategy only | V11 | `validate_config.py:284-290` |
| `strategies.regimes.<name>` | dict \| `null` | `null` = deliberately flat (forecast 0.0) — **the "none" assignment**, not an error | V1 (must be object or null); V10 (fully-ungated detector forbids null at `default_regime` target) | `validate_config.py:59-64,241-257`; `strategy_engine.py:139-141`; `STRATEGY_FRAMEWORK.md:59` |
| `strategies.regimes.<name>.components[]` | list | `{id, class, params, weight, lookback?, history_transforms?, transforms}` | V2(n/a here — no cross-ref needed for strategy engine ids), V3/V4 (transform ops), V5 (history-ops-before-scalar-ops order), V6 (lookback ≥ transform min_periods), V8 (weight numeric, per-regime total > 0) | `validate_config.py:102-165,259-278`; `strategy_engine.py:32-38,143-162` |
| `regime_detector`/`strategies` component `params` | dict | class-specific (see component table below) | **NOT validated** — a typo'd key is silently ignored and the class default is used | `STRATEGY_CONFIG_REFERENCE.md:108` (explicit warning) |
| `aux_feeds` (top-level) | list | `["funding_rate"]`, `["fear_greed"]` (deny-by-default; unrecognized name raises `UnrecognizedAuxFeedError`) | none in `validate_config.py`; enforced in `prescreen_signal.py::_merge_aux_feeds()` only | `STRATEGY_CONFIG_REFERENCE.md:202-235` |
| `symbols` / `timeframe` / instrument-set | **absent from strategy_config.json entirely** | n/a | n/a | see §Gap below |

Module-map correction: `CLAUDE.md`'s module map says "Config validator V1-V10"; the file has
**V11** too (`validate_config.py:280-290`, `min_allocation_change`), undocumented in that map.

### Component catalog (24 classes, `strategies/strategy_components.py`)

Confirmed exactly 24 `class ...(SubStrategyComponent)` definitions (`grep -c` match to
`CLAUDE.fork.md`'s figure). These are **live** — instantiated by `_load_class(c["class"])` in
both `ConfigDrivenRegimeEngine.__init__` (`regime_engine.py:36`) and
`ConfigDrivenStrategyEngine.__init__` (`strategy_engine.py:33`) — distinct from the dead
`SubStrategyComponent.generate_forecast()`/`CompositeStrategy`/etc. orchestration classes the
main `CLAUDE.md` correctly flags as unreachable. No contradiction between the two docs: the
*leaf* component classes are live; the *composite orchestration* classes above them are dead.

Full params table already exists and is accurate: `STRATEGY_CONFIG_REFERENCE.md` §4
(lines 148-235), cross-checked against every `self.parameters.get(...)`/`params.get(...)` call
in `strategy_components.py` (24/24 classes match). Three components declare
`consumes_feeds` (aux-feed requirement): `FundingRateMeanReversionComponent` →
`("funding_rate",)` (`strategy_components.py:704`), `FearGreedContrarianComponent` →
`("fear_greed",)` (`:790`), `WhaleLargeTradeImbalanceComponent` →
`(WHALE_LT_IMBALANCE_COLUMN, WHALE_ATTESTED_COLUMN)` (`:1334`) — the last is reserved/gated,
not in `FEED_REGISTRY` (`STRATEGY_CONFIG_REFERENCE.md:222-230`).

### Transform ops (`strategies/registry.py::TRANSFORM_OPS_REGISTRY`)

**15**, matching the main `CLAUDE.md`'s corrected count (`registry.py:51-87`): `identity`,
`percentile`, `negate_percentile`, `zscore`, `ratio_to_mean`, `ema` (history-based, must come
first); `scale`, `threshold_filter`, `clip`, `sigmoid`, `negate` (scalar); `vol_normalize`,
`vol_adjusted`, `price_normalized`, `volume_filter` (data-aware). **None of the 15 does
cross-component forecast standardization/scaling** — `scale` and `clip` are the closest
(single-component, config-supplied factor/bounds), `zscore` is per-component-history-only. This
is relevant to E-060/card F's "existing transform pipeline handles standardization" claim: it
is per-component only; nothing in the registry normalizes one component's output against
another's, which the design guide (if it composes blocks with disparate output scales) will
need to state explicitly rather than assume.

### The "none" assignment (task 5)

`strategies.regimes.<name>: null` is a documented, deliberate, first-class pattern — "stay
flat, forecast 0.0" — not a silent gap (`STRATEGY_CONFIG_REFERENCE.md:94`,
`STRATEGY_FRAMEWORK.md` invariant 6, `strategy_engine.py:139-141`,
`regime_engine.py:98-101,113-120` return `True`/no-op when a regime key is absent from
`_components`). The one thing the engine *forbids* is the combination validate_config.py's
**V10** exists for: a fully-ungated detector (`components=[]` AND `rules=[]`, so every bar
resolves to `default_regime`) pointed at a null `strategies.regimes` entry — that produces a
config that silently forecasts 0.0 forever with no error anywhere except the validator.
`backtest-engineering/SKILL.md`'s "Ungated hypotheses" section (lines 125-196) already encodes
this pattern in prose for the LLM; the design guide inherits this section largely verbatim.

## 2. What the pipeline carries today (present-structured vs prose-only vs absent)

Schema top-level properties (`workflow_artifacts/schemas/*.schema.json`, read directly):

- **`hypothesis_card.schema.json`**: `hypothesis_id, thesis, rationale, edge_source,
  signal_concept, target_market, timeframe, assumptions, expected_failure_modes,
  library_lookup, power_parameters`. **No `class`/`weight`/`transforms`/`regime_detector`
  field anywhere, and no `pass_rule`/`criteria` field.** `target_market`/`timeframe` are the
  only two fields that map onto anything the engine consumes, and neither maps onto
  `strategy_config.json` — the engine's schema has no symbol/timeframe key at all (§Gap).
- **`expanded_hypothesis_card.schema.json`**: `base_hypothesis_id, expanded_variants,
  regime_specific_variants, reverse_hypothesis, alternative_data_candidates,
  behavioral_features`. `expanded_variants` entries are prose (`diversity_axis`,
  `edge_source_compatibility`, etc. — `innovation-expansion/SKILL.md:93-97`), not config
  patches.
- **`backtest_spec.schema.json`**: `hypothesis_id, status, config, config_rationale,
  selected_variant_id, component_gap`. **`config` is where the full bot-config vocabulary
  first appears, structured, today** — its own schema entry says only `"type": "object",
  "nullable": true`, deferring to `"trading-bot/strategy_config.schema.json"` for real
  validation. **That file does not exist anywhere in the repo** (`find`/`grep` both empty) —
  the actual enforcement is `trading-bot/tools/validate_config.py`, called from code, not from
  a schema. This matches `strategy-research/CLAUDE.md`'s standing note: "schemas are declared
  but not enforced."

Skill files, matching the schemas exactly:

- **`hypothesis-design/SKILL.md`** (341 lines, Step 1a today): zero mentions of `pass_rule` or
  `criteria` — it authors `edge_source`/`signal_concept`/`power_parameters` prose only. This
  is the direct, corpus-independent confirmation of Part 1 finding #2 (pass_rule is never
  authored at Step 1 today) and of card N (a pass-through rule "is needed after all, at 1a").
- **`innovation-expansion/SKILL.md`** (195 lines, Step 2 today): variant fields are
  `diversity_axis`, `edge_source_compatibility`, category tags — prose descriptions, not
  config-field patches. Confirms card K's "today's loose variant descriptions... don't map
  onto config fields."
- **`backtest-engineering/SKILL.md`** (228 lines, Step 5-ish today): this is **already** the
  real config-authoring skill — it produces `backtest_spec.yaml.config`, cites
  `STRATEGY_CONFIG_REFERENCE.md` as its own required reading, and its "Forbidden" section
  (lines 205-227) already hand-encodes V9's default_regime restriction and the
  "no invented component classes" rule in prose. E-056's `strategy-config-authoring/SKILL.md`
  is substantially this file relocated from Step 5 to Step 1b, not a new invention.

### Design-guide seed gaps (what `STRATEGY_CONFIG_REFERENCE.md` + `WORKFLOW_CAPABILITIES.md`
### lack for an LLM to write a complete config unaided)

- **Symbol/timeframe/instrument-set has no field in `strategy_config.json` at all.**
  Confirmed by reading a real spec-ready config (`runs/run_059/artifacts/backtest_spec.yaml`):
  its `config` block is exactly `{regime_detector, strategies, aux_feeds,
  significance_methodology}` — no symbol, no timeframe. Today, symbol/timeframe live only in
  `hypothesis_card.yaml.target_market`/`.timeframe` and get threaded into a separately-
  generated **protocol** file (`run_context.yaml: protocol: funding_mr_daily_retest_v1.json`,
  `_ensure_protocol_from_constraints`), per Part 2 decision **E** ("Protocol = time + cost
  only. Symbol, universe, timeframe are design fields."). Card K's target design — 1b's config
  carrying "instrument set as one symbol or a named universe" — is a **new field the engine's
  config schema does not have today**, not a relocation of an existing one. This is the single
  largest gap the design guide has to close, and `STRATEGY_CONFIG_REFERENCE.md` (owned by
  `regime_engine.py`/`strategy_engine.py`/`registry.py`, none of which read a symbol field)
  gives no guidance on it because the engine itself has no opinion on symbol — that's supplied
  externally by the backtest harness/launcher.
  `WORKFLOW_CAPABILITIES.md` (68 lines) is a thin FAQ pointing back to
  `STRATEGY_CONFIG_REFERENCE.md`; it adds no vocabulary of its own.
- `params` key typos are silently ignored (documented warning, not enforced) —
  the design guide needs a positive, per-class required/optional param list (already in
  `STRATEGY_CONFIG_REFERENCE.md` §4) that the LLM is instructed to match exactly, since nothing
  downstream will catch a misspelling.
- Regime-rule condition syntax (`op: gte|gt|lte|lt|between`) uses a **different vocabulary**
  from `verdict_criteria_evaluator.py`'s comparator set (`>=, >, <=, <, ==` — see §4). A design
  guide that also touches criterion authoring (even by cross-reference) should flag this is not
  the same syntax, so an LLM doesn't transplant one into the other.
- No worked example exists for `score` or `score_product` mode's `regimes.<name>.components[]`
  in isolation from `STRATEGY_CONFIG_REFERENCE.md` itself — that file is in practice the whole
  seed; nothing else adds coverage.

## 3. Measuring the guessing (corpus, denominator stated)

**40 runs** carry both `hypothesis_card.yaml` and `candidate_strategy_config.json` under
`strategy-research/runs/run_*/artifacts/` on this checkout, 2026-09-20 (listed:
run_009–run_035, run_039, run_041–run_044, run_047, run_048, run_050, run_053, run_054,
run_057, run_059, run_060). The delivery plan's own S1 brief states 39 — one run was added to
the corpus between that count (2026-09-17/19) and this measurement; not investigated further,
noted as a live discrepancy, not a bug.

Method: for each config field, checked whether its value (or, for component `class`, the bare
class name) appears as a case-insensitive substring anywhere in that run's
`hypothesis_card.yaml` + `expanded_hypothesis_card.yaml` text. This is a **textual-echo proxy
for provenance, not true provenance** — a value could coincidentally match without being
"sourced," and a genuinely-derived value (e.g. a scaling_factor computed from a stated
threshold) won't match textually. Treat percentages as an upper bound on how much really has a
traceable source, not an exact figure.

| Field kind | Sourced / Total | % |
|---|---|---|
| `aux_feeds` | 8/8 | 100% |
| `regime_detector.components[].class` | 0/57 | **0%** |
| `regime_detector.default_regime` | 14/40 | 35% |
| `regime_detector.mode` | 6/40 | 15% |
| `regime_detector.rules` (non-empty) | present in 25/40, never substring-checked (numeric thresholds) | — |
| `strategies.regimes.*.components[].class` | 18/43 | 42% |
| `strategies.regimes.*.components[].weight` | 10/43 | 23% |
| `strategies.regimes.*.components[].transforms` | 6/43 | 14% |
| `strategies.regimes.*.components[].lookback` (when set) | 2/24 | 8% |
| `strategies.regimes.*.components[].params.scaling_factor` | 24/43 | 56% |
| `strategies.regimes.*.components[].params.period`/`window`/`k` (numeric window sizes) | mostly 75–100% | high — these numbers do tend to appear in the card's `power_parameters`/rationale prose |
| `strategies.warmup` | 10/40 | 25% |
| Top-level extra keys not in `{regime_detector, strategies, aux_feeds}` | `significance_methodology` (4/40), `_comment` (2/40) | invented at config time, no card equivalent field exists |

Headline: **component `class` selection is 0% textually sourced** (the card never contains a
Python dotted path — expected, since it's prose vs. code, but it does mean the class → thesis
mapping is entirely the LLM's unconstrained inference at authoring time today) and **transform
pipeline choice / weight / lookback overrides are the least-sourced numeric fields** (14–23%),
consistent with card K's framing that this is exactly "the scaffolding an LLM adds" the design
guide must constrain. Window-size-type params (`period`, `k`, `window`) are comparatively
well-sourced because `power_parameters` prose in the card tends to state them explicitly
(e.g. run_059's `n_bars`/flip-count narrative).

### `_record_variant_selection` instrument/timeframe resolution (task 3 second half)

`workflow/run_phase1_research.py::_record_variant_selection` (`:1939-1952`) tries, in order:
variant-level `target_market` → `target_markets` → `instrument`, falling back to
`hypothesis_card.get("target_market")`; timeframe: variant-level `timeframe` →
`timeframe_expanded` → `timeframe_original`. Its `resolved_instrument` is then passed through
`_coerce_scalar_instrument` (`:1832-1877`), whose dict-shape fallback tries
`_INSTRUMENT_SINGLE_ASSET_KEYS = ("asset", "symbol", "instrument", "target_market")`
(`:1829`). **Union of all distinct key names tried across both functions: `target_market`,
`target_markets`, `instrument`, `asset`, `symbol` — exactly five**, matching card K's "five
different key names" claim precisely (I could not find that exact phrase's arithmetic spelled
out anywhere else, so this derivation is new in this session). Measured occurrence in the real
corpus (`hypothesis_card.yaml` + `expanded_hypothesis_card.yaml`, all 60 run dirs, not just the
40-run denominator): `target_market` 56 files, `target_markets` 2 files, `asset` 4 files,
`instrument` 0 files, `symbol` 0 files. **3 of the 5 keys are ever actually used; 2
(`instrument`, `symbol`) exist in the code with zero real occurrences.**

## 4. Pass-rule authorship path (E-059-adjacent, characterized as-is)

Both real materialization paths in `workflow/run_campaign.py` copy `pass_rule` **verbatim**
from an operator-authored brief; neither authors it at Step 1:

- **Fresh launch**, `_materialize_run` (`:298-365`): `pre_registration["pass_rule"] =
  evaluation.get("pass_rule")` where `evaluation = brief.get("evaluation") or {}` (`:323,334`)
  — `brief` here is the operator/queue-registered brief, not an LLM stage output.
- **Refinement child**, `_materialize_refinement_run` (`:456-524`): identical extraction,
  `pre_registration["pass_rule"] = evaluation.get("pass_rule")` (`:479`), from an
  operator-authored refinement brief (`brief["evaluation"]["pass_rule"]`), copied "verbatim"
  per its own docstring (`:460`) — this is the **operator-authored** refinement path (via
  `refinement_brief_path`/B1), distinct from the **internal LLM routing's own
  `proposed_brief.yaml`** path the roadmap review's finding #2 also names (`_route_refine`,
  not read in this session — out of scope for S1's exact citations, flagged under "Not
  determined").

`tools/verdict_criteria_evaluator.py` criterion dict shape, read end to end (925 lines):
`_evaluate_one_criterion` (`:217-276`) reads `{metric, comparator, threshold,
per_symbol_threshold?, null_handling?}` — matches the dispatch's expected shape exactly, with
one addition (`per_symbol_threshold`, a dict of `symbol -> threshold` overriding the
pooled/global `threshold`). Comparators (`_VALID_COMPARATORS`, `:51`): **`>=, >, <=, <, ==`**
— note this is a **different token vocabulary** from `regime_detector.rules`' comparator set
(`gte, gt, lte, lt, between` — `regime_engine.py:161-170`); a criterion-menu author must not
assume these are interchangeable. `null_handling` has exactly one recognized value in code,
`"fails_threshold"` (`:233,268`); anything else (including absent) yields `SPEC_ERROR`, not a
silent pass — i.e. every criterion must explicitly declare its null policy or the evaluator
refuses to grade it.

Dict-shaped `pass_rule` count, re-measured directly: **10** `pre_registration.yaml` files in
the corpus, **3** with a dict-shaped `pass_rule.criteria` list — matches the roadmap review's
figure exactly. Their 3 distinct `metric` values: `median_sharpe` (3 uses),
`max_abs_drawdown_pct` (3), `zero_trade_slot_pct` (2).

**39** `verdict_interpretation.yaml` files exist; their `criteria_summary` entries are **free
prose**, not structured `{metric, ...}` dicts (no file in the corpus has a literal `metric:`
key inside `criteria_summary`) — 104 total entries measured. Extracting the text before the
first comparison operator in each `criterion` string gives a sprawl of near-duplicate and
one-off phrasings, e.g. (case as found): `sharpe`/`Sharpe`/`V1 sharpe`/`V1 Sharpe` (≈11
variants of one concept), `win_rate`/`Win rate`/`V1 win_rate` (≈9), `trade_count`/`Trade
count`/`min_trade_count` (≈7), `max_drawdown_pct`/`Max drawdown` (≈6),
`regime_frequency`/`Regime frequency` (≈5), plus genuinely non-metric, non-scale-free entries
that are pure narrative checks — `"ER/VR no lookahead"`, `"No look-ahead in ATR"`, `"Reverse
hypothesis, regime-specificity, parameter monotonicity"`, `"Cost drag quantification:"`. This
is raw enumeration only, not a proposed menu — handed to E-046b as instructed.

## 5. Consumers and change classification (task 6)

- **`tools/build_exclusion_digest.py`**: reads `hypothesis_card.yaml.target_market` (via
  `extract_instruments`, `:176-192`, explicitly list/comma-string/dict-tolerant) and
  `.timeframe`; `composition_fingerprint()` (`:227-278`) reads
  `candidate_strategy_config.json`'s `strategies.regimes.*.components[]` shape directly
  (class/params canonicalized). **Additive under E-056 S2**, provided the config's
  `regime_detector`/`strategies`/`aux_feeds` shape is preserved (it is, per card K: "5a needs
  no LLM... the three patched configs are assembled" using the same validator) — this reader
  doesn't care *who* wrote the config, only its shape.
- **`tools/anti_adjacency_gate.py`**: same shape dependency — `layer2_digest_check` /
  `evaluate_candidate` (`:406-538`) take a `hypothesis_card.yaml`-shaped dict plus an optional
  `candidate_strategy_config.json`-shaped file for the fingerprint. **Additive**, same
  reasoning; Layer 1 (KB text match) is untouched by anything E-056 changes.
- **Schema validators**: `hypothesis_card.schema.json` would need `target_market`/`timeframe`
  fields retained (already does) plus, if card N's pass-through rule requires the schema to
  optionally carry a pre-attached config/criteria for already-formed candidates, a new optional
  block — **additive** (a new optional property, nothing existing removed).
  `backtest_spec.schema.json`'s `config` property becomes largely vestigial once 1b writes the
  config directly and 5a is a pure `tool:` patch-apply stage — this is where a **breaking**
  change actually lands: the stage that currently *produces* `config` (`backtest_engineering`)
  is retired as an LLM stage per the delivery plan (slice 3), so any consumer that assumes
  `backtest_specification` is where a config is first authored (rather than merely
  assembled/patched) needs updating. Not fully enumerated in this session — flagged under "Not
  determined."
- **`trading-bot/tools/validate_config.py`**: unaffected either way — it validates the shape
  wherever it's called from (`backtest_specification` today, a new `tool:`-stage `5a` under the
  redesign) and has no opinion on which stage calls it.

## 6. S2 proposal (itemized, per dispatch task 7)

**Design guide (1b), build items:**
1. New `docs/STRATEGY_DESIGN_GUIDE.md` (or in-place rewrite of
   `STRATEGY_CONFIG_REFERENCE.md`) — additive/rewrite, no bit-identity implication (docs only).
   Content: everything in the existing reference file, verbatim where accurate, plus:
   (a) the new instrument-set field/manifest contract (§2 gap — genuinely new schema surface,
   needs its own validator addition, not just doc text); (b) an explicit statement that
   `params` keys are unchecked and must match the catalog exactly; (c) a note that regime-rule
   comparators (`gte/gt/lte/lt/between`) and criterion-menu comparators (`>=/>/<=/</==`) are
   different vocabularies.
2. `strategy-config-authoring/SKILL.md`, adapted from `backtest-engineering/SKILL.md`'s
   existing "Forbidden"/"Ungated hypotheses" sections (already ~80% of the needed content) —
   pre-registered success signal: byte-diff the retired skill's rule content against the new
   skill's rule content and confirm no rule is silently dropped.
3. `strategy_config_authoring` stage added to `STAGE_CONFIGS`, flagged off by default
   (`orchestrator.config_direct_authoring.enabled`) — bit-identity: flag-off run produces a
   byte-identical stage graph and artifact set to today (delivery plan's own stated test
   pattern, `tests/test_e054_stage_wiring.py`-style). Pre-registered success signal: one flag-on
   run produces a `validate_config.py`-passing config with a manifest, and the flag-off suite
   still passes unchanged.

**Pass-through rule (1a), build items:**
1. Encode card N literally: any candidate entering with an existing config + criteria (reader
   proposal, composition brief, un-parked idea) causes 1a/1b to run a **completeness check
   only** (config present, validates, manifest paths resolve, criteria menu-shaped) rather than
   re-authoring. Bit-identity: a pass-through candidate's config must be byte-identical
   before/after 1a/1b when nothing is missing — pre-registered signal: diff the config file
   pre- and post-pass-through on one synthetic already-formed candidate.
2. `research_brief.yaml` gains the carrier field for "this is already-formed" (exact field name
   not decided in this session — flagged below).

## Not determined

- Exact mechanics of the **internal LLM routing's own `proposed_brief.yaml`** pass_rule path
  (`_route_refine`, cited in the roadmap review's finding #2 but not read in this session) —
  only the two operator-authored materialization paths were traced.
- Whether `research_brief.yaml`'s pass-through carrier field already has a natural home (e.g.
  an existing but unused key) — not checked against the live schema for that file.
- Full enumeration of every `backtest_spec.schema.json`/`pre_registration.yaml`
  consumer beyond the four named in the dispatch (`build_exclusion_digest.py`,
  `anti_adjacency_gate.py`, schema validators, `verdict_criteria_evaluator.py`) — a full
  grep-based consumer survey (every `.py` file under `workflow/`/`tools/` that opens these
  artifact files) was not run; only the four named files were read.
- Whether the one-run corpus-size discrepancy (39 in the delivery plan vs. 40 measured here) is
  a new run added since, a different denominator definition, or a counting difference — not
  investigated.
- `strategies.regimes.*.components[].params.<name>` sourcing percentages above 56% were
  spot-checked for a few field names (`period`, `k`, `window`) but not audited row-by-row for
  false positives from the substring-match method (e.g. a `period: 20` could match "20%" in
  unrelated prose) — treat the >90% rows as an upper bound, not a verified rate.
- Whether the score/score_product regime-scoring `divisor` key and `min_score`/`min_margin`
  need their own design-guide worked example beyond `STRATEGY_CONFIG_REFERENCE.md`'s existing
  one — not assessed against S2 authoring difficulty.

---

## Paste-ready Linear comment

**E-056 S1 — characterization complete (2026-09-20).** Worktree note: this checkout was 2
commits behind master and missing the E-056 dispatch's required reading
(`roadmap_review_2026-09-18.md`, `delivery_plan_v26.md`, `engineering_roadmap.html`, all added
by `844e6a17`); read via `git show 844e6a17:<path>` without merging. Full findings:
`strategy-research/engineering/roadmap/E-056/S1_FINDINGS.md`.

Headline results:
- Bot-config vocabulary table built (`regime_detector`/`strategies`/`aux_feeds`, all 24
  component classes, all 15 transform ops) — `STRATEGY_CONFIG_REFERENCE.md` is ~99% accurate
  and is the design guide's real seed. **Biggest gap: symbol/timeframe/instrument-set has no
  field in `strategy_config.json` at all today** — card K's "instrument set as one symbol or a
  named universe" in 1b's output is new schema surface, not a relocation.
- Corpus measured on 40 runs (delivery plan said 39 — one-run drift, unexplained): component
  **`class` selection is 0% textually traceable** to the hypothesis card; transform-pipeline
  choice, weight, and lookback overrides are 8–23% traceable; window-size params (`period`,
  `k`, `window`) are 75–100% traceable. This is the scaffolding the design guide must constrain.
- The "five different key names" for variant instrument resolution (card K) is confirmed
  exactly: `target_market, target_markets, instrument, asset, symbol` across
  `_record_variant_selection` + `_coerce_scalar_instrument`. Only 3 of 5 ever occur in the real
  corpus; `instrument` and `symbol` are dead code paths (0 occurrences each).
- `pass_rule` is copied verbatim from the operator brief on both real materialization paths
  (`run_campaign.py:334,479`) — never authored at Step 1 today, confirming Part 1 finding #2
  independently of the roadmap review.
- `verdict_criteria_evaluator.py`'s criterion shape confirmed:
  `{metric, comparator, threshold, per_symbol_threshold?, null_handling?}`, comparators
  `>=/>/<=/</==` — a **different vocabulary** from regime-rule comparators (`gte/gt/lte/lt`).
  10 `pre_registration.yaml`, 3 dict-shaped, 3 distinct metrics used. 39
  `verdict_interpretation.yaml` files' 104 criteria are free prose with no structured `metric`
  field — wide, messy near-duplicate phrasing, raw list handed to E-046b.
- `trading-bot/strategy_config.schema.json`, which `backtest_spec.schema.json` cites as the
  real validator, **does not exist anywhere in the repo** — actual enforcement is
  `trading-bot/tools/validate_config.py`, called from code. Consistent with
  `strategy-research/CLAUDE.md`'s "schemas declared but not enforced" note.
- Consumer impact: `build_exclusion_digest.py` and `anti_adjacency_gate.py` are additive (shape
  unchanged, only who authors it changes); `backtest_spec.schema.json`'s `config` property
  becomes vestigial once 1b authors directly — the one place a real breaking-change audit is
  still needed (not completed this session).

Not determined (see file for full list): the internal-LLM-routing `proposed_brief.yaml`
pass_rule path; full consumer survey beyond the four named files; root cause of the 39-vs-40
corpus count drift.
