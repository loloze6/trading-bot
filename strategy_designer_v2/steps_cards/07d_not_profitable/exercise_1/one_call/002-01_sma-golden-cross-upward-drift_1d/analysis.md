---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3117 USD
---
## Findings
- **F1:** A larger forecast does not earn more. The forward 10-bar return is 0.0146 at forecast 0–5, 0.0167 at 5–10, 0.0081 at 10–15, 0.0049 at 15–20 and 0.0238 at the cap, against 0.0128 on flat bars. The next-day return on active bars is 0.00127, about the same as 0.00130 on flat bars, while volatility is higher (sd 0.053 vs 0.043).
- **F2:** Inside the active (50>200) state, the gain sits only where 20-day and 60-day momentum are both positive.
- **F3:** On active bars, a close above the 50-day SMA is followed by +0.00316 next-day return (t=3.2, n=2527). A close below it is followed by -0.00182 (t=-1.48, n=1927).
- **F4:** On active bars, the next-day return rises with closeness to the 60-day high.
- **F5:** The book loses through whipsaw, not fees.
- **F6:** On active bars the gain is concentrated in volatile states. The next-day return is -0.00001 in the calmest volatility tercile, 0.00095 in the middle one and 0.00364 in the most volatile.
- **F7:** The aligned-momentum effect weakens over time. It earned r1n 0.0075 (t=4.05, f10 0.070) in 2018–21 and 0.0015 (t=1.03, f10 0.024) in 2022–25.
- **F8:** The forecast misses gains while flat. Flat bars with positive 20- and 60-day momentum return 0.0027 next day (t=2.03, n=1027), above the 0.0013 of active bars.
- **F9:** Risk is large for the gain, which is what fails Calmar (0.001). The mean per-window maximum drawdown is -28.7% and the worst is -96%.

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_new-high-breakout-continuation` (from F4, F8, F2): After a daily close at a new 60-day high, the coin keeps rising over the following days, more than from its other bars.
- `002-01_sma-golden-cross-upward-drift.d2_uptrend-pullback-drags-returns` (from F2, F3, F1, F5): When the 50-day SMA is above the 200-day SMA but the close has fallen below the 50-day SMA, or the 20-day return has turned negative, the coin's next days' returns fall below its average.
- `002-01_sma-golden-cross-upward-drift.d3_volatile-aligned-momentum-drift` (from F6, F2, F7): When a coin's 20-day and 60-day returns are both positive and its recent daily volatility is high relative to its own history, its next-day return is above its average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
