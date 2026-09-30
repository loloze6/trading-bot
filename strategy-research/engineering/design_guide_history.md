# Design guide: history and engineering notes

Engineering history moved out of `strategy-research/docs/STRATEGY_DESIGN_GUIDE.md` and
`strategy-research/docs/COMPONENT_CATALOG.md` when they were rewritten for their real reader (a closed-book LLM that
designs strategy configs) under D-054 (`engineering/DECISION_LOG.md`, 2026-09-30). **Nothing here is an input to any
LLM stage.** The guide and the catalogue carry only what a designer needs; this note keeps provenance, the review
fixes, the plumbing, and the record of what the old text got wrong.

## Provenance of the old guide

- Sections 1-6 of the old `STRATEGY_DESIGN_GUIDE.md` were carried over near-verbatim from
  `trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md`, built for E-056 S2 Slice 3a
  (`engineering/roadmap/E-056/S2_FINDINGS.md` §6/§9). The old header said the reference was authoritative where the
  two disagreed, because it was read directly by `backtest-engineering/SKILL.md` and lived next to the engine code
  (`regime_engine.py`, `strategy_engine.py`, `registry.py`).
- Section 7 was new in that slice: an instrument-set proposal (7a), the component-existence check (7b), the
  `block_manifest.yaml` contract (7c, built 2026-09-24), a vocabulary callout (7d) and the ungated pattern folded from
  `backtest-engineering/SKILL.md` (7e).
- The old header called config-direct authoring "Slice 3b, not yet built". It is built.
- D-054 deleted `trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md` and its sync test
  (`trading-bot/tests/test_component_reference_sync.py`; `strategy-research/tests/test_design_guide_in_sync.py` covers
  the same check on the catalogue) and folded `docs/WORKFLOW_CAPABILITIES.md` into the guide.
  The guide is now the single source; nothing is "authoritative over" it.

## What the old text got wrong (corrected in the rewrite)

Stale or false statements found while verifying against the code on 2026-09-30:

1. The checklist said `strategies.warmup` must equal the value in the startup log. It has no effect:
   `main_strategy.py` calls `set_warmup(required_bars)` right after construction.
2. "A `lookback` override is NOT validated against the transforms' minimum periods" was stale. Validator V6 enforces
   it and `AdvancedStrategy.__init__` raises on any violation.
3. The `aux_feeds` section said the key is consumed by `prescreen_signal.py::_merge_aux_feeds()`. That file no longer
   exists. The key is read only by `data_availability_gate.py`, `decide_next.py` and `composition.py`; the engine
   gets feeds from each component's `consumes_feeds` plus `FEED_REGISTRY`
   (`strategies/strategy_engine.py` `required_feeds()`, `core/backtester.py` required-feed check,
   `core/launcher.py` passing `FEED_REGISTRY` as `extra_feeds`).
4. The ungated section said `default_regime` MUST be `"unknown"` because `is_ready()` read the regime before
   `classify()` ran. `main_strategy.is_ready()` now classifies first (F7 fix). `validate_config.py`: any of the four
   names is fine for a fully ungated detector; V10 still forbids pointing it at a null regime.
   (`backtest-engineering/SKILL.md` and `strategy-config-authoring/SKILL.md` still carry the old "MUST be unknown"
   text in their "Ungated hypotheses" and "Forbidden" sections, which are pinned byte-identical to each other by
   `test_e056_config_direct_authoring.py`; that is a separate slice.)
5. Header and provenance text ("Slice 3b, not yet built"; "STRATEGY_CONFIG_REFERENCE.md is authoritative") were stale.
6. "Component spec (both engines)" implied `weight`, `lookback` and `history_transforms` apply to regime detector
   components. They are ignored there.
7. Checklist item 1 said missing rule ids fail at startup. Only veto ids do; a rule condition naming a missing id
   silently evaluates false (V2 catches it).
