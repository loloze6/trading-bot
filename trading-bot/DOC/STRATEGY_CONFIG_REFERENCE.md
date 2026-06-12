# STRATEGY_CONFIG_REFERENCE.md
Purpose: edit `strategy_config.json` without reading code. Every key, every option.
Schema and behavior owned by `regime_engine.py`, `strategy_engine.py`, `registry.py`.

## Top-level shape
```json
{
  "regime_detector": { ... },   // → ConfigDrivenRegimeEngine
  "strategies":      { ... }    // → ConfigDrivenStrategyEngine
}
```

## 1. `regime_detector`
| Key | Type | Default | Meaning |
|---|---|---|---|
| `mode` | `"threshold_rules"` \| `"score"` | `threshold_rules` | Classification algorithm |
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

## 2. `strategies`
| Key | Type | Default | Meaning |
|---|---|---|---|
| `warmup` | int | engine lookback | Min HISTORY DEQUE entries per active-regime component before forecasts are emitted. Unit is deque appends, NOT bars: appends start only once the component's own `is_ready()` fires, so first possible forecast ≈ max(required_bars, component required periods + warmup). Capped at smallest deque size. Legacy-parity value: 51 |
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
| `class` | dotted path | required | e.g. `strategies.strategy_components.RSIPullbackComponent`; validated at startup |
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
| `BuyAndHoldStrategy` | — | constant +10 | 0 |

### Hedges / filters
| Class | params | Output | Req |
|---|---|---|---|
| `PriceOverextensionHedgeComponent` | period(21), scaling_factor(2.0) | contrarian z-score vs EMA | period |
| `VolumeExpansionHedgeComponent` | vol_period(24), scaling_factor(20.0) | volume-expansion hedge | vol+1 |
| `VolatilityFromStdDevComponent` | vol_period(20), scaling_factor(1.0) | returns stdev % | vol_period |

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
