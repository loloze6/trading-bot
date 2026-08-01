# Improvement 09 — Cost Hurdle as an Upstream Design Constraint

## Gap

Cost drag is the campaign's empirically dominant kill cause, yet it is handled purely **reactively**: the `cost_drag` diagnostic rule fires after a full backtest and prescribes "raise threshold_filter". Nothing prevents a hypothesis whose implied turnover makes it dead-on-arrival at Binance spot fee levels from consuming a validation gate, a backtest spec, and a full walk-forward before that arithmetic is done. The arithmetic requires no backtest: expected gross edge per trade vs round-trip cost is computable from the hypothesis's timeframe, signal class, and turnover — approximately at validation time, precisely at prescreen time (Improvement 08).

## Two-layer gate

### Layer 1 — Coarse, at `validation_gate` (LLM, declarative)

New required block in `validation_protocol.yaml`:

```yaml
cost_feasibility:
  assumed_round_trip_cost_bps: float      # from config: Binance spot taker fee ×2 + spread estimate for the symbol; maintained in one place, config/cost_model.yaml
  expected_holding_bars: [min, max]       # from hypothesis: signal class + timeframe
  expected_trades_per_window: int          # implied by holding period and gating
  required_gross_edge_bps_per_trade: float # = 2 × assumed_round_trip_cost_bps (safety factor 2)
  plausibility: enum[plausible, marginal, implausible]
  plausibility_rationale: string           # must reference the signal class and timeframe, e.g. "1h mean-reversion with ~6-bar holds must clear ~X bps/trade gross; typical gross edges for this class are Y–Z bps"
```

Hard rule in the `quant-validation` skill: `plausibility: implausible` → validation status cannot be `approve`; must be `refine` with the blocking issue "turnover/cost mismatch" (typical fixes: longer timeframe, tighter gating, wider holding period), or `reject`. This mirrors the existing "no falsifiable statement → no approval" hard rule.

### Layer 2 — Precise, at `signal_prescreen` (deterministic, Improvement 08)

`prescreen_result.yaml` already computes `turnover_proxy` (implied rebalance count under the 0.20 allocation threshold). Add:

```yaml
cost_check:
  implied_trades_per_window: float
  estimated_gross_edge_bps_per_trade: float   # from IC and return volatility: rough expectancy per rebalance, documented formula in tool
  cost_bps_per_trade: float                    # from config/cost_model.yaml
  edge_to_cost_ratio: float
  pass: boolean                                # ratio >= 2.0
```

Routing: `pass = false` with significant positive IC → refine at the signal-smoothing/filter level **before** the backtest (this is the generative version of the current post-hoc `cost_drag` rule). `pass = false` with marginal IC → treat as prescreen kill.

### Single source of truth for costs

New `config/cost_model.yaml` (per symbol: fee tier, spread estimate, optional slippage bps). Consumed by: validation gate (Layer 1), prescreen (Layer 2), the backtest engine, and the `cost_drag` diagnostic rule — currently these can silently disagree. One file, four consumers.

## Interaction with existing `cost_drag` rule

The rule stays (execution can always surprise), but after 08+09 land, a `cost_drag` firing means the *upstream estimate was wrong*, which is itself diagnostic: the verdict must record the estimate-vs-realized gap in `supporting_evidence`, and repeated large gaps trigger recalibration of `config/cost_model.yaml` — turning the pipeline's #1 killer into a self-calibrating model instead of a recurring surprise.

## Acceptance criteria

1. No hypothesis with `cost_feasibility.plausibility = implausible` reaches `backtest_specification` (schema + routing check).
2. `config/cost_model.yaml` exists and is the only place fee/spread numbers appear (grep audit: no hardcoded fee constants in tools or skills).
3. Regression: ≥2 historical runs killed by `cost_drag` are re-evaluated through Layer 1/Layer 2 logic and would have been blocked or refined pre-backtest.
4. When `cost_drag` fires post-backtest despite gates, `verdict_interpretation.supporting_evidence` contains the estimated-vs-realized cost gap.
