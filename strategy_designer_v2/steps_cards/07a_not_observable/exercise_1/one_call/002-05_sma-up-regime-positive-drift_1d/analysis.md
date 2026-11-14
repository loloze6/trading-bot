---
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
idea tested: 002-05_sma-up-regime-positive-drift
step 5: not observable
step 6: none
mode: one call
explorations: 1
cost: 0.1256 USD
---
## Findings
- **F1:** The test had one coin (BTCUSD) and one window (w1) of only 120 daily bars, so it found 13 in-stretch bars against the plan's minimum of 100 and 1 up-cross stretch against the minimum of 3; the 106 out-of-stretch bars just met their own minimum of 100.
- **F2:** The only up-stretch is not a new cross: it was already under way at the window's first bar and covers bars 0 to 12 (raw spread positive in 10.8% of bars, max 50.3); the next 107 bars all have the 50-day SMA below the 200-day SMA.
- **F3:** After the stretch the spread moved further away from a new up-cross, not toward one: its raw mean was -85.4 in the window's middle third (min -92.0) and still -66.4 in the last third (max -56.9). BTC fell 21.1% over the window, so the window held one down-regime, and the 50/200-day regime lasts longer than the window itself.
- **F4:** The outcome is very noisy compared with the effect the plan looks for: next-bar returns have a standard deviation of 0.0332 (0.0233 in-stretch, 0.0342 out). With 13 in-stretch bars the standard error of their mean is about 0.0065, so even the observed -0.0069 difference gives only t = -0.95.
- **F5:** The forecast's spread follows the regime exactly: it is 0 on 75% or more of bars (median 0, mean 0.36, max 6.47), and it is positive on exactly the raw-positive bars (0 mismatches). The book made only 3 trades, so the config reaches its situation as designed, and the shortfall comes from too little data.

## Ideas
- `002-05_sma-up-regime-positive-drift.a1_daily-golden-cross-regime-drift` (from F1, F2, F3, F4): On BTC daily bars over many years, the bars where the 50-day SMA is above the 200-day SMA (from an up-cross to the next down-cross) are followed by a higher mean next-day close-to-close return than the bars where it is below.
- `002-05_sma-up-regime-positive-drift.a2_hourly-sma-cross-regime-drift` (from F1, F2, F3, F5): On BTC hourly bars, the bars where the 50-bar SMA is above the 200-bar SMA (from an up-cross to the next down-cross) are followed by a higher mean next-hour return than the bars where it is below.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
