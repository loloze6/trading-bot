---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When the 50-day SMA is above the 200-day SMA but the close has fallen below the 50-day SMA, or the 20-day return has turned negative, the coin's next days' returns fall below its average.
Consequence: A trader in a golden-cross uptrend would cut the long whenever the close drops back under the 50-day SMA or short-term momentum turns down, which removes the whipsaw losses.
Why:
- F2: Inside the active (50>200) state, the gain sits only where 20-day and 60-day momentum are both positive.
- F3: On active bars, a close above the 50-day SMA is followed by +0.00316 next-day return (t=3.2, n=2527). A close below it is followed by -0.00182 (t=-1.48, n=1927).
- F1: A larger forecast does not earn more. The forward 10-bar return is 0.0146 at forecast 0–5, 0.0167 at 5–10, 0.0081 at 10–15, 0.0049 at 15–20 and 0.0238 at the cap, against 0.0128 on flat bars. The next-day return on active bars is 0.00127, about the same as 0.00130 on flat bars, while volatility is higher (sd 0.053 vs 0.043).
- F5: The book loses through whipsaw, not fees.