8. A line said composition work was not built yet. `tools/composition.py` exists and is flag-enabled; the fact that
   the manifest has no instrument key still holds.
9. Component variant patterns were wrong for the three breakout/band components: `DonchianBreakoutComponent` with
   `scaling_factor` -20 is an anti-breakout (mean reversion), not a "lower-band breakdown", and a longer `period`
   does not give "fewer, higher-conviction breaks" (the output is the continuous position of the close in its range,
   never an event); `KeltnerBreakoutComponent` with `scaling_factor` -20 is a pure sign flip on every bar, and
   `atr_multiplier` only rescales magnitude; `RSIPullbackComponent` `long_only` is positive whenever RSI < 50, not
   "only buys dips"; `EMASpreadComponent` is a continuous spread, not a crossover event.
10. Catalogue rows that misdescribed their component: `VolumeExpansionHedgeComponent` fires on low-volume up-moves
    only (range (-`sf`, 0]); `MomentumDivergenceComponent` ignores `scaling_factor` and its product is positive for
    agreement in either direction; `VolatilityFromStdDevComponent` and `PriceEvolutionOnPeriodComponent` ignore
    `scaling_factor`; the feed-based components return 0.0 (not NaN) for a missing column and test the hour only.

## CODE-REVIEW FIX (2026-09-21), carried from the old section 7

The old section numbering was reshuffled after an adversarial review found two defects in the original draft:
(1) the guide's own checklist claimed `default_regime` creates a gate-bypass risk in `score_product` mode identical
to `threshold_rules` mode. `_classify_score_product` (`trading-bot/strategies/regime_engine.py`) never reads
`self._default_regime`; its gate-fail path is hardcoded to `MarketRegime.UNKNOWN`. `validate_config.py` V9 still
applies the same restriction to `score_product` mode whenever `rules` is non-empty, which is a pre-existing
over-strictness (a `score_product` config normally has no `rules`, so it rarely fires). Do not read V9 passing or
failing as evidence about `score_product`'s real gate behaviour. (2) Three cross-references pointed to "7b" for V12
documentation while 7b was an unrelated proposal; a real V12 section was added.

## Old section 7a: instrument-set / symbol / timeframe field, PROPOSED, NOT BUILT

The config schema has no symbol, timeframe or instrument-set key (top-level keys: `regime_detector`, `strategies`,
`aux_feeds`). E-056 S1 flagged this as the largest real gap in the reference documentation and the characterization
session (`S2_FINDINGS.md` §6) confirmed it. The open question, deliberately unresolved, was whether such a field would
be a new top-level sibling or live elsewhere. Since the manifest contract was built (2026-09-24) it forbids any
coin/instrument field (a validated block is usable on any coin). No check in `validate_config.py` reads such a field.
The guide now states the consequence as a limit ("What the config cannot express") instead of a proposal.

## Old section 7b: component-class existence check (V12), built with Slice 3a

Every `class` in `regime_detector.components[]` and `strategies.regimes.*.components[]` is checked at
`validate_config.py` time with `strategies.registry._load_class`, the function the engine calls at startup, so V12
fails on exactly the configs the engine would refuse to start on. Before V12 an invented or misspelt class passed
validation and failed only at engine startup, after a full backtest had been launched and its data fetched. Verified
against the full real corpus (every `candidate_strategy_config.json` under `strategy-research/runs/run_*/` at the
time): zero currently-passing real configs newly failed, so V12 shipped unconditionally, with no flag. V12 checks that
the path imports to a class; it does not check that the class is a component.

## Old section 7c: who checks the manifest

One implementation, `strategy-research/tools/block_manifest.py`, used everywhere the manifest is read:

- right after stage 1b (`determine_post_strategy_config_authoring_route`), against `backtest_spec.yaml`'s config and
  before `innovation_expansion` runs: a missing or invalid manifest sends 1b back once with the error in its handoff;
  a second failure stops the run. A stale manifest is deleted when 1b starts, so a pass never inherits an earlier one;
