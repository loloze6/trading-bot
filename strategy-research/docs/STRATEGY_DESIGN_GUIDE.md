# STRATEGY_DESIGN_GUIDE.md

**Provenance.** Sections 1-6 below are carried over near-verbatim from
`trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md` (that file is NOT deleted,
rewritten, or retired by this document — it remains the code-owned reference;
this file is additive, built for E-056 S2 Slice 3a per
`strategy-research/engineering/roadmap/E-056/S2_FINDINGS.md` §6/§9). Where the
two disagree in the future, `STRATEGY_CONFIG_REFERENCE.md` is authoritative —
it is read directly by `backtest-engineering/SKILL.md` and lives next to the
engine code it documents (`regime_engine.py`, `strategy_engine.py`,
`registry.py`). Re-sync this file with it if either drifts.

Section 7 (below) is genuinely new content: an instrument-set proposal
(§7a, PROPOSED, NOT BUILT), the component-existence check (§7b, built), the
`block_manifest.yaml` contract (§7c, built 2026-09-24), and vocabulary /
authoring callouts. Read each subsection's own banner before treating it as
current behavior.

Purpose: edit `strategy_config.json` without reading code. Every key, every
option — plus, in §7, what a future config-direct-authoring path (Slice 3b,
not yet built) is expected to add.

## Top-level shape
```json
{
  "regime_detector": { ... },   // → ConfigDrivenRegimeEngine
  "strategies":      { ... },   // → ConfigDrivenStrategyEngine
  "aux_feeds":       [ ... ]    // optional — non-OHLCV columns to merge onto the bar
                                //   DataFrame before any component sees it. See §4a.
}
```

## 1. `regime_detector`
| Key | Type | Default | Meaning |
|---|---|---|---|
| `mode` | `"threshold_rules"` \| `"score"` \| `"score_product"` | `threshold_rules` | Classification algorithm |
| `components` | list | required | Indicator components (see §Component spec) shared by rules/vetoes/scores |
| `vetoes` | list | `[]` | Evaluated FIRST every bar, both modes. First veto whose rules all pass for `consecutive_bars` bars forces its `result` regime |
| `rules` | list | `[]` | threshold_rules mode only. Priority-ordered; first match wins |
| `default_regime` | regime name | `"unknown"` | threshold_rules fallback when no rule matches |
| `regimes` | dict | `{}` | score mode only: per-regime weighted transformed components |
| `min_score` | float | 0.35 | score mode: winner must reach this |
| `min_margin` | float | 0.05 | score mode: winner−runner-up must reach this; else UNKNOWN |

Score mode: each regime's score = Σ(weight × transformed value)/Σweights — a weight-normalized average. Absolute weight magnitudes are irrelevant (only ratios matter); to hit `min_score`, adjust transform output scales, not weights.

Regime names (must map to `MarketRegime`): `trending`, `mean_reversion`, `chop`, `unknown`. Adding a new name requires code (enum + `_REGIME_MAP`) → STRATEGY_EXTENDING.md §C.

### Mode algorithms (vetoes run first in BOTH modes)
**`threshold_rules`** (default): per bar, take each component's latest RAW value; walk `rules` top-down; first rule whose `any_of` matches wins; no match → `default_regime`. Deterministic if/else — use when regime boundaries are absolute thresholds (current production mode).

**`score`**: per bar, for each entry in `regime_detector.regimes`, compute score = weight-normalized average of TRANSFORMED component values; winner = argmax. Winner must satisfy `score ≥ min_score` AND `(score − runner-up) ≥ min_margin`, else regime = `unknown`. Use when regimes compete on relative evidence rather than hard cutoffs. Readiness is stricter: every component history must be FULL (= lookback), vs ≥ 1 entry for threshold_rules. Config shape:

**`score_product`**: per bar, for each regime compute score = Π (transformed_value / divisor) across components; winner = argmax. Same `min_score` / `min_margin` gating as `score` mode. Use when the hypothesis is a PRODUCT of regime indicators (e.g. ER × VR/2.0 ≥ threshold). Each component in `regimes[r].components` accepts an optional `"divisor"` key (default 1.0) to normalize its scale contribution. **Single-regime pattern:** define only the target regime (e.g. `"trending"`); with one regime, margin = 1.0 always, so only `min_score` governs firing. Outside the threshold, returns `unknown`. Does NOT support inversion (fire when score < threshold) or SMA smoothing of the score — those require engine extension. Config shape:
```json
"regimes": {
  "trending": {"components": [
    {"id": "er", "weight": 0.45, "transforms": [{"op": "percentile"}]},
    {"id": "vr", "weight": 0.55, "transforms": [{"op": "percentile"}]}
  ]},
  "mean_reversion": {"components": [
    {"id": "vr", "weight": 1.0, "transforms": [{"op": "negate_percentile"}]}
  ]}
}
```
Entries reference declared `components` by `id` (same shared histories as rules/vetoes); transform output scales must be comparable across regimes for argmax to be meaningful (percentile-family ops, all 0–1, are the safe choice).

