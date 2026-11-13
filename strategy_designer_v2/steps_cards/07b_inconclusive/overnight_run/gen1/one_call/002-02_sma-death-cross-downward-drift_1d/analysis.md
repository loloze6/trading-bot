---
line: 7.b inconclusive
backtest: 002-02_sma-death-cross-downward-drift_1d
idea tested: 002-02_sma-death-cross-downward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3273 USD
---
## Findings
- **F1:** The short's result is swamped by the market's own moves. The per-case excess gain has a standard deviation of 0.137 against a pooled weighted mean of 0.0022 (t 0.39, hit 52%, n 825), and it correlates 0.71 with BTC's own forward fall. When BTC's next 10 bars go down, the excess gain is +0.086 (t 13.5, hit 85%). When they go up, it is -0.076 (t -10.9, hit 22%).
- **F2:** The sign flips by period rather than by coin, so the pooled result cancels out. 2018 gives +0.037 (t 1.75) and 2019 gives +0.016 (t 1.87). 2020 gives -0.079 (t -4.44) and 2021 gives -0.063 (t -2.54). Every coin sits near zero, between t -0.57 and t 0.75.
- **F3:** The short works where the coin is in a moderate drawdown from its 60-bar high. That middle tercile gives +0.028 (t 2.95, hit 58%, n 227). The deepest-drawdown tercile gives -0.011 (t -1.07) and the near-high tercile gives +0.001 (t 0.10).
- **F4:** Within the moderate-drawdown cases, the gain is concentrated where price has bounced back above its 20-bar SMA: +0.055 (t 3.39, hit 61%, n 95). The same drawdown with price below its 20-bar SMA gives +0.009 (t 0.80). Deep drawdown with price above its 20-bar SMA gives -0.033 (t -1.48).
- **F5:** The forecast's size does not grade the effect. The low, mid and high |forecast| terciles give -0.005, +0.006 and +0.002, all with |t| < 0.7. The deepest raw-spread tercile is only +0.007 (t 0.71).
- **F6:** Fresh death crosses tend to reverse rather than persist. Cases at most 20 bars after the cross give -0.026 (t -1.60, hit 41%). Cases 51 to 100 bars after give +0.016 (t 0.83).

## Ideas
- `002-02_sma-death-cross-downward-drift.b1_short-relief-bounce-in-downtrend` (from F3, F4, F1): When a coin's 50-day SMA is below its 200-day SMA, and price is in a moderate drawdown from its 60-day high (neither near the high nor at the deepest lows) and has bounced back above its 20-day SMA, the coin falls over the next 10 days by more than its average 10-day move.
- `002-02_sma-death-cross-downward-drift.b2_fresh-death-cross-reverses` (from F6, F2): When a coin's 50-day SMA has just crossed below its 200-day SMA, within the last 20 bars, the coin rises over the next 10 days by more than its average 10-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
