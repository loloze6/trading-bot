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

## 1. `risk_management.rebalance_threshold` is dead

*Recorded 2026-07-28, dispatch W11 step 6(b). Flagged by dispatch W10.*

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
