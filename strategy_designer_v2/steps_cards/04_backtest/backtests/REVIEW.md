# Review of the backtests in this folder

**What ran.** Every plan in `../../03_test_plan/plans/` (58 plans: daily and hourly, fold A), through `../helper/run_backtest.py`, which runs the bot's backtest unchanged.

These records follow the rewrite of the plans with the fidelity rule. Step 4 reran only the plans whose config or data changed. It ignores component labels and params written at their catalogue default, since those don't change what the engine computes. Log: `run_log_fidelity.txt`. The first run's log is `run_log.txt`. Size: 37 MB.

## What the refresh did

| | plans |
|---|---|
| Record kept: config and data unchanged | 14 |
| Rerun, or run for the first time | 15 |
| Not run: untestable or missing-components (their old records removed) | 29 |

## The current state

| | daily | hourly | total |
|---|---|---|---|
| Plans | 29 | 29 | 58 |
| Run | 15 | 12 | 27 |
| Not run: untestable (two coins) | 7 | 7 | 14 |
| Not run: missing-components | 6 | 9 | 15 |
| Not run: refused by the engine | 1 | 1 | 2 |

- **Coins.** Ideas from brief 001 (RSI) run on BTC and ETH; BNB has no data on the reachable venue (Kraken). Every other idea runs on the default, BTC.
- **Windows.** Every run plan ran 6 of 6 windows per coin.

## The plans the engine refused

`003-02_low-volume-down-move-reverts` (daily and hourly). Its regime detector is a veto on a constant (`BuyAndHoldStrategy`), with the default regime flat: the same pattern that stopped five plans in the first run. The engine stops at its warm-up check: "warmup_prefetch: strategy not ready after 48 prefetch bars". The cause is under investigation (another agent). The fix belongs in step 3.

## What the engine reports, per plan (not a verdict)

The engine's own `forecast_return_corr_all_bars` per window, from `metrics.json`. It is not the plans' criteria: applying those is step 5's job. It shows only that the records are complete and not empty.

