# strategy_config.json — Field Reference

Edit this file only. No Python changes needed. Run `python trading-bot/main.py simulate` to test.

---

## Annotated config

```json
{
  "regime_detector": {
    // "threshold_rules" = priority if/else with absolute thresholds (current, deterministic)
    // "score"           = weighted scoring + argmax (adaptive, see end of file)
    "mode": "threshold_rules",

    // Components compute one raw value per bar from OHLCV data.
    // "id"     = your local name, referenced in rules/vetoes
    // "class"  = full Python import path to the component class
    // "params" = constructor args for that component
    // lookback is auto-computed from each component's get_required_periods() — no manual field.
    "components": [
      {
        "id":     "er",
        "class":  "strategies.strategy_components.EfficiencyRatioRegimeComponent",
        "params": {"period": 24, "smooth_period": 5}
      },
      {
        "id":     "vr",
        "class":  "strategies.strategy_components.VarianceRatioComponent",
        "params": {"k": 5, "window": 100}
      },
      {
        "id":     "vol",
        "class":  "strategies.strategy_components.VolatilityPercentileRegimeComponent",
        "params": {"vol_period": 20, "lookback_period": 100, "smooth_period": 5}
      }
    ],

    // Vetoes override rules when a sustained extreme is detected. Checked FIRST, every bar.
    // "id"               = component id to monitor (must be declared in components above)
    // "transforms"       = pipeline applied to the component's history; output is a single float
    // "rules"            = AND conditions evaluated against the pipeline output (no "id" needed,
    //                      context is already the veto's own component). Same op/value grammar as
    //                      threshold rules. All conditions must hold simultaneously to increment counter.
    // "consecutive_bars" = bars the conditions must hold continuously before the veto fires
    // "result"           = regime string assigned when veto fires (overrides all rules)
    "vetoes": [
      {
        "id":               "vol",
        "transforms":       [{"op": "identity"}],
        "rules":            [{"op": "gte", "value": 0.90}],
        "consecutive_bars": 2,
        "result":           "chop"
      }
    ],

    // Rules evaluated top-to-bottom. First match wins. Fires if ANY condition set (any_of) fully matches.
    // Each condition set is an AND list. Operators: "gte" ">=" | "lte" "<=" | "gt" ">" | "lt" "<" | "between"
    // "between" requires "low" and "high" keys instead of "value".
    "rules": [
      {
        "regime": "trending",
        "any_of": [
          [{"id": "er", "op": "gte", "value": 0.25}, {"id": "vr", "op": "gte", "value": 1.10}],
          [{"id": "er", "op": "gte", "value": 0.30}, {"id": "vr", "op": "between", "low": 0.90, "high": 1.10}]
        ]
      },
      {"regime": "mean_reversion", "any_of": [
        [{"id": "er", "op": "lte", "value": 0.20}, {"id": "vr", "op": "lte", "value": 0.90}]
      ]},
      {"regime": "chop", "any_of": [
        [{"id": "er", "op": "lte", "value": 0.15}, {"id": "vol", "op": "lte", "value": 0.35}]
      ]}
    ],

    // Regime returned when no rule matches. Acts as the "else" fallback.
    "default_regime": "mean_reversion"
  },

  "strategies": {
    // lookback is auto-computed from component get_required_periods() — no manual field.
    "regimes": {
      // null = no position in this regime (forecast = 0)
      "trending": null,

      "mean_reversion": {
        "components": [
          {
            // Local name for this signal within the ensemble
            "id": "rsi",
            // Full Python import path to the component class
            "class": "strategies.strategy_components.RSIPullbackComponent",
            // Constructor args passed to the component
            "params": {"period": 14, "scaling_factor": 0.4, "long_only": true, "entry_threshold": 0.0},
            // Relative contribution weight. Normalized across all components in this regime.
            "weight": 1.0,
            // Ordered pipeline of transform ops applied to the component's rolling history.
            // History-based ops (identity, percentile, zscore, ema...) normalize relative to history.
            // Scalar ops (scale, threshold_filter, clip, negate) operate on the running value.
            "transforms": [
              // Step 1: reduce history to latest raw value (no normalization)
              {"op": "identity"},
              // Step 2: gate — if |value| < min_abs, this component contributes 0 this bar
              {"op": "threshold_filter", "params": {"min_abs": 15.0}},
              // Step 3: multiply by factor to map into the [-20, +20] forecast range
              {"op": "scale", "params": {"factor": 1.0}}
            ]
          }
        ]
      },

      "chop":    null,
      "unknown": null  // fired during warmup or when score mode finds no clear winner
    }
  }
}
```

---

## Common edits

**Loosen/tighten a regime threshold** → edit `"value"` in a rule condition.

**Add a new regime** → add a rule block + add the regime key under `strategies.regimes` (null or strategy block).

**Replace the strategy for a regime** → replace the `null` or the whole block under `strategies.regimes.<name>`.

**Add a second component to an ensemble** → add another object to `strategies.regimes.<name>.components`. Weights are auto-normalized.

**Disable a veto** → set `"consecutive_bars": 9999`.

**Use a component from a different module** → set `"class"` to its full dotted import path. Any importable class with the right interface works.

**Normalize a signal** → replace `{"op": "identity"}` with `{"op": "percentile"}` (rank in [0,1] over history), then set scale to 20.

**Remove the threshold gate** → delete the `threshold_filter` step, or set `"min_abs": 0.0`.

**Switch to adaptive scoring** → change `mode` to `"score"`, remove `rules`/`default_regime`, add `regimes` block. See STRATEGY_OPTIONS.md for score mode schema.

---

## Transform pipeline

Each component produces one raw value per bar. The `transforms` list is an ordered pipeline applied to that component's rolling history before it enters the weighted ensemble.

**Pipeline execution:**
1. Seed: `value = history[-1]` (latest raw value)
2. For each step: `value = op(value, full_history, params)`
3. Result is the component's weighted contribution to the ensemble forecast

**Op types:**
- History-based (`identity`, `percentile`, `zscore`, etc.) — recompute from the full history, ignoring the incoming `value`. These normalize the signal relative to its past.
- Scalar (`scale`, `threshold_filter`, `clip`, `negate`, `sigmoid`) — transform the running `value` from the previous step.

Order matters: `percentile → scale → threshold_filter` produces different results than `identity → threshold_filter → scale`.

---

## Constraints

- Every veto `id` and every condition `id` in `rules` must match a declared `components[].id`.
- Veto `rules` conditions have no `id` field — they evaluate against the veto's own component output.
- Veto `result` must be a valid regime name.
- Every `class` must be a valid dotted import path to a class that subclasses `SubStrategyComponent`.
- Every `op` in `transforms` (including veto `transforms`) must be a valid key in `TRANSFORM_OPS_REGISTRY`.
- History-based ops (`identity`, `percentile`, `zscore`, etc.) must appear BEFORE scalar ops (`scale`, `threshold_filter`, etc.) in any `transforms` list — history-based ops discard the accumulated value.
- Valid regime names: `"trending"`, `"mean_reversion"`, `"chop"`, `"unknown"`.
- Forecast is hard-clipped to [-20, +20]. Final signal after `scale` should not exceed ±20.
- `lookback` is derived automatically from component requirements. Do not add it to config.