`score_product` mode example (ER × VR/2.0 ≥ 0.4 → trending):
```json
"regime_detector": {
  "mode": "score_product",
  "min_score": 0.4,
  "min_margin": 0.0,
  "components": [
    {"id": "er", "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent", "params": {"period": 24, "smooth_period": 5}},
    {"id": "vr", "class": "strategies.strategy_components.VarianceRatioComponent", "params": {"k": 5, "window": 100}}
  ],
  "regimes": {
    "trending": {"components": [
      {"id": "er", "divisor": 1.0, "transforms": [{"op": "identity"}]},
      {"id": "vr", "divisor": 2.0, "transforms": [{"op": "identity"}]}
    ]}
  },
  "default_regime": "unknown"
}
```
With ER=0.5, VR=2.0 → product = 0.5 × 1.0 = 0.5 (≥ 0.4: fires). With ER=0.6, VR=0.8 → product = 0.6 × 0.4 = 0.24 (< 0.4: returns unknown).

### Veto entry
```json
{"id": "vol", "transforms": [{"op": "identity"}],
 "rules": [{"op": "gte", "value": 0.90}],
 "consecutive_bars": 2, "result": "chop"}
```
`id` must reference a declared component (validated at startup). `rules` are ANDed against the transformed value.

### Rule entry (threshold_rules)
```json
{"regime": "trending", "any_of": [
  [{"id": "er", "op": "gte", "value": 0.25}, {"id": "vr", "op": "gte", "value": 1.10}],
  [{"id": "er", "op": "gte", "value": 0.30}, {"id": "vr", "op": "between", "low": 0.90, "high": 1.10}]
]}
```
`any_of` = OR of condition-sets; each set = AND of conditions on RAW (untransformed) latest component values.
Comparison ops: `gte`, `gt`, `lte`, `lt`, `between` (`low`/`high`, inclusive).

**Comparator-vocabulary divergence (see §7d for the full callout):**
`regime_detector.rules`/`vetoes` use `gte`/`gt`/`lte`/`lt`/`between` — a
DIFFERENT vocabulary from `strategy-research/tools/verdict_criteria_evaluator.py`'s
`_VALID_COMPARATORS` (`>=`, `>`, `<=`, `<`, `==`), used for campaign
pass/fail criteria, not config rules. They are not interchangeable strings —
do not copy one vocabulary into the other's field.