- the tool-only `backtest_specification` stage (5a) re-checks it against 1b's base config before building any variant
  (backstop; stops the run). Per variant, only block paths must resolve (a variant may change scaffolding); one whose
  patch removes a block path is marked `not_tested` (`manifest paths unresolved`);
- `tools/block_registry.py` checks it again against the tested base config when a validated run registers its block
  (`config_fragment` is the values at `block.config_paths`).

`workflow_artifacts/schemas/block_manifest.schema.json` documents the same shape (the shape part of rules 1-3) and
`tests/test_e056_1b_block_manifest.py` keeps schema and code in agreement; the same test runs `check_manifest` on the
first ```` ```yaml ```` block starting with `block:` in the design guide, so that block must stay first and valid
against the ungated RSI base config in that test. A pass-through candidate's `manifest` field (hypothesis-design
IMPROVEMENT 08) is written through verbatim and checked the same way; `hypothesis_card.schema.json`'s `manifest` field
`$ref`s the manifest schema, so a malformed one is also caught at the card.

## Old section 7d: comparator-vocabulary divergence

`regime_detector.rules` and `vetoes` use `gte`/`gt`/`lte`/`lt`/`between`. A separate vocabulary lives in
`strategy-research/tools/verdict_criteria_evaluator.py` (`_VALID_COMPARATORS`: `>=`, `>`, `<=`, `<`, `==`), used for
campaign pass/fail criteria evaluated against `config/criterion_menu.yaml`: a different config surface from
`strategy_config.json`. They are not interchangeable: `">="` in a regime rule is an unknown op (silently false), and
`"gte"` in a criterion is not in `_VALID_COMPARATORS`. Confirmed by E-056/E-046b S1 (`S2_FINDINGS.md` §6 item 3,
`S1_FINDINGS.md`, `verdict_criteria_evaluator.py`). The guide keeps only the regime-rule half (write `gte`, not `>=`).

## Old section 8: the sync test

`strategy-research/tests/test_design_guide_in_sync.py` compared the old guide's component catalogue against
`^class X(SubStrategyComponent):` in `trading-bot/strategies/strategy_components.py` (set equality, row count, no
duplicates; the class count, 24, pinned). It now does the same against `COMPONENT_CATALOG.md` between its
`CATALOG:START` / `CATALOG:END` markers and additionally requires every row's Kind to be one of the four kinds
(graded, on/off, constant, regime measure) and pins the D-051 assignment. `test_design_guide_examples.py` runs every
`<!-- example: name -->` JSON block of the guide through `validate_config.validate()` and the real strategy engine on a
seeded synthetic price path and asserts the property the guide states.

## Block combiner internals (E-060 S3a / S3b)

The guide documents usage only. Internals, from `strategies/strategy_engine.py`:

- Each block runs as it was validated: its own source timing (`required_bars`, `warmup`, `buffer_bars`: its components
  and gate see only the last `buffer_bars` bars, with calculated columns recomputed on that slice, so a longer window
  needed by another block never changes what it computes) and its own gate (the source `regime_detector`, run by its
  own `ConfigDrivenRegimeEngine`). On a bar its gate classifies into regime r, its final forecast is part r (weights
  normalised within the part, clipped +/-20); in any other regime, or before its source would be ready, it abstains
  (contributes 0 and records nothing).
- Standardisation is scale-only and past-only: `target x v_t / mean(abs(v))` over the block's last `window` PAST active
  values (the current value is not in its own denominator), no mean subtraction (a block's directional bias survives
  and a zero stays zero), capped at +/-20, 0.0 when the past mean is about 0, and 0 until `min_periods` past values
  exist. Regime forecast = sum over blocks of (W_b / sum W) x block value, clipped +/-20. `get_required_periods()`
  includes each block's `required_bars + warmup + min_periods`.
- A non-finite block value raises `BlockCombinerError`; it never reaches an allocation and is never replaced by 0.0.
- Why it cannot leak: every quantity at bar t comes from the window ending at t and from block values of bars before
  t; nothing is estimated once over a period. A regime without these keys never enters this code.
- `weight_schedule` (S3b): an entry is a set of constants fixed before the run; `tools/composition.py` estimates each
  entry only from data strictly before its `from` date, and the engine applies it only to bars on or after `from`
  (00:00 UTC). A config without the key never enters it.

## `aux_feeds` history (W14 and the feed pointers)

- Before dispatch W14 step 2 the top-level `aux_feeds` key, read by `prescreen_signal.py` (since deleted), silently
  dropped an unrecognised name; W14 made it deny-by-default (`UnrecognizedAuxFeedError`). With `prescreen_signal.py`
  gone that code path no longer exists.
- Live and backtest feeds are driven by explicit `register_feed()` calls, or, for a full backtest, by `FEED_REGISTRY`
  membership passed as `extra_feeds`, and are separately deny-by-default through the `window_seconds` causality
  declaration (`trading-bot/data/ADDING_A_FEED.md` step 2).
- The whale-footprint feeds are in `RESERVED_FEED_REGISTRY` (`data/feed_registry.py::WHALE_FOOTPRINT_FEEDS`); opting in
  by name still needs a committed designation in `campaign_data_policy.yaml` or construction raises
  `ReservedDataError`.
- Working reference configs for the feed-based components: run_041 (`H-041-A`, `strategy-research/runs/run_041/`) and
  run_042 (`H-041-C`, `strategy-research/runs/run_042/artifacts/candidate_strategy_config.json`). The original false
  `component_gap` on funding rate (run_044, 2026-07-04) is why the old guide insisted feed-based ideas were "config
  alone". Under D-051 those components are on/off, so a graded feed-based forecast is now a genuine `component_gap`.

## `strategies.min_allocation_change`, history

It is not a strategy-engine setting: it overrides `RiskManager`'s `min_allocation_change.threshold` control
(`risk/risk_manager.py`) for one strategy's runs (E-055). It is the same gate `config.json`'s
`risk_management.controls.min_allocation_change.threshold` has always set globally (default 0.2, live before the key
existed); the key makes the floor tunable per strategy. See `strategy-research/engineering/improvements/known_divergences.md` section 1.

## `WORKFLOW_CAPABILITIES.md`: what was folded and what was dropped

Folded into the guide: the signal variants achievable by config (sign flip, scaling, parameter ranges, multi-component
ensembles, regime modes and vetoes, `score_product` with divisors), and the rule that an invented component name is
checked against the catalogue before a `component_gap` is emitted. Dropped because it is pipeline-level, not config
design, and is documented elsewhere: the autonomy boundary (holdout execution, capital deployment, campaign restart
after `space_empty`, concurrent writers; see `docs/RUNBOOK.md` and `docs/HALT_RECOVERY.md`). Dropped because it was
false: the "Common confusion" row saying a timeframe with no cache needs no fetch because `CandleBuilder` aggregates
finer data on the backtest path. Finer-to-coarser aggregation is an explicit opt-in (`trading.fetch_interval_seconds`);
without it a missing exact-timeframe cache raises "No historical data" (`docs/DATA_AVAILABILITY.md`, CUL-250).

## Tests and pointers

- `strategy-research/tests/test_design_guide_in_sync.py`: catalogue against the component classes.
- `strategy-research/tests/test_design_guide_examples.py`: every guide example, and the guide's factual claims.
- `strategy-research/tests/test_e056_1b_block_manifest.py`: the manifest example in the guide and in the 1b skill.
- Decisions: D-051 (graded forecasts only), D-052 (regime-gate rule deletion, separate slice), D-053 (a design variant
  keeps the idea), D-054 (this documentation split) in `engineering/DECISION_LOG.md`; findings behind them in
  `engineering/OBSERVATIONS_QUEUE.md` (O-1, O-4, O-7).
