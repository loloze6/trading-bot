---
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
idea tested: 002-05_sma-up-regime-positive-drift
step 5: not observable
step 6: none
mode: one call
explorations: 1
cost: 0.1472 USD
---
## Findings
- **F1:** The test ran on one coin and one window only (BTCUSD, w1, 2022, 120 bars), not the 6 windows the plan assumed, so it got 13 in-stretch bars against the 100 asked for, 107 out-of-stretch bars, and 1 up-cross stretch against the 3 asked for.
- **F2:** The window fell in a bear year where the 50-day SMA stayed below the 200-day SMA almost throughout: the only stretch was already under way at the window's first bar (positions 0–12, in-share 0.65 in the first 20-bar block, forecast mean 3.34, max 6.47), and the raw spread then stayed negative for every remaining 20-bar block, with block means from -49 to -89 and a low of -92.
- **F3:** With a 50-day/200-day cross, one stretch can last months, so a 120-bar window holds at most about one or two stretches (here raw-positive runs = 1); the plan's 3 distinct stretches need several coins or windows, not a single window.
- **F4:** The outcome is noisy compared with the effect: the next-bar return's standard deviation is 0.0332 against an observed difference of -0.0069 (Welch t -0.95, 13 vs 106 cases); at 100 cases per side the standard error of the difference would still be about 0.0047, so the test needs many hundreds of in-stretch bars across coins and years to separate a drift of a few tenths of a percent a day.

## Ideas
- `002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad` (from F1, F2, F3, F4): Over the stretch from an upward cross of the short average over the long average until the next downward cross, price rises more often and further than over random stretches of the same length.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