## 2. `strategies`
| Key | Type | Default | Meaning |
|---|---|---|---|
| `warmup` | int | engine lookback | Min HISTORY DEQUE entries per active-regime component before forecasts are emitted. Unit is deque appends, NOT bars: appends start only once the component's own `is_ready()` fires, so first possible forecast ≈ max(required_bars, component required periods + warmup). Capped at smallest deque size. Legacy-parity value: 51 |
| `min_allocation_change` | float | none (falls back to `config.json`'s 0.2) | **Not a strategy-engine setting** — overrides `RiskManager`'s `min_allocation_change.threshold` control (`risk/risk_manager.py`) for THIS strategy's runs only. A rebalance is rejected whenever `abs(target_allocation − actual_allocation) < min_allocation_change`. This is the same gate `config.json`'s `risk_management.controls.min_allocation_change.threshold` has always set globally (default 0.2, live since before this key existed) — setting it here just makes that floor tunable per strategy instead of fixed for every strategy in one file. Omit to keep the global 0.2. See `known_divergences.md` §1 for the history. |
| `regimes` | dict | required | regime name → forecast config, or `null` = stay flat (forecast 0.0) |

### Per-regime forecast config
```json
"mean_reversion": {
  "components": [ <component spec>, ... ]   // ensemble: Σ (weight/Σweights) × pipeline(value); result clipped ±20
}
```

### Component spec (both engines)
| Key | Type | Default | Meaning |
|---|---|---|---|
| `id` | str | required | Unique key; referenced by rules/vetoes (regime engine) |
| `class` | dotted path | required | e.g. `strategies.strategy_components.RSIPullbackComponent`; validated at startup (and, since Slice 3a, at `validate_config.py` time too — see §7b) |
| `params` | dict | `{}` | Passed to component constructor (see catalog). WARNING: keys are NOT validated — a typo'd key is silently ignored and the default is used. Double-check spelling against the catalog |
| `weight` | float | required (strategy engine) | Ensemble weight, normalized by sum |
| `lookback` | int | engine lookback | History deque size. REQUIRED in practice when using `ratio_to_mean`-style normalization (sets the normalization window; legacy parity: 500). WARNING: an explicit override is NOT validated against the transforms' min periods — `"lookback": 10` with `percentile` (min 50) silently runs a 10-sample percentile (the warmup cap lowers warmup to 10, no error). Always set override ≥ the largest min-period of the component's ops |
| `history_transforms` | list of steps | `[]` | Applied once at append time; defines what the deque stores. Use for per-bar-state normalization (`vol_normalize`) |
| `transforms` | list of steps | required (strategy engine; vetoes; score mode) | Pipeline run at every forecast |

Transform step: `{"op": "<name>", "params": {...}}`.

## 3. Transform ops (`TRANSFORM_OPS_REGISTRY`)
Order rule: history-based ops recompute from history and DISCARD the accumulated value → place them first.

### History-based (ignore accumulated value)
| op | params | output |
|---|---|---|
| `identity` | — | latest raw value |
| `percentile` | — | rank of latest in history, 0–1 |
| `negate_percentile` | — | 1 − percentile |
| `zscore` | — | (latest − mean)/std; 0 if std≈0 |
| `ratio_to_mean` | — | latest / mean(\|history\|); NaN entries skipped; 0 if mean≈0 |
| `ema` | `span` (10) | EWM of history |

### Scalar (operate on accumulated value)
| op | params | output |
|---|---|---|
| `scale` | `factor` (1.0) | v × factor |
| `threshold_filter` | `min_abs` (0.0) | v if \|v\| ≥ min_abs else 0.0 |
| `clip` | `min`, `max` | clipped v |
| `sigmoid` | — | 1/(1+e^−v) |
| `negate` | — | −v |

### Data-aware (read current OHLCV window)
| op | params | output | notes |
|---|---|---|---|
| `vol_normalize` | — | v / (stddev_24 × close) | NO guard; NaN propagates by design. Intended for `history_transforms` |
| `vol_adjusted` | — | v / (stddev_24 × close), guarded (returns v if denom invalid) | read-time use only; do NOT use for history normalization |
| `price_normalized` | — | v / close, guarded | |
| `volume_filter` | `period` (20) | v if volume ≥ rolling mean else 0.0 | |

Every op MUST have a `TRANSFORM_MIN_PERIODS` entry (startup KeyError otherwise). Current minimums: percentile/negate_percentile 50, zscore/ratio_to_mean 30, ema 3×span, all others 1.

## 4. Component catalog (`strategies.strategy_components.*`)
All expose `raw_value()`; usable in both engines. `params` defaults in parentheses. "Req" = `get_required_periods()`.

**Component count is 24 today**, mechanically checked, not hand-counted —
`tests/test_design_guide_in_sync.py` (§8 below) fails the suite if this
catalog and `strategies/strategy_components.py` ever drift apart.

### Regime indicators (bounded outputs, good for rules)
| Class | params | Output scale | Req |
|---|---|---|---|
| `EfficiencyRatioRegimeComponent` | period(24), smooth_period(5) | 0–1 smoothed ER | period+1 |
| `VarianceRatioComponent` | k(5), window(100) | ~0.5–1.5; >1.10 trend, <0.90 mean-rev | window+k |
| `VolatilityPercentileRegimeComponent` | vol_period(20), lookback_period(100), smooth_period(5) | 0–1 vol rank | lookback+vol |
| `RSquaredRegimeComponent` | period(48) | 0–1 trend linearity | period |
| `ADXDirectionalComponent` | period(24) | −1..+1 DI-ratio | period+1 |

### Directional alpha (forecast-scale outputs)
| Class | params | Output | Req |
|---|---|---|---|
| `RSIPullbackComponent` | period(14), scaling_factor(0.4), long_only(false) | (50−RSI)×sf; long_only clamps ≥0. NOTE: `entry_threshold` param exists but is DEAD in config path — use `threshold_filter` transform | period+1 |
| `PriceEvolutionComponent` | period(20), scaling_factor(2.0) | pct-change × sf | period+1 |
| `PriceEvolutionOnPeriodComponent` | comparison_period(20), scaling_factor(20) | pct-change (sf unused in calc — verify before relying) | period+1 |
| `EMASpreadComponent` | fast_period(9), slow_period(21), scaling_factor(5.0) | EMA spread % × sf | slow |
| `EMADiff` | ST_EMA_period(12), LT_EMA_period(26) | absolute EMA gap (price units) | LT |
| `MacroTrendFilterComponent` | period(200), scaling_factor(2.0) | long-horizon trend | period |
| `DonchianBreakoutComponent` | period(48), scaling_factor(20.0) | breakout position | period |
| `KeltnerBreakoutComponent` | ema_period(20), atr_period(20), atr_multiplier(1.5), scaling_factor(20.0) | channel breakout | max(ema,atr)+1 |
| `MomentumDivergenceComponent` | short_period(5), long_period(20), scaling_factor(1.5) | short×long trend alignment | long |
| `MacdHistogramCrossoverComponent` | fast_period(12), slow_period(26), signal_period(9), scaling_factor(10.0) | ±sf event-pulse the bar the MACD histogram (MACD line − signal line) crosses zero (bullish/bearish); 0 all other bars — stateful, not a transform | slow+signal |
| `SmaTrendLongOnlyComponent` | lookback_L(100), scaling_factor(10.0) | sf if prior bar's close > SMA(lookback_L), else 0 — long-only (never negative), one-bar lag on both close and SMA (see class docstring: engine has no next-open fill, this is the closest approximation) | L+1 |
| `GatedSmaTrendLongOnlyComponent` | lookback_L(100), scaling_factor(10.0), er_period(20), gate_threshold(0.30) |sf if in position, else 0. SMA(L) long-only trend entry-latched by raw Kaufman ER(er_period) $\ge$ gate_threshold evaluated strictly at transition. One-bar lag on indicators | max(L+1, er_period+2) |
| `BuyAndHoldStrategy` | — | constant +10 | 0 |

### Hedges / filters
| Class | params | Output | Req |
|---|---|---|---|
| `PriceOverextensionHedgeComponent` | period(21), scaling_factor(2.0) | contrarian z-score vs EMA | period |
| `VolumeExpansionHedgeComponent` | vol_period(24), scaling_factor(20.0) | volume-expansion hedge | vol+1 |
| `VolatilityFromStdDevComponent` | vol_period(20), scaling_factor(1.0) | returns stdev % | vol_period |

### Structural / sentiment alpha (non-OHLCV — REQUIRE `aux_feeds`, see §4a)
| Class | params | Output | Req |
|---|---|---|---|
| `FundingRateMeanReversionComponent` | threshold(0.001), scaling_factor(10.0) | −sign(funding_rate)×sf at 8h settlement bars (UTC hour%8==0); 0 elsewhere. `threshold=0.0` fires at EVERY settlement bar regardless of magnitude (continuous variant) instead of only extremes | 2 |
| `FearGreedContrarianComponent` | fear_threshold(25.0), greed_threshold(75.0), scaling_factor(10.0) | +sf if prior day's F&G < fear_threshold, −sf if > greed_threshold, else 0; fires only at UTC-midnight boundary bars | 2 |
| `WhaleLargeTradeImbalanceComponent` | persistence_bars(3), min_abs_imbalance(0.5), scaling_factor(10.0) | mean(`whale_lt_imbalance`)×sf when the imbalance holds ONE sign with \|LTI\| ≥ min_abs_imbalance across `persistence_bars` consecutive fully-attested bars (continuation — sign NOT inverted); **NaN (abstain)** if any bar in that window is unattested, unmeasured, or the aux columns are absent; 0.0 only when the whole window was measured and was not sustainedly imbalanced | persistence_bars |

All three force `standardized_forecast: false` internally (constructor default override) —
do not add a `standardized_forecast: true` param expecting it to take effect.

**`WhaleLargeTradeImbalanceComponent` emits NaN, and that is deliberate** — read its
docstring before configuring it. NaN is ABSTENTION ("this bar measured nothing"), which
the framework supports (`STRATEGY_FRAMEWORK.md` invariant 1: NaN appends are legal;
never inject 0.0 placeholders). NaN propagates through `apply_transform_pipeline` to the
whole per-regime ensemble sum, so an abstained bar yields a NaN forecast for the regime,
not a partial one from the remaining components. Configure it **alone in its regime**
unless you intend that. Requires BOTH `whale_lt_imbalance` and `whale_attested` (see §4a).

#### §4a. `aux_feeds` (top-level config key)
Required whenever a component reads a column that isn't in the raw OHLCV bar DataFrame.
Recognized values today: `"funding_rate"` (merges a `funding_rate` column, backward
as-of join — `FundingRateMeanReversionComponent` requires this), `"fear_greed"`
(merges a `fear_greed` column, **with a +1 day shift already applied** for point-in-time
correctness per A8.4 — `FearGreedContrarianComponent` requires this).

**This `"aux_feeds"` config key is consumed by `prescreen_signal.py::_merge_aux_feeds()`
only** (the prescreen/signal-extraction path). It is DENY BY DEFAULT (dispatch W14 step
2): any name outside `{"funding_rate", "fear_greed"}` raises `UnrecognizedAuxFeedError`
naming the feed, rather than silently proceeding without the column — the prior
silent-drop behavior documented here before W14 was a real bug, not a documented
tolerance. The live/backtest `DataManager` path does not read this config key at all —
it is driven by explicit `register_feed()` calls (or, for a full backtest, by
`FEED_REGISTRY` membership passed as `extra_feeds` in `core/launcher.py`), and is
separately deny-by-default via the `window_seconds` causality declaration
(`data/ADDING_A_FEED.md` step 2).
```json
"aux_feeds": ["fear_greed"]
```
**Whale-footprint feeds are RESERVED and are not in `FEED_REGISTRY`.** The six names in
`data/feed_registry.py::WHALE_FOOTPRINT_FEEDS` live in `RESERVED_FEED_REGISTRY`; a caller
opts in by name and `campaign_data_policy.yaml` still has to carry a committed
designation or construction raises `ReservedDataError`. `WhaleLargeTradeImbalanceComponent`
needs two of them — `"whale_lt_imbalance"` and `"whale_attested"` — and abstains (NaN)
rather than firing if either column is missing. Note also that
`prescreen_signal.py::_merge_aux_feeds()` still knows only `funding_rate` and
`fear_greed` — it now REFUSES a whale feed name rather than silently dropping it, but it
still cannot DELIVER one; the `DataManager.register_feed()` path can.
A hypothesis needing funding rate or Fear & Greed is achievable via config ALONE
(existing components + `aux_feeds`) — this is NOT a component_gap. See run_041
(`H-041-A`, `strategy-research/runs/run_041/`) and run_042 (`H-041-C`,
`strategy-research/runs/run_042/artifacts/candidate_strategy_config.json`) for
working reference configs.

### Component variant patterns

**`KeltnerBreakoutComponent` — Variants via config (no new component needed):**
- Upper-band long breakout (momentum): `scaling_factor: +20.0` (default)
- Lower-band short/mean-reversion: `scaling_factor: -20.0` — inverts the signal;
  fires when price breaks BELOW the lower band. Use in trending regime with a negative
  forecast expectation, or in mean_reversion regime expecting bounce.
- Wider channels (fewer signals, higher conviction): increase `atr_multiplier` (e.g. 2.0)
- Tighter channels (more signals, lower conviction): decrease `atr_multiplier` (e.g. 1.0)

**`RSIPullbackComponent` — Variants via config (no new component needed):**
- Long-only mean-reversion: `long_only: true` (clamps forecast ≥ 0; only buys dips)
- Bidirectional: `long_only: false` (default) — fires on both overbought shorts and oversold longs
- Signal magnitude: adjust `scaling_factor` (higher = stronger raw signal before normalization)

**`EMASpreadComponent` — Variants via config (no new component needed):**
- Momentum (long when fast > slow): `scaling_factor: +5.0` (default)
- Inverse momentum (short when fast > slow): `scaling_factor: -5.0` — inverts signal direction
- Faster/slower crossover: adjust `fast_period` and `slow_period`

**`DonchianBreakoutComponent` — Variants via config (no new component needed):**
- Upper-band breakout (long momentum): `scaling_factor: +20.0` (default)
- Lower-band breakdown (short): `scaling_factor: -20.0` — inverts the signal
- Wider channel (fewer, higher-conviction breaks): increase `period` (e.g. 96)
- Tighter channel (more frequent signals): decrease `period` (e.g. 24)

## 5. Worked example (current production mean_reversion)
```json
{"id": "rsi", "class": "strategies.strategy_components.RSIPullbackComponent",
 "params": {"period": 14, "scaling_factor": 0.4, "long_only": true},
 "weight": 1.0, "lookback": 500,
 "history_transforms": [{"op": "vol_normalize"}],
 "transforms": [
   {"op": "ratio_to_mean"},
   {"op": "scale", "params": {"factor": 10.0}},
   {"op": "threshold_filter", "params": {"min_abs": 15.0}}
 ]}
```
Reads as: store vol-normalized pullback scores (500 deep) → current / mean(|history|) → ×10 (≈ "average signal = 10") → drop |forecast| < 15 → ensemble clip ±20. Threshold 15 on this scale ≈ "1.5× stronger than average signal".

## 6. Edit checklist
1. Component ids unique; veto/rule ids exist in `components` (startup error otherwise).
2. Pipeline order: history-based ops first, then scalar/data-aware.
3. Normalization vs per-bar market state (vol, price) → `history_transforms`, never read-time.
4. Set `"lookback"` explicitly on any component using `ratio_to_mean`/`percentile`/`zscore` — it IS the statistic's window.
5. After change, check startup log `StrategyEngine: lookback=X, warmup=Y` — warmup must equal config value, not a capped surprise.
6. Re-run backtest; diff `results/regime_debug.csv` and per-bar forecasts against the previous run before trusting performance numbers.
7. Pick the regime mode and gate pattern the hypothesis actually needs; default
   `threshold_rules`, one active regime is fine for a first test. If the
   hypothesis has no regime condition at all, use the ungated pattern in §7e
   rather than inventing a dummy always-true rule (see §7e for why the latter
   fails validation).
8. `default_regime` must be `"unknown"` in `threshold_rules` mode whenever
   `regime_detector.rules` is non-empty — a real gate exists there, and
   pointing `default_regime` at `trending`/`mean_reversion`/`chop` in that
   case bypasses it (every bar that fails every rule still gets classified
   as that regime and traded). `validate_config.py` VIOLATION V9 enforces
   this for all three names, not just `trending`. **CODE-REVIEW CORRECTION
   (2026-09-21):** in `score_product` mode, `default_regime` has NO
   behavioral effect at all — `_classify_score_product`
   (`regime_engine.py:205-224`) never reads it; a gate-fail there is
   hardcoded to `MarketRegime.UNKNOWN` regardless of the configured value.
   V9 currently applies the same restriction to `score_product` mode
   anyway (a pre-existing over-strictness in `validate_config.py`, not
   introduced by this slice and out of scope to change here) — so V9 may
   reject a `score_product` config for a bypass that cannot actually occur
   in that mode. Do not read V9 passing/failing as evidence about
   `score_product`'s real gate behavior. This restriction does NOT apply to
   the fully-ungated pattern (§7e) — there is no gate there to bypass.
9. Do not invent component classes, transform ops, or regime names absent from
   this guide's catalog (§4) — `validate_config.py` VIOLATION V12 (§7b) now
   catches an invented `class` value mechanically, but do not rely on the
   validator to find authoring mistakes a human/LLM author should have
   avoided in the first place.

## 7. Design-guide-only content (new for E-056 Slice 3a)

Everything above this line is the carried-over reference (§0 provenance
note). Everything below is new: §7a is a proposed, unbuilt schema addition;
§7b is NOT a proposal — it is built and live (validate_config.py
VIOLATION V12, shipped in this same slice); §7c is built and live (the
manifest contract, E-056 1b block-manifest ticket, 2026-09-24); §7d is a vocabulary callout;
§7e is authoring guidance folded from `backtest-engineering/SKILL.md`'s
Checklist/Forbidden sections (§6.7-9 above).

### CODE-REVIEW FIX (2026-09-21)

This section's numbering was reshuffled after an adversarial review caught
two real defects in the original draft: (1) this guide's own §6 item 8
claimed `default_regime` creates a gate-bypass risk in `score_product` mode
identical to `threshold_rules` mode — false. `_classify_score_product`
(`trading-bot/strategies/regime_engine.py:205-224`) never reads
`self._default_regime` at all; its gate-fail path is hardcoded to
`MarketRegime.UNKNOWN` regardless of the configured value, confirmed by
grep showing `_default_regime` is read only at `regime_engine.py:70` (the
assignment) and `:153` (inside `_classify_threshold_rules`, a different
method). `validate_config.py`'s pre-existing V9 check (unmodified by this
slice) DOES apply the same restriction to `score_product` mode regardless —
that is a separate, pre-existing over-strictness in production code this
slice did not introduce and is out of scope to fix here; flagged as a
follow-up, not silently corrected mid-docs-change. (2) three cross-references
in the original draft pointed readers to "§7b" for V12 documentation while
§7b's actual heading was the unrelated manifest-contract proposal — a real
section that documented V12 never existed. Fixed by inserting §7b below as
V12's own section and renumbering everything after it.

