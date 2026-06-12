# STRATEGY_FRAMEWORK.md
Purpose: minimal mental model of the config-driven strategy framework. Read this first.
For config edits → STRATEGY_CONFIG_REFERENCE.md. For new components/transforms → STRATEGY_EXTENDING.md.

## File map
| File | Role |
|---|---|
| `strategy_config.json` | Single source of truth: regime detection rules + per-regime forecast pipelines |
| `strategies/main_strategy.py` | `AdvancedStrategy`: owns data buffer, wires regime engine + strategy engine, emits `(forecast, _, regime, confidence, debug)` |
| `strategies/regime_engine.py` | `ConfigDrivenRegimeEngine`: classifies bar into a `MarketRegime` |
| `strategies/strategy_engine.py` | `ConfigDrivenStrategyEngine`: produces forecast in [-20, +20] for the active regime |
| `strategies/registry.py` | `_load_class` (dotted-path import), `TRANSFORM_OPS_REGISTRY`, `apply_transform_pipeline`, `TRANSFORM_MIN_PERIODS`, lookback derivation |
| `strategies/strategy_components.py` | Indicator components (stateless re: pipeline; emit one scalar/bar via `raw_value()`) |
| `strategies/strategy_base.py` | `StrategyNode`/`SubStrategyComponent` ABCs, `MarketRegime` enum, `RollingBuffer`, `MainStrategy` |

## Per-bar data flow
```
new bar
 └─ AdvancedStrategy.update()
     ├─ RollingBuffer.add_data(bar)          # buffer size = required_bars + 100
     │    └─ get_df() recomputes calculated columns (e.g. stddev_24) over the WINDOW
     ├─ regime_engine.update(window)         # each component.update(df) → if ready: history[cid].append(raw_value())
     └─ strategy_engine.update(window)       # same, but per (regime, component); history_transforms applied AT APPEND
 └─ AdvancedStrategy.generate_forecast()
     ├─ regime_engine.classify() → MarketRegime    (vetoes first, then rules/score)
     └─ strategy_engine.forecast(regime)
          for each component in regimes[regime].components:
              value = apply_transform_pipeline(history_deque, transforms, window)
          ensemble = Σ (weight/Σweights) × value
          return clip(ensemble, -20, +20)          # null regime config → 0.0
```
Forecast → `forecast_to_allocation` (= forecast/10.0) downstream.

## Key contracts
- **Component contract** (`SubStrategyComponent`): `update(df)` sets `self._raw_value` (one float per bar), `is_ready()`, `get_required_periods()`. Engines never call `generate_forecast()` — legacy path only. `_raw_value` must be on a consistent scale per component (see catalog).
- **History deques**: one per (regime, component-id) in the strategy engine; one per component-id in the regime engine (shared across rules/vetoes). Appended every bar once `is_ready()`. NaN appends are legal and intentional (see invariants).
- **Transform pipeline** (`apply_transform_pipeline(history, transforms, data)`): seeds `value = history[-1]`, then applies ops in order. Two op kinds:
  - history-based (`identity`, `percentile`, `zscore`, `ratio_to_mean`, `ema`, ...): RECOMPUTE from full history, DISCARD accumulated value → must come before scalar ops.
  - scalar/data-aware (`scale`, `threshold_filter`, `clip`, `negate`, `sigmoid`, `vol_adjusted`, ...): operate on accumulated value.
- **history_transforms vs transforms**: `history_transforms` run ONCE at append time and define what the deque stores (e.g. `vol_normalize` → deque holds vol-adjusted values). `transforms` run at every forecast over the stored history. Normalizations whose denominator depends on per-bar market state MUST be history_transforms — at read time the OHLCV buffer is shorter than the deque and the historical denominators no longer exist.

## Readiness gating (three layers, all must pass)
1. `data_buffer.size >= required_bars` — required_bars = max(regime engine, strategy engine, stddev period 24).
2. `regime_engine.is_ready()` — threshold_rules mode: every history ≥ 1; score mode: every history full (= lookback).
3. `strategy_engine.is_ready(current_regime)` — every history of the ACTIVE regime ≥ `warmup`. Note: regime checked is the previous bar's (classify runs after); harmless, transitions are rare.

## Lookback / warmup derivation (startup)
- Engine `lookback` = max over components of `component_effective_lookback(spec, comp.get_required_periods())` = max(component periods, min-periods of every op in `transforms` + `history_transforms`).
- Per-component deque size = spec `"lookback"` override, else engine lookback.
- `warmup` = min(config `warmup`, smallest deque maxlen). Startup log line: `StrategyEngine: lookback=X, warmup=Y` — verify after any config change.
- `transform_min_periods(op)` raises `KeyError` for ops missing from `TRANSFORM_MIN_PERIODS` → fails at startup, not silently.

## Invariants & footguns (do not "fix" these)
1. **`vol_normalize` has NO zero/NaN guard on purpose.** During warmup `stddev_24` is NaN → NaN is appended → pandas `mean()` in `ratio_to_mean` skips it. Adding a 0.0 fallback poisons the normalization mean (historic bug). Same class of bug: never inject 0.0 placeholders into history deques.
2. **`stddev_24` (and any RollingBuffer calculated column) is recomputed over the current window** → first N-1 rows of every window are always NaN. Never read historical rows of a calculated column for normalization; normalize at append time instead.
3. **Pipeline order matters**: a history-based op after a scalar op silently discards the scalar's output (`[scale, percentile]` throws away scale).
4. **threshold_filter runs before the ensemble ±20 clip** — harmless while min_abs < 20; revisit if min_abs ≥ 20.
5. **A strategy component spec without `"lookback"` override** gets the engine-default deque; the warmup cap then silently lowers effective warmup to that size. Check the startup log line.
6. `regimes: {"<name>": null}` = deliberately flat in that regime (forecast 0.0). Not an error.
7. **`regime_scores`/`regime_margin` in `debug_info` are score-mode-only fields.** Under `threshold_rules` they are structurally `{}` and `None` — correct and expected, not missing data. Only populated when `regime_detector.mode = "score"`.

## Verified baseline
Backtest BTCUSDT 1h 2024-04-01→2024-05-30: bit-identical (4-dp) per-bar regimes and forecasts vs legacy `WeightedComponentRegimeDetector`/`CompositeStrategy` implementation (1438 bars, 0 diffs).
