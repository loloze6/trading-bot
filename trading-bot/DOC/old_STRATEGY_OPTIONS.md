# Strategy Options Reference

---

## Available Components

Each component computes one raw numeric value per bar from OHLCV data.
Reference by full import path in `"class"`. Output range determines which transform ops to pair.

### Regime / Structure

| Class (last segment) | Full `"class"` path | Output | What it measures | Key params |
|---|---|---|---|---|
| `EfficiencyRatioRegimeComponent` | `strategies.strategy_components.EfficiencyRatioRegimeComponent` | [0, 1] | Trend efficiency: 1 = straight line, 0 = pure noise | `period` (24), `smooth_period` (5) |
| `VarianceRatioComponent` | `strategies.strategy_components.VarianceRatioComponent` | ~[0.5, 1.8] | Autocorrelation: >1 = trending, <1 = mean-reverting, 1 = random walk | `k` (5), `window` (100) |
| `VolatilityPercentileRegimeComponent` | `strategies.strategy_components.VolatilityPercentileRegimeComponent` | [0, 1] | Smoothed % rank of current vol vs history: 0 = quiet, 1 = explosive | `vol_period` (20), `lookback_period` (100), `smooth_period` (5) |
| `RSquaredRegimeComponent` | `strategies.strategy_components.RSquaredRegimeComponent` | [0, 1] | Pearson R² of price vs time: 1 = perfect linear trend | `period` (48) |
| `ADXDirectionalComponent` | `strategies.strategy_components.ADXDirectionalComponent` | [-1, 1] | ADX DI-ratio: +1 = strong uptrend, -1 = strong downtrend, 0 = no direction | `period` (24) |

### Directional / Alpha

| Class (last segment) | Full `"class"` path | Output | What it measures | Key params |
|---|---|---|---|---|
| `KeltnerBreakoutComponent` | `strategies.strategy_components.KeltnerBreakoutComponent` | [-24, +24] | Penetration depth of ATR Keltner bands. Near 0 inside, ±1.2 when broken. | `ema_period` (20), `atr_period` (20), `atr_multiplier` (1.5), `scaling_factor` (20) |
| `RSIPullbackComponent` | `strategies.strategy_components.RSIPullbackComponent` | [-20, +20] | `(50 − RSI) × scaling_factor`. Positive = oversold (buy). `long_only: true` clips negatives to 0. | `period` (14), `scaling_factor` (0.4), `long_only` (false) |
| `EMASpreadComponent` | `strategies.strategy_components.EMASpreadComponent` | unbounded % | % gap between fast and slow EMA × scaling_factor. Positive = uptrend. | `fast_period` (9), `slow_period` (21), `scaling_factor` (5.0) |
| `DonchianBreakoutComponent` | `strategies.strategy_components.DonchianBreakoutComponent` | [-20, +20] | Where price sits in N-bar High-Low range, shifted to [-1,+1] × scaling_factor. | `period` (48), `scaling_factor` (20) |
| `PriceEvolutionComponent` | `strategies.strategy_components.PriceEvolutionComponent` | unbounded % | Net % price change over `period` bars × scaling_factor. Raw momentum. | `period` (20), `scaling_factor` (2.0) |
| `MomentumDivergenceComponent` | `strategies.strategy_components.MomentumDivergenceComponent` | unbounded | `short_trend% × long_trend%`. Positive = both aligned (trend acceleration). | `short_period` (5), `long_period` (20) |

### Hedge / Filter

| Class (last segment) | Full `"class"` path | Output | What it measures | Key params |
|---|---|---|---|---|
| `PriceOverextensionHedgeComponent` | `strategies.strategy_components.PriceOverextensionHedgeComponent` | unbounded | `−(z-score of price vs EMA) × scaling_factor`. Negative when price overextended above EMA. | `period` (21), `scaling_factor` (2.0) |
| `VolumeExpansionHedgeComponent` | `strategies.strategy_components.VolumeExpansionHedgeComponent` | [−20, 0] | Negative when price rises on below-average volume (bull trap). 0 otherwise. | `vol_period` (24), `scaling_factor` (20) |
| `MacroTrendFilterComponent` | `strategies.strategy_components.MacroTrendFilterComponent` | unbounded % | % distance of price from long EMA × scaling_factor. Positive = above macro trend. | `period` (200), `scaling_factor` (2.0) |
| `VolatilityFromStdDevComponent` | `strategies.strategy_components.VolatilityFromStdDevComponent` | [0, ~5%] | Rolling std of returns. Use as a risk scaler or vol regime filter. | `vol_period` (20) |
| `BuyAndHoldStrategy` | `strategies.strategy_components.BuyAndHoldStrategy` | 10 (constant) | Always outputs +10. Benchmark or always-long baseline. | — |

---

## TRANSFORM_OPS_REGISTRY