### §7a. Instrument-set / symbol / timeframe field — PROPOSED, NOT BUILT

**This does not exist in the config schema today.** The top-level shape in
"Top-level shape" above (`regime_detector`, `strategies`, `aux_feeds`) has no
symbol, timeframe, or instrument-set key anywhere. There is currently no way
to declare, inside `strategy_config.json` itself, which symbol(s) or
timeframe a config targets — that information lives elsewhere today (backtest
harness arguments, run-level metadata), not in the strategy config object.

E-056 S1 flagged this as the single largest real gap in the existing
reference documentation, and this guide's own characterization session
(`S2_FINDINGS.md` §6) independently confirmed it, finding no counter-evidence.

**Open question, deliberately not resolved here:** whether this field would
live as a new top-level sibling of `regime_detector`/`strategies`/`aux_feeds`,
or somewhere else. (Not in the §7c block manifest: since that contract was
built, 2026-09-24, it forbids any coin/instrument field — a validated block
is usable on any coin.) This depends on composition work (Slice 7) that is
not built yet. Do not invent a resolution
to this question when authoring configs — it is unresolved by design, not by
omission.

**Not enforced by `validate_config.py`.** No V-check reads or requires this
field, because it does not exist yet.

### §7b. Component-class existence check (`validate_config.py` VIOLATION V12) — BUILT, LIVE

