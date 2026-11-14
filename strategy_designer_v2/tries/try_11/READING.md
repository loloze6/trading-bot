# try 11: reading of `summarise.py` on try 09 (one window, W1, claim range_break_strength)

`python3 steps/analyst/summarise.py tries/try_09/engine` writes `tries/try_09/engine/book_summary.yaml` (89 lines for two sizings, about 45 per window; no dates). `engine_fold_A` had only configs and trades files, no `engine_verdict.yaml` or results, so it was not run.

Key numbers, full_size W1:
- net return -95.24%, Sharpe -12.16 (core) / -11.51 (bar_equity), drawdown -95.2%; fees 490 against gross pnl -462; cost drag 106%.
- 2514 trades, win rate 32.3%, average net -0.38, largest win 29.4, largest loss -47.4, average hold 1.71 bars; long net -507, short net -445.
- exposure 99.9%, turnover 3452, mean absolute allocation change 1.21 per bar.
- forecast: quantiles 1/10/25/50/75/90/99 = -20 / -15.5 / -6.8 / 0.2 / 7.1 / 14.3 / 20; 11.7% of bars at the cap, 8.0% near zero (<1), 50.7% positive.
- sign agreement with the next bar's return: 46.8% on all bars, 48.3% on event bars; correlation -0.018.
- 29 event bars, 12-bar forward return: strength positive n=10, mean +1.04%, 50% up; strength negative n=19, mean -0.24%, 32% up.
- equity deciles 713, 422, 355, 262, 170, 137, 98, 76, 54, 48 (start 998.5): steady bleed, no single collapse. Worst bar -47.3 (index 501), best +30.3.
vol_target W1: -63.4%, same 2514 trades, fees 391, gross -243.

Columns used (from `bars.csv`): equity `postRebalance_total_value`; position `postRebalance_current_allocation`; allocation `previous_allocation` and `allocation_change`; `forecast`; `debug_info.components.<claim id>.event` and `.strength`. Trades: `net_profit_loss_absolute`, `net_profit_loss_percent`, `side`, `duration_minutes` (the plain `profit_loss_*` fields are gross of fees).

What the files lacked or got around:
- The claim's horizon is not in the engine folder; the script reads `horizon_bars` from `claims.yaml` beside `engine/` (12 if absent).
- `exposure` and `turnover` come from `bar_equity`; exposure is also recomputed from the position column (99.9, agrees).
- The forecast cap (20) and "near zero" (<1) are constants in the script.
- Bar spacing is taken from the timestamps' median step to convert trade minutes to bars; no date is written.
- `run_dir` is relative to the repo root; the script finds that root by walking up to the folder that holds `strategy_designer_v2`.
