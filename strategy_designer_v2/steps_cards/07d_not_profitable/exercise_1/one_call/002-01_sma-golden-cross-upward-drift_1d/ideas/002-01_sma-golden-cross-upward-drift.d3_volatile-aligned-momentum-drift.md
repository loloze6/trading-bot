---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day and 60-day returns are both positive and its recent daily volatility is high relative to its own history, its next-day return is above its average.
Consequence: A trader would size trend longs up in volatile, momentum-aligned states and stay small in calm ones.
Why:
- F6: On active bars the gain is concentrated in volatile states. The next-day return is -0.00001 in the calmest volatility tercile, 0.00095 in the middle one and 0.00364 in the most volatile.
- F2: Inside the active (50>200) state, the gain sits only where 20-day and 60-day momentum are both positive.
- F7: The aligned-momentum effect weakens over time. It earned r1n 0.0075 (t=4.05, f10 0.070) in 2018–21 and 0.0015 (t=1.03, f10 0.024) in 2022–25.