Unlike §7a, this is not a proposal — it shipped in this same slice
(E-056 Slice 3a). Every `class` value in `regime_detector.components[]` and
`strategies.regimes.*.components[]` is now checked, at `validate_config.py`
time, against `strategies.strategy_components` via
`strategies.registry._load_class` (the exact function the live engine calls
at startup — V12 reuses it rather than re-implementing dotted-path
resolution, so V12 fails on exactly the set of configs the engine would
already refuse to start on, no more, no less).

**Before this check:** an invented or typo'd `class` value passed
`validate_config.py` silently and only failed much later, at engine startup
— after a full backtest had already been launched and its data fetched.
**After this check:** the same mistake is caught at validation time, before
any backtest runs.

Verified against the full real corpus (every `candidate_strategy_config.json`
under `strategy-research/runs/run_*/`): zero currently-passing real configs
newly fail under V12 — this check only adds a new failure mode for configs
that were already broken and would have failed at startup regardless. Shipped
unconditionally, no flag, on exactly that empirical basis.

### §7c. The manifest contract (`block_manifest.yaml`) — BUILT, LIVE (config-direct-authoring flow)

Built 2026-09-24 (E-056 1b block-manifest ticket; was "PROPOSED, NOT
BUILT"). Stage 1b (`strategy_config_authoring`, only under
`orchestrator.config_direct_authoring.enabled`) writes
`artifacts/block_manifest.yaml` next to `backtest_spec.yaml` whenever its
status is `spec_ready`. It says which part of the base config IS the
hypothesis's block, as opposed to scaffolding — so the block registry can
store the block alone, without a second LLM pass re-deriving the boundary.