| plan | coin | windows | trades (sum) | forecast vs next return, all bars, per window |
|---|---|---|---|---|
| 001-01_rsi-high-extreme-reversal_1d | BTCUSD | 6 | 149 | +0.001, -0.001, +0.110, +0.014, -0.049, -0.000 |
| 001-01_rsi-high-extreme-reversal_1d | ETHUSD | 6 | 153 | -0.037, +0.014, +0.014, +0.072, +0.180, +0.029 |
| 001-01_rsi-high-extreme-reversal_1h | BTCUSD | 6 | 3829 | -0.002, +0.003, +0.016, -0.026, +0.001, -0.006 |
| 001-01_rsi-high-extreme-reversal_1h | ETHUSD | 6 | 3871 | -0.018, -0.013, +0.000, -0.004, +0.000, -0.003 |
| 001-02_rsi-low-extreme-rebound_1d | BTCUSD | 6 | 156 | -0.007, -0.039, +0.091, -0.033, +0.109, +0.000 |
| 001-02_rsi-low-extreme-rebound_1d | ETHUSD | 6 | 181 | -0.009, -0.094, +0.077, +0.029, +0.100, -0.029 |
| 001-02_rsi-low-extreme-rebound_1h | BTCUSD | 6 | 3268 | -0.010, +0.002, -0.003, -0.006, -0.021, +0.004 |
| 001-02_rsi-low-extreme-rebound_1h | ETHUSD | 6 | 3248 | -0.017, -0.024, -0.004, -0.015, +0.007, -0.002 |
| 001-03_rsi-high-extreme-continuation_1d | BTCUSD | 6 | 142 | -0.001, +0.001, -0.110, -0.014, +0.049, +0.000 |
| 001-03_rsi-high-extreme-continuation_1d | ETHUSD | 6 | 147 | +0.037, -0.014, -0.014, -0.072, -0.180, -0.029 |
| 001-03_rsi-high-extreme-continuation_1h | BTCUSD | 6 | 3787 | +0.002, -0.003, -0.016, +0.026, -0.001, +0.006 |
| 001-03_rsi-high-extreme-continuation_1h | ETHUSD | 6 | 3831 | +0.018, +0.013, -0.000, +0.004, -0.000, +0.003 |
| 001-04_rsi-low-extreme-continuation_1d | BTCUSD | 6 | 182 | +0.007, +0.039, -0.091, +0.033, -0.109, -0.000 |
| 001-04_rsi-low-extreme-continuation_1d | ETHUSD | 6 | 226 | +0.009, +0.094, -0.077, -0.029, -0.100, +0.029 |
| 001-04_rsi-low-extreme-continuation_1h | BTCUSD | 6 | 3320 | +0.010, -0.002, +0.003, +0.006, +0.021, -0.004 |
| 001-04_rsi-low-extreme-continuation_1h | ETHUSD | 6 | 3346 | +0.017, +0.024, +0.004, +0.015, -0.007, +0.002 |
| 002-01_sma-upcross-upward-drift_1d | BTCUSD | 6 | 30 | -0.109, n/a, n/a, -0.080, -0.008, -0.044 |
| 002-01_sma-upcross-upward-drift_1h | BTCUSD | 6 | 650 | +0.002, +0.005, -0.025, +0.020, -0.010, +0.012 |
| 002-02_sma-downcross-downward-drift_1d | BTCUSD | 6 | 37 | +0.109, n/a, n/a, +0.080, +0.008, +0.044 |
| 002-02_sma-downcross-downward-drift_1h | BTCUSD | 6 | 763 | +0.011, +0.022, -0.016, +0.014, -0.004, -0.006 |
| 002-03_price-upcross-long-sma-drift_1d | BTCUSD | 6 | 47 | n/a, n/a, n/a, -0.189, -0.022, -0.032 |
| 002-03_price-upcross-long-sma-drift_1h | BTCUSD | 6 | 1327 | +0.014, -0.000, +0.001, +0.025, +0.001, +0.010 |
| 002-04_price-downcross-long-sma-drift_1d | BTCUSD | 6 | 118 | -0.248, -0.098, -0.149, -0.067, -0.087, +0.005 |
| 002-04_price-downcross-long-sma-drift_1h | BTCUSD | 6 | 1755 | +0.013, +0.019, -0.016, +0.025, -0.011, -0.021 |
| 002-05_sma-up-regime-positive-drift_1d | BTCUSD | 6 | 30 | -0.109, n/a, n/a, -0.080, -0.008, -0.044 |
| 002-05_sma-up-regime-positive-drift_1h | BTCUSD | 6 | 650 | +0.002, +0.005, -0.025, +0.020, -0.010, +0.012 |
| 002-06_sma-down-regime-negative-drift_1d | BTCUSD | 6 | 62 | -0.127, -0.150, -0.034, -0.151, n/a, -0.072 |
| 002-06_sma-down-regime-negative-drift_1h | BTCUSD | 6 | 763 | +0.011, +0.022, -0.016, +0.014, -0.004, -0.006 |
| 003-01_low-volume-up-move-reverts_1d | BTCUSD | 6 | 143 | -0.132, +0.038, -0.041, -0.009, +0.119, +0.024 |
| 003-03_high-volume-up-move-continues_1d | BTCUSD | 6 | 120 | -0.071, -0.035, -0.063, +0.119, -0.013, -0.018 |
| 003-03_high-volume-up-move-continues_1h | BTCUSD | 6 | 2643 | +0.003, +0.015, -0.026, +0.024, +0.015, -0.018 |
| 003-04_high-volume-down-move-continues_1d | BTCUSD | 6 | 128 | -0.016, +0.062, -0.006, -0.043, -0.020, -0.140 |
| 003-05_up-move-retrace-by-volume_1d | BTCUSD | 6 | 296 | -0.166, -0.045, -0.020, +0.137, +0.008, +0.040 |
| 003-05_up-move-retrace-by-volume_1h | BTCUSD | 6 | 6185 | -0.001, -0.007, -0.020, +0.021, +0.028, -0.017 |
| 003-06_down-move-retrace-by-volume_1d | BTCUSD | 6 | 381 | -0.020, +0.130, -0.014, -0.102, -0.022, -0.107 |

