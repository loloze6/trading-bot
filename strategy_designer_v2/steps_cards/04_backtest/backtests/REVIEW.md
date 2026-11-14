# Review of the backtests in this folder

**What ran.** Every plan in `../../03_test_plan/plans/` (29 plans, one per idea, daily bars, fold A; the hourly set is in `../exercise_hourly_anticipation/`), through `../helper/run_backtest.py`, which runs the bot's backtest unchanged.

These records follow the rewrite of the plans with symmetric criteria. Step 4 reran only the plans whose config or data changed. It ignores component labels and params written at their catalogue default, since those don't change what the engine computes. Log: `run_log_symmetric.txt`. Earlier logs: `run_log.txt` (first run), `run_log_fidelity.txt` (after the fidelity rule). Size: 5 MB.

## What the refresh did

| | plans |
|---|---|
| Record kept: config and data unchanged | 8 |
| Rerun and run: 001-02, 002-02, 003-03, 003-04, 003-05 | 5 |
| Rerun and refused by the engine: 003-01, 003-02 | 2 |
| Not run: untestable or missing-components (003-06's old record removed) | 14 |

## The current state

| | plans |
|---|---|
| Plans (daily) | 29 |
| Run | 13 |
| Not run: untestable (two coins) | 7 |
| Not run: missing-components | 7 |
| Not run: refused by the engine | 2 |

- **Coins.** Ideas from brief 001 (RSI) run on BTC and ETH; BNB has no data on the reachable venue (Kraken). Every other idea runs on the default, BTC.
- **Windows.** Every run plan ran 6 of 6 windows per coin.

## The plans the engine refused

`003-01_low-volume-up-move-reverts` (it ran before this rewrite) and `003-02_low-volume-down-move-reverts`. Both have a regime detector that is a veto on a constant (`BuyAndHoldStrategy` through `volume_filter`), with the default regime flat. The engine stops at its warm-up check: "warmup_prefetch: strategy not ready after 48 prefetch bars". This is the parked pattern (`../../POTENTIAL_ADJUSTMENTS.md`); its investigation is with another agent. Their old records are removed, so step 5 gives them no verdict, not a verdict on an old config.

## What the engine reports, per plan (not a verdict)

The engine's own `forecast_return_corr_all_bars` per window, from `metrics.json`. It is not the plans' criteria: applying those is step 5's job. It shows only that the records are complete and not empty.

| plan | coin | windows | trades (sum) | forecast vs next return, all bars, per window |
|---|---|---|---|---|
| 001-01_rsi-high-extreme-reversal_1d | BTCUSD | 6 | 149 | +0.001, -0.001, +0.110, +0.014, -0.049, -0.000 |
| 001-01_rsi-high-extreme-reversal_1d | ETHUSD | 6 | 153 | -0.037, +0.014, +0.014, +0.072, +0.180, +0.029 |
| 001-02_rsi-low-extreme-rebound_1d | BTCUSD | 6 | 156 | -0.007, -0.039, +0.091, -0.033, +0.109, +0.000 |
| 001-02_rsi-low-extreme-rebound_1d | ETHUSD | 6 | 181 | -0.009, -0.094, +0.077, +0.029, +0.100, -0.029 |
| 001-03_rsi-high-extreme-continuation_1d | BTCUSD | 6 | 142 | -0.001, +0.001, -0.110, -0.014, +0.049, +0.000 |
| 001-03_rsi-high-extreme-continuation_1d | ETHUSD | 6 | 147 | +0.037, -0.014, -0.014, -0.072, -0.180, -0.029 |
| 001-04_rsi-low-extreme-continuation_1d | BTCUSD | 6 | 182 | +0.007, +0.039, -0.091, +0.033, -0.109, -0.000 |
| 001-04_rsi-low-extreme-continuation_1d | ETHUSD | 6 | 226 | +0.009, +0.094, -0.077, -0.029, -0.100, +0.029 |
| 002-01_sma-upcross-upward-drift_1d | BTCUSD | 6 | 30 | -0.109, n/a, n/a, -0.080, -0.008, -0.044 |
| 002-02_sma-downcross-downward-drift_1d | BTCUSD | 6 | 62 | -0.127, -0.150, -0.034, -0.151, n/a, -0.072 |
| 002-03_price-upcross-long-sma-drift_1d | BTCUSD | 6 | 47 | n/a, n/a, n/a, -0.189, -0.022, -0.032 |
| 002-04_price-downcross-long-sma-drift_1d | BTCUSD | 6 | 118 | -0.248, -0.098, -0.149, -0.067, -0.087, +0.005 |
| 002-05_sma-up-regime-positive-drift_1d | BTCUSD | 6 | 30 | -0.109, n/a, n/a, -0.080, -0.008, -0.044 |
| 002-06_sma-down-regime-negative-drift_1d | BTCUSD | 6 | 62 | -0.127, -0.150, -0.034, -0.151, n/a, -0.072 |
| 003-03_high-volume-up-move-continues_1d | BTCUSD | 6 | 138 | -0.080, -0.039, -0.047, +0.127, -0.024, -0.020 |
| 003-04_high-volume-down-move-continues_1d | BTCUSD | 6 | 128 | -0.016, +0.062, -0.006, -0.043, -0.020, -0.140 |
| 003-05_up-move-retrace-by-volume_1d | BTCUSD | 6 | 241 | -0.111, +0.001, -0.080, +0.065, +0.042, +0.006 |