```yaml
block:
  kind: forecast                 # forecast | regime -- the only two block kinds
  config_paths:                  # non-empty; JSON pointers into the base config
    - /strategies/regimes/unknown/components/0
scaffolding:                     # may be []; config the idea needs but that is not the idea
  - /strategies/warmup
  - /regime_detector
rationale: the RSI pullback component is the hypothesis; the ungated detector and warmup only run it
```

Rules (every one enforced by code):

1. Exactly the keys `block` (with exactly `kind`, `config_paths`),
   `scaffolding` and `rationale` — no others. `rationale` is a non-empty
   string.
2. `kind` is `forecast` or `regime`. A `forecast` block has at least one
   `config_paths` entry under `/strategies/regimes/`; a `regime` block has at
   least one at or under `/regime_detector`.
3. Every pointer (block and scaffolding) is an RFC 6901 JSON pointer into the
   strategy config itself (`/strategies/...`, not `/config/strategies/...`)
   and resolves in the base config. Pointers are distinct.
4. No pointer lies inside another's subtree — neither two block paths, nor a
   block path and a scaffolding path. A config piece is block or scaffolding,
   never both.
5. No coin, symbol, timeframe or instrument field (a validated block is usable
   on any coin), and no `hypothesis_id` (the run already carries the idea's
   identity).

