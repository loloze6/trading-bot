# Review of the backtests in this folder

Step 4, unchanged helper and engine, on the 10 hourly plans, fold A: every plan ran 6 of 6 windows per coin (BTC and ETH for brief 001; BNB has no data on the venue; BTC for brief 002). About 45 minutes. The run and its review, with the books' exposure: `../../../HOURLY_RUN.md`.

The engine's own figures (not a verdict):

| plan | coin | windows | trades (sum) | forecast vs next return, all bars, per window |
|---|---|---|---|---|
| 001-01_rsi-high-extreme-reversal-down_1h | BTCUSD | 6 | 3829 | -0.002, +0.003, +0.016, -0.026, +0.001, -0.006 |
| 001-01_rsi-high-extreme-reversal-down_1h | ETHUSD | 6 | 3871 | -0.018, -0.013, +0.000, -0.004, +0.000, -0.003 |
| 001-02_rsi-low-extreme-reversal-up_1h | BTCUSD | 6 | 3871 | -0.012, -0.004, +0.004, -0.005, -0.023, +0.004 |
| 001-02_rsi-low-extreme-reversal-up_1h | ETHUSD | 6 | 3845 | -0.026, -0.021, -0.006, -0.023, +0.003, +0.004 |
| 001-03_rsi-high-extreme-continuation-up_1h | BTCUSD | 6 | 3787 | +0.002, -0.003, -0.016, +0.026, -0.001, +0.006 |
| 001-03_rsi-high-extreme-continuation-up_1h | ETHUSD | 6 | 3831 | +0.018, +0.013, -0.000, +0.004, -0.000, +0.003 |
| 001-04_rsi-low-extreme-continuation-down_1h | BTCUSD | 6 | 3320 | +0.010, -0.002, +0.003, +0.006, +0.021, -0.004 |
| 001-04_rsi-low-extreme-continuation-down_1h | ETHUSD | 6 | 3346 | +0.017, +0.024, +0.004, +0.015, -0.007, +0.002 |
| 002-01_sma-cross-up-drift-up_1h | BTCUSD | 6 | 650 | +0.002, +0.005, -0.025, +0.020, -0.010, +0.012 |
| 002-02_sma-cross-down-drift-down_1h | BTCUSD | 6 | 763 | +0.011, +0.022, -0.016, +0.014, -0.004, -0.006 |
| 002-03_price-cross-above-sma-up_1h | BTCUSD | 6 | 1327 | +0.014, -0.000, +0.001, +0.025, +0.001, +0.010 |
| 002-04_price-cross-below-sma-down_1h | BTCUSD | 6 | 1755 | +0.013, +0.019, -0.016, +0.025, -0.011, -0.021 |
| 002-05_short-above-long-sma-drift-up_1h | BTCUSD | 6 | 650 | +0.002, +0.005, -0.025, +0.020, -0.010, +0.012 |
| 002-06_short-below-long-sma-drift-down_1h | BTCUSD | 6 | 763 | +0.011, +0.022, -0.016, +0.014, -0.004, -0.006 |
