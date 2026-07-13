# STRATEGY_EXTENDING.md
Purpose: add a new component, transform op, or regime. Each recipe is self-contained; total code change per recipe is one class or one lambda + registry entries + config.

Moving a hypothesis to a NEW TIMEFRAME (not just a new component)? See
`docs/TIMEFRAME_CHANGE_PLAYBOOK.md` first — warmup mechanics, the two
different assumption-sweep categories (bar-count vs. signal-shape), shakedown
doctrine, and the cross-check pattern that catches a signal-shape bug hiding
behind a bar-count fix.

## A. New indicator component
Where: `strategies/strategy_components.py`. No registration needed — config references the dotted class path.

```python
class MyComponent(SubStrategyComponent):
    def __init__(self, name, weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 20)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            self._raw_value = float(<one scalar from the window>)   # REQUIRED: engines read raw_value()
            self.confidence = 1.0
            self.debug_info = {}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period

    def get_required_periods(self) -> int:
        return self.period          # must be >= the data your math actually needs
```
Rules:
- `update()` is called EVERY bar with the full rolling window (recompute from window; do not assume incremental state). Internal smoothing state (lists) is allowed — see `EfficiencyRatioRegimeComponent`.
- Set `_raw_value` only when ready; one consistent scale. Keep raw; scaling/normalization belongs in transforms.
- `get_required_periods()` undersized → silent NaN/IndexError downstream. Off-by-one: pct-change over N bars needs N+1.
- Then reference in config: `{"id": "x", "class": "strategies.strategy_components.MyComponent", "params": {...}, ...}`. Class path validated at startup via `_load_class`.

## B. New transform op
Where: `strategies/registry.py`. THREE mandatory touch points:

1. `TRANSFORM_OPS_REGISTRY` — signature `(v, h, p, d) -> float`:
   - `v` accumulated pipeline value, `h` full history `pd.Series`, `p` step params dict, `d` current OHLCV window (may be None).
   - Decide the kind and respect it: history-based (recompute from `h`, ignore `v` — document it goes first in pipelines) | scalar (use `v` only) | data-aware (use `v` + `d`).
2. `TRANSFORM_MIN_PERIODS` — REQUIRED; startup raises KeyError without it. Set the real statistical minimum (rank/mean/std-type ops: 30–50; scalar ops: 1). Param-dependent minimums (like ema's 3×span) go in `transform_min_periods()` instead.
3. If intended for `history_transforms` (append-time): it runs on a 1-element series; only `v` and `d["..."].iloc[-1]` are meaningful. Do NOT add NaN/zero-guard fallbacks that substitute a value — propagate NaN so `ratio_to_mean`'s pandas mean skips the bar (see FRAMEWORK invariant 1; a 0.0 fallback here caused a real bug).

```python
"my_op": lambda v, h, p, d: v * p.get("k", 1.0),        # scalar example
# TRANSFORM_MIN_PERIODS["my_op"] = 1
```

## C. New regime
1. `strategies/strategy_base.py`: add to `MarketRegime` enum.
2. `strategies/regime_engine.py`: add to `_REGIME_MAP`.
3. Config: add classification path (a `rules` entry / score-mode `regimes` entry / veto `result`) AND a `strategies.regimes` entry (`null` = flat is valid).
4. Check downstream consumers of `regime.value` (CSV outputs, risk controls) tolerate the new value.

## D. What does NOT need code
- New ensembles, weights, thresholds, normalization windows, regime rules, vetoes → config only.
- Turning a regime on/off → set its `strategies.regimes` entry to a config object / `null`.
- Reusing one component class with different params under different ids → config only.

## E. Mandatory validation after ANY extension
1. Startup must be clean: class-path, veto-id, and min-periods checks all fail fast — read the first 20 log lines.
2. Check `StrategyEngine: lookback=X, warmup=Y` against expectation.
3. If the change is meant to be iso-functional: diff per-bar forecasts + regimes vs previous run log (`grep -o "Forecast: [+-][0-9.]*"` / `grep -o "Regime: [a-zA-Z_]*"`, then `diff`). Expect 0 diffs.
4. If the change is meant to alter behavior: confirm diffs appear ONLY where intended (e.g. only in the targeted regime's bars).
