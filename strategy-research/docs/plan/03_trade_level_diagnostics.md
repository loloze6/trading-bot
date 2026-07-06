# Improvement 03 — Trade-Level Diagnostics (Entry/Exit Attribution)

## Gap

`protocol_result.yaml` currently reports Sharpe, drawdown, trade count, win rate, and three scalar diagnostics (`forecast_return_corr`, `cost_drag_pct`, `win_rate_vs_sharpe`). None of these can distinguish *where inside a trade* value is being won or lost. A strategy that correctly identifies direction but exits too early looks identical, in current outputs, to a strategy whose signal is simply wrong — both show mediocre Sharpe and unremarkable win rate. Every `refine`/`pivot` verdict issued today is therefore guessing which side of the trade (entry, holding, or exit) to fix, if any.

This improvement adds trade-level (not just aggregate) diagnostics to the deterministic backtest tool, and a new sub-field of the verdict that attributes performance to entry quality, exit quality, or the underlying signal.

## New artifact: `trade_diagnostics.json`

Produced alongside `protocol_result.yaml` by `tools/run_protocol.py`. One record per closed trade, plus an aggregated summary.

### Per-trade record

```json
{
  "trade_id": "string",
  "symbol": "string",
  "window": "string",
  "regime_at_entry": "string",
  "direction": "long | short",
  "entry_time": "iso8601",
  "exit_time": "iso8601",
  "holding_bars": "int",
  "realized_return": "float",
  "mae": "float",              // max adverse excursion during the trade, as % move against position
  "mfe": "float",              // max favorable excursion during the trade
  "entry_efficiency": "float", // realized_return vs. return if entered at next-bar open instead of signal bar
  "exit_efficiency": "float",  // realized_return vs. best possible exit within the holding window (given the actual entry)
  "exit_reason": "signal_flip | stop_loss | time_stop | end_of_window"
}
```

### Aggregated summary (feeds `protocol_result.yaml` as a new `trade_diagnostics_summary` block)

```yaml
trade_diagnostics_summary:
  mae_mfe_ratio_median: float          # low ratio + poor realized return => exits leaving money on table
  entry_efficiency_median: float        # near 0 = entry timing adds nothing beyond direction call; negative = entry timing actively hurts
  exit_efficiency_median: float         # same interpretation for exits
  holding_period_distribution:
    p10_bars: int
    p50_bars: int
    p90_bars: int
  pnl_concentration:
    pct_pnl_from_top_decile_trades: float   # tail-dependency: fragile if very high
  exit_reason_breakdown:
    signal_flip_pct: float
    stop_loss_pct: float
    time_stop_pct: float
    end_of_window_pct: float
```

## Implementation notes for `tools/run_protocol.py`

- MAE/MFE requires intra-holding-period price path, not just entry/exit prices — ensure the backtest loop retains bar-by-bar prices during the holding window rather than discarding them after computing realized return.
- `entry_efficiency` and `exit_efficiency` require counterfactual computation (next-bar-open entry; best-possible-exit-in-window) — implement as pure post-hoc calculations against the same price series, no re-simulation of the strategy needed.
- Keep this fully deterministic — no LLM involvement. This is a metrics-engineering change to an existing Python tool, not a new skill.

## Verdict-interpreter changes

Add a new field to `verdict_interpretation.yaml`:

```yaml
trade_attribution:
  primary_weakness: enum[entry, exit, holding_sizing, signal_direction, none_healthy]
  evidence: string   # must reference specific trade_diagnostics_summary fields
```

Decision logic to embed in the skill:

| Pattern in `trade_diagnostics_summary` | `primary_weakness` |
|---|---|
| High `mfe`, low realized return, low `exit_efficiency_median` | `exit` — signal finds good moves, exits give them back |
| Negative `entry_efficiency_median` | `entry` — entering late/early relative to signal degrades the edge |
| High `mae` before profitable close, many `stop_loss` exits on trades that would have recovered | `holding_sizing` — stops too tight relative to the signal's natural noise |
| Poor `entry_efficiency`, `exit_efficiency`, and negative `forecast_return_corr` together | `signal_direction` — genuine signal problem, not execution |
| None of the above triggered | `none_healthy` |

This directly feeds Improvement 01's `mechanism_failure = entry_exit_execution_gap`: when `primary_weakness` is `entry`, `exit`, or `holding_sizing`, the verdict must **not** discard the underlying signal — it routes to a parameter-level refine on execution logic (altitude 1), which is a fundamentally different and cheaper fix than pivoting the hypothesis family.

## Schema/orchestrator changes

- `schemas/trade_diagnostics.schema.json` — new.
- `schemas/protocol_result.schema.json` — add `trade_diagnostics_summary` block.
- `schemas/verdict_interpretation.schema.json` — add `trade_attribution` block.
- No new pipeline stage required — this is an enrichment of the existing `protocol_execution` tool output and the existing `verdict_interpreter` stage's inputs.

## Acceptance criteria

1. `trade_diagnostics.json` is produced for every `protocol_execution` run with at least one closed trade, with per-trade MAE/MFE/entry/exit efficiency populated.
2. `verdict_interpretation.yaml` includes `trade_attribution.primary_weakness` for every verdict, with evidence citing a specific summary field.
3. At least one regression case can be constructed (e.g., a synthetic strategy with a known "good entry, bad exit" pattern) where `primary_weakness = exit` is correctly identified.
4. When `primary_weakness != signal_direction` and `!= none_healthy`, the routed action is a parameter-level refine targeting execution logic, not a family pivot — verifiable in orchestrator routing logs.
