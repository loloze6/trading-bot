# Known divergences: configuration vs. engine behaviour

Settings that exist in configuration or documentation but are **not in force** in
the running engine. Each entry states what the config says, what the code
actually does, and what depends on the difference.

A divergence is recorded here rather than repaired on sight. Changing engine
behaviour to match a stale doc is a silent strategy change; changing it requires
its own dispatch, its own re-costing, and — because every archived backtest was
produced under the *actual* behaviour — an explicit decision about what happens
to those results. Documenting is reversible. Rewiring is not.

---

## 1. `risk_management.rebalance_threshold` is dead (RESOLVED 2026-09-10, E-055)

*Recorded 2026-07-28, dispatch W11 step 6(b). Flagged by dispatch W10.*

**Update 2026-09-10 (E-055):** this entry's headline claim -- "no drift
threshold anywhere" -- was itself wrong, and has been corrected, not just the
docs it flagged as wrong. A change-based drift gate has been live the whole
time: `RiskManager._ctrl_min_allocation_change` (`risk/risk_manager.py`)
rejects any rebalance where `abs(allocation_change)` is below
`risk_management.controls.min_allocation_change.threshold` (`config.json`,
0.2). Git archaeology (`git log -p -S"min_allocation_change"`) shows it was
introduced in the SAME commit and diff hunk as the `rebalance_threshold`
key/constructor arg described below being commented out -- strong evidence
this control is that mechanism's direct successor, not an unrelated one. The
dead key and the commented-out constructor call (both quoted below as
historical record) have now been deleted from `config.json` and
`core/launcher.py`.

**What this means for the two dependents listed below:** neither was ever
running under "no threshold." `prereg_whale_footprint_v2.yaml`'s
`avg_holding_bars` reasoning and every archived backtest's turnover/cost
figures were produced under the 0.2 floor from the start -- nothing about
their validity or comparability changes. The maker-execution assessment's
citation of a nonexistent `ForecastManager.needs_rebalance()` is still wrong
for that specific claim (no such method exists, and never has), independent
of this correction.

**What actually changed (E-055):** `strategy_config.json` can now set
`strategies.min_allocation_change` to override the 0.2 default **for that
strategy's runs only** (`strategies/main_strategy.py` reads it;
`core/launcher.py::_build_risk_and_forecast_managers` threads it into
`RiskManager`'s controls). Omitting the key is byte-identical to before this
existed. Only a strategy that explicitly sets a value below 0.2 will see any
different turnover than the same strategy did previously -- and even then,
only down to that new value, since RiskManager's own comparison
(`abs(change) < threshold`) is what enforces it either way.

**Original record follows, kept for history:**

**Config says:** `trading-bot/config.json:16` sets
`risk_management.rebalance_threshold = 0.20`.

**Docs said:** the architecture overview described
`ForecastManager.needs_rebalance()` returning `bool + Δ`, with "Rebalance
triggers when `|new_target - actual_market_allocation| >= rebalance_threshold`
(default 5%)". Three claims, all wrong: the method does not exist, no threshold
comparison happens anywhere, and the configured value is 0.20, not 0.05.

**The engine actually does:** rebalances toward target on **every bar** whenever
the allocation change is nonzero at all. The only gate is

```python
# trading-bot/core/trading_bot.py:229
if abs(allocation_change) != 0.0:
    approved_rebalance, ... = self.risk_manager.approve_allocation_change(...)
```

`ForecastManager` (`trading-bot/execution/forecast_manager.py`) has no
`needs_rebalance` method and no threshold state — its `__init__` takes no
arguments and still carries a stale `# 5% threshold` comment. The only reference
to the config key anywhere in the tree is **commented out**:

```python
# trading-bot/core/launcher.py:108-111
# risk_manager = RiskManager(
#     max_position_size=...,
#     rebalance_threshold=self.config.get('risk_management').get('rebalance_threshold', 0.2)
# )
```

Drift gating is therefore not merely mis-parameterised; it was never wired up.
`RiskManager.approve_allocation_change` still runs and can veto a change, but on
its own controls, not on a drift threshold.

**Status: DOCUMENTED, NOT REPAIRED.** Engine behaviour is unchanged by W11.

**What depends on this**

- **Turnover and cost.** Rebalancing every bar is the maximum-turnover regime.
  Every archived backtest and every `cost_model.yaml` figure derived from one was
  produced under it, so the numbers are internally consistent — but they describe
  an engine with no drift band, and any future comparison against a threshold-
  gated engine is not like-for-like.
- **`prereg_whale_footprint_v2.yaml`.** Its `avg_holding_bars` reasoning cites
  this fact directly, and depends on it holding: because no threshold damps
  turnover, a measured holding period of ~5.74 bars is *signal persistence*
  rather than an artifact of a rebalance band. Wiring the threshold up would
  invalidate that argument and the required-IC derivation resting on it.
- **Maker-execution planning.** `engineering/improvements/done/design_and_docs/10_maker_execution_assessment.md`
  reasons about `ForecastManager.needs_rebalance()` as an existing gate. It is
  not one; that analysis needs re-reading with this in mind.

**If someone decides to wire it up**, the change is a strategy change, not a bug
fix: it needs a dispatch, a re-cost, and a decision on the archived results.
Deleting the dead config key instead is the other clean option. Leaving it
half-present, as now, is the state this entry exists to keep visible.
