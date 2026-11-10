# Review of the backtests in this folder

The production run: every plan in `../../03_test_plan/plans/`, daily and hourly bars, fold A, through `../helper/run_backtest.py` (the bot's backtest, unchanged). Log: `../production_run_log.txt`. About 1 hour 20 minutes, no model call. Size: 38 MB, with bars and trades gzipped.

## Counts

| | daily | hourly | total |
|---|---|---|---|
| Plans | 29 | 29 | 58 |
| Run | 14 | 13 | 27 |
| Not run: untestable plan (another coin, or a divergence) | 13 | 13 | 26 |
| Not run: refused by the engine | 2 | 3 | 5 |

- **Coins.** Ideas from briefs 001 (RSI) name BTC, ETH and BNB: BTC and ETH ran; BNB has no data on the reachable venue (Kraken). Every other idea runs on the default, BTC.
- **Windows.** Every run plan ran 6 of 6 windows per coin: 210 windows in all.
- **The forced plans.** The four divergence plans that were forced in step 3's first run were not run. After step 3's rerun they are untestable, and their index lines now say so.

## The five plans the engine refused

`003-01_1d`, `003-05_1d`, `003-01_1h`, `003-02_1h`, `003-06_1h`. All five have the same regime detector:
- one component, `BuyAndHoldStrategy`, with a veto that applies `volume_filter` to it;
- no rules;
- the default regime flat (`unknown`, null).

The engine stops at its own warm-up check, in `trading-bot/core/launcher.py`: "warmup_prefetch: strategy not ready after 48 prefetch bars ... 2x-required_bars was insufficient for this config". The validator accepts this config; the engine's warm-up does not. The other volume plans (veto on `PriceEvolutionComponent`, or a rule on `VolumeExpansionHedgeComponent`) all ran. The fix belongs in step 3: name the pattern in the reference copy or the prompt. It is not made yet.

## What the engine reports, per plan (not a verdict)

The engine's own `forecast_return_corr_all_bars` per window, as written in `metrics.json`. It is not the plans' criteria: those are step 5's to apply, on the bars. It is shown here only to say the records are complete and not empty.

| plan | coin | windows | trades (sum) | forecast vs next return, all bars, per window |
|---|---|---|---|---|
| 001-01_rsi-high-extreme-reversal_1d | BTCUSD | 6 | 149 | +0.001, -0.001, +0.110, +0.014, -0.049, -0.000 |
| 001-01_rsi-high-extreme-reversal_1d | ETHUSD | 6 | 153 | -0.037, +0.014, +0.014, +0.072, +0.180, +0.029 |
| 001-01_rsi-high-extreme-reversal_1h | BTCUSD | 6 | 3325 | -0.001, +0.004, +0.008, -0.030, +0.001, -0.009 |
| 001-01_rsi-high-extreme-reversal_1h | ETHUSD | 6 | 3387 | -0.016, -0.012, -0.006, -0.007, +0.001, -0.005 |
| 001-02_rsi-low-extreme-rebound_1d | BTCUSD | 6 | 156 | -0.007, -0.039, +0.091, -0.033, +0.109, +0.000 |
| 001-02_rsi-low-extreme-rebound_1d | ETHUSD | 6 | 181 | -0.009, -0.094, +0.077, +0.029, +0.100, -0.029 |
| 001-02_rsi-low-extreme-rebound_1h | BTCUSD | 6 | 3268 | -0.010, +0.002, -0.003, -0.006, -0.021, +0.004 |
| 001-02_rsi-low-extreme-rebound_1h | ETHUSD | 6 | 3248 | -0.017, -0.024, -0.004, -0.015, +0.007, -0.002 |
| 001-03_rsi-high-extreme-continuation_1d | BTCUSD | 6 | 142 | -0.001, +0.001, -0.110, -0.014, +0.049, +0.000 |
| 001-03_rsi-high-extreme-continuation_1d | ETHUSD | 6 | 147 | +0.037, -0.014, -0.014, -0.072, -0.180, -0.029 |
| 001-03_rsi-high-extreme-continuation_1h | BTCUSD | 6 | 3787 | +0.002, -0.003, -0.016, +0.026, -0.001, +0.006 |
| 001-03_rsi-high-extreme-continuation_1h | ETHUSD | 6 | 3831 | +0.018, +0.013, -0.000, +0.004, -0.000, +0.003 |
| 001-04_rsi-low-extreme-continuation_1d | BTCUSD | 6 | 199 | -0.063, +0.037, -0.081, -0.038, -0.122, -0.001 |
| 001-04_rsi-low-extreme-continuation_1d | ETHUSD | 6 | 241 | +0.012, +0.104, -0.160, -0.068, -0.046, +0.028 |
| 001-04_rsi-low-extreme-continuation_1h | BTCUSD | 6 | 4009 | +0.016, -0.000, +0.001, +0.004, +0.018, -0.003 |
| 001-04_rsi-low-extreme-continuation_1h | ETHUSD | 6 | 4024 | +0.018, +0.021, +0.005, +0.016, -0.007, +0.003 |
| 002-01_sma-upcross-upward-drift_1d | BTCUSD | 6 | 30 | -0.109, n/a, n/a, -0.080, -0.008, -0.044 |
| 002-01_sma-upcross-upward-drift_1h | BTCUSD | 6 | 650 | +0.002, +0.005, -0.025, +0.020, -0.010, +0.012 |
| 002-02_sma-downcross-downward-drift_1d | BTCUSD | 6 | 62 | -0.127, -0.150, -0.034, -0.151, n/a, -0.072 |
| 002-02_sma-downcross-downward-drift_1h | BTCUSD | 6 | 763 | +0.011, +0.022, -0.016, +0.014, -0.004, -0.006 |
| 002-03_price-upcross-long-sma-drift_1d | BTCUSD | 6 | 47 | n/a, n/a, n/a, -0.189, -0.022, -0.032 |
| 002-03_price-upcross-long-sma-drift_1h | BTCUSD | 6 | 1327 | +0.014, -0.000, +0.001, +0.025, +0.001, +0.010 |
| 002-04_price-downcross-long-sma-drift_1d | BTCUSD | 6 | 118 | -0.248, -0.098, -0.149, -0.067, -0.087, +0.005 |
| 002-04_price-downcross-long-sma-drift_1h | BTCUSD | 6 | 1755 | +0.013, +0.019, -0.016, +0.025, -0.011, -0.021 |
| 002-05_sma-up-regime-positive-drift_1d | BTCUSD | 6 | 30 | -0.109, n/a, n/a, -0.080, -0.008, -0.044 |
| 002-05_sma-up-regime-positive-drift_1h | BTCUSD | 6 | 650 | +0.002, +0.005, -0.025, +0.020, -0.010, +0.012 |
| 002-06_sma-down-regime-negative-drift_1d | BTCUSD | 6 | 62 | -0.127, -0.150, -0.034, -0.151, n/a, -0.072 |
| 002-06_sma-down-regime-negative-drift_1h | BTCUSD | 6 | 763 | +0.011, +0.022, -0.016, +0.014, -0.004, -0.006 |
| 003-02_low-volume-down-move-reverts_1d | BTCUSD | 6 | 116 | +0.011, +0.154, -0.024, -0.132, -0.040, +0.029 |
| 003-03_high-volume-up-move-continues_1d | BTCUSD | 6 | 138 | -0.080, -0.039, -0.047, +0.127, -0.024, -0.020 |
| 003-03_high-volume-up-move-continues_1h | BTCUSD | 6 | 2643 | +0.003, +0.015, -0.026, +0.024, +0.015, -0.018 |
| 003-04_high-volume-down-move-continues_1d | BTCUSD | 6 | 128 | -0.016, +0.062, -0.006, -0.043, -0.020, -0.140 |
| 003-04_high-volume-down-move-continues_1h | BTCUSD | 6 | 2729 | -0.003, +0.004, -0.008, -0.011, -0.024, -0.024 |
| 003-05_up-move-retrace-by-volume_1h | BTCUSD | 6 | 6185 | -0.001, -0.007, -0.020, +0.021, +0.028, -0.017 |
| 003-06_down-move-retrace-by-volume_1d | BTCUSD | 6 | 250 | -0.024, +0.135, -0.019, -0.113, -0.004, -0.097 |