**Who checks it.** One implementation, `strategy-research/tools/block_manifest.py`,
used by both readers:

- the tool-only `backtest_specification` stage (5a) checks it against 1b's
  base config before building any variant; a missing, unparseable, malformed
  or unresolved manifest stops the run (`RuntimeError`). A variant whose patch
  removes a block path is marked `not_tested` (`manifest paths unresolved`);
- `tools/block_registry.py` checks it again against the tested base config
  when a validated run registers its block (`config_fragment` = the values at
  `block.config_paths`).

`workflow_artifacts/schemas/block_manifest.schema.json` documents the same
shape (rules 1-3's shape part); `tests/test_e056_1b_block_manifest.py` keeps
schema and code in agreement. A pass-through candidate's `manifest` field
(hypothesis-design IMPROVEMENT 08) is written through verbatim and checked the
same way.

### §7d. Comparator-vocabulary divergence

`regime_detector.rules`/`vetoes` (§1/§2 above) use the comparator vocabulary
`gte`/`gt`/`lte`/`lt`/`between`. A separate, unrelated vocabulary exists in
`strategy-research/tools/verdict_criteria_evaluator.py`'s `_VALID_COMPARATORS`
tuple: `>=`, `>`, `<=`, `<`, `==` — used for campaign-level pass/fail
criteria evaluation (`pass_rule`/criterion checks against
`config/criterion_menu.yaml`), a completely different config surface from
`strategy_config.json`'s own regime rules.

**These two vocabularies are not interchangeable.** A rule written with `">="`
in `regime_detector.rules` is not a recognized op there (only `gte` is); a
criterion written with `"gte"` in a `pass_rule`/criterion spec is not in
`_VALID_COMPARATORS` (only `">="` is). Confirmed independently by this
session and by E-056/E-046b S1 (`S2_FINDINGS.md` §6 item 3,
`S1_FINDINGS.md` line 243, `verdict_criteria_evaluator.py:52`). Check which
config surface you are authoring for before picking a comparator string.

### §7e. Ungated hypotheses — the canonical no-regime pattern

Folded from `backtest-engineering/SKILL.md`'s "Ungated hypotheses" section
(current authoring guidance, unchanged by this guide — see that skill file
for the full, current-authority version if this guide and the skill ever
diverge). Most hypotheses in the current campaign have no regime condition at
all (the signal should be active every bar). Building this with a dummy
always-true rule and an invented regime name is what caused run_043's first
blocker (2026-07-04) — `VIOLATION V7` rejected the invented name, but the
correct pattern avoids needing one:

```json
"regime_detector": {
  "mode": "threshold_rules",
  "components": [],
  "rules": [],
  "default_regime": "unknown"
},
"strategies": {
  "warmup": 51,
  "regimes": {
    "unknown": { "components": [ /* the real signal */ ] },
    "trending": null, "mean_reversion": null, "chop": null
  }
}
```

`default_regime` MUST be `"unknown"` in this pattern specifically (not any of
the four interchangeably) — `main_strategy.is_ready()` reads
`current_regime` before `classify()` runs for the current bar, so on the
first ready-candidate bar `current_regime` is still `MarketRegime.UNKNOWN`
regardless of the configured target; only `default_regime="unknown"` avoids
a one-bar early, under-warmed forecast. See
`backtest-engineering/SKILL.md` "Ungated hypotheses" and
`trading-bot/tests/test_ungated_config_pattern.py` for the full empirical
verification this pattern is built on. `validate_config.py` VIOLATION V10
enforces the concrete authoring mistake this pattern invites (a fully-ungated
detector pointing `default_regime` at a null `strategies.regimes` entry).

## 8. Design-guide-catalog sync test

`strategy-research/tests/test_design_guide_in_sync.py` mechanically compares
this file's §4 component catalog against
`grep -c "^class.*SubStrategyComponent" trading-bot/strategies/strategy_components.py`
and the actual class names found — not a hardcoded count — so this guide
cannot silently drift out of step the way `STRATEGY_CONFIG_REFERENCE.md`
itself could (nothing enforced that file's catalog stayed in sync before this
test existed).
