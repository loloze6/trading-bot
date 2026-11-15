---
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
idea tested: 002-05_sma-up-regime-positive-drift
step 5: not observable
step 6: none
mode: one call
explorations: 1
cost: 0.1623 USD
---
## Findings
- **F1:** The test ran on one coin (BTCUSD) and one window (w1, year 2022) of only 120 daily bars, not the 6 windows the plan pooled over. Only 13 bars (10.8 %) had a positive forecast and 107 had none. That is short of the plan's 100 in-stretch bars and gives 1 up-cross stretch against the 3 required.
- **F2:** The single stretch was already under way at the window's start. It covered bars 0 to 12, all in the first quarter of the window. The 50-day SMA's spread over the 200-day SMA then fell from +50.3 to -56.9 on the standardised scale, averaging -75.0, -83.9 and -63.6 over the later three quarters. The window caught the end of one bull stretch and a bear market, with no new upward cross.
- **F3:** The forecast matched the raw spread's sign exactly: 0 bars had a positive spread and a zero forecast, and 0 bars the reverse. The forecast's peak was 6.47 and its in-stretch mean 3.34. The shortfall therefore comes from the data's span, not from a config that rarely reaches the situation.
- **F4:** The outcome is noisy compared with any plausible drift.

## Ideas
- `002-05_sma-up-regime-positive-drift.a1_sma-up-regime-positive-drift` (from F1, F2, F3, F4): While a coin's 50-day simple moving average stands above its 200-day simple moving average, the coin's return over the next day is higher than its average daily return, and the further the 50-day average stands above the 200-day one, the higher that return.
- `002-05_sma-up-regime-positive-drift.a2_sma-up-regime-drift-wide` (from F1, F2, F4): While a coin's 50-day simple moving average stands above its 200-day simple moving average, the coin's return over the next day is higher than its average daily return, and the further the 50-day average stands above the 200-day one, the higher that return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