Applied as an ordered pipeline of steps in `"transforms"`. Each step receives the accumulated value
from the previous step plus the full component history.

**Signature:** `(v: float, history: pd.Series, params: dict) → float`

### History-based ops — normalize the signal against its own rolling history

| `"op"` | Formula | Output | When to use |
|--------|---------|--------|-------------|
| `identity` | `history[-1]` | same as component | First step when raw scale is already correct. |
| `percentile` | `rank(history) / N` | [0, 1] | Signal strength relative to history. 0.5 = median. |
| `negate_percentile` | `1 − percentile` | [0, 1] | When LOW values are bullish (e.g., low ER → good for mean-reversion). |
| `zscore` | `(raw − mean) / std` | ~[−3, +3] | Mean-normalize. Sensitive to distribution shifts. |
| `ratio_to_mean` | `raw / mean(abs(history))` | ~[0, 3] | Multiplicative normalize. Better for always-positive signals. |
| `ema` | `ewm(span=p["span"])[-1]` | same as component | Smooth over history before further ops. Default span=10. |

### Scalar ops — transform the running pipeline value

| `"op"` | Formula | Output | When to use |
|--------|---------|--------|-------------|
| `scale` | `v × p["factor"]` | scaled | Map normalized signal to [-20,+20] forecast range. |
| `threshold_filter` | `v if \|v\| ≥ p["min_abs"] else 0` | 0 or v | Gate: suppress weak signals. |
| `clip` | `clip(v, p["min"], p["max"])` | bounded | Cap extremes without zero-centering. |
| `sigmoid` | `1 / (1 + e^-v)` | (0, 1) | Soft-clip. Reduces outlier impact without a hard boundary. |
| `negate` | `-v` | flipped sign | Invert directional bias. |

**Pairing guide:**
- Component output already in target range (Keltner ±20, RSI ±20) → `identity` → `threshold_filter` → `scale: 1.0`
- Component in [0,1] (ER, vol_percentile) → `identity` (for threshold rules); or `percentile` → `scale: 20` for strategy
- Unbounded momentum → `zscore` → `scale: 7`; or `ratio_to_mean` → `scale: 10`
- Need smoothing before gating → `ema` (first) → `threshold_filter` → `scale`

---

## Score mode schema (alternative to threshold_rules)

Replace `"rules"` and `"default_regime"` with this structure under `regime_detector`.
Score mode `regimes` components use `id` (references a declared detector component) + `weight` + `transforms`.
No `class` field — score mode doesn't instantiate new objects, it rescores existing ones.

```json
"mode": "score",
"min_score": 0.35,   // Minimum winning score (0–1). Lower = more bars classified.
"min_margin": 0.05,  // Gap between #1 and #2 score required to commit.
"regimes": {
  "trending": {
    "components": [
      {"id": "er", "weight": 0.45, "transforms": [{"op": "percentile"}]},
      {"id": "vr", "weight": 0.55, "transforms": [{"op": "percentile"}]}
    ]
  },
  "mean_reversion": {
    "components": [
      {"id": "er", "weight": 0.45, "transforms": [{"op": "negate_percentile"}]},
      {"id": "vr", "weight": 0.55, "transforms": [{"op": "negate_percentile"}]}
    ]
  },
  "chop": {
    "components": [
      {"id": "er",  "weight": 0.5, "transforms": [{"op": "negate_percentile"}]},
      {"id": "vol", "weight": 0.5, "transforms": [{"op": "negate_percentile"}]}
    ]
  }
}
```

Each regime's score = weighted average of component pipeline outputs (should be in [0,1]).
Winner must beat `min_score` AND lead runner-up by `min_margin`, else → `unknown`.

To add smoothing: prepend `{"op": "ema", "params": {"span": 3}}` to a component's `transforms`.
This smooths the component history before scoring, equivalent to the old `smoothing_span` field.

**Regime flicker in score mode:** without smoothing, score mode reacts immediately to each bar.
On noisy data this can produce rapid regime switches (flicker). If this appears during testing,
add `{"op": "ema", "params": {"span": 3}}` as the first step in each scoring component's
`transforms` list — this is the correct fix, not re-adding a `smoothing_span` config field.

---

## Signal pipeline

```
component.raw_value()              raw number each bar
→ rolling history (auto-sized to component's required periods)
→ transforms[0]                    first op (usually a history-based normalizer)
→ transforms[1]                    e.g. threshold_filter
→ transforms[2]                    e.g. scale
→ × (weight / Σweights)            weighted contribution
→ Σ ensemble                       combine components
→ clip(−20, +20)                   hard ceiling
→ ForecastManager                  converts forecast to position size
```

Forecast → allocation: +20 = 100% long, +10 = ~50% long, 0 = flat, −10 = ~50% short, −20 = 100% short.
