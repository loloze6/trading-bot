---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over its last day, measured against its own 20-day volatility of daily returns, the higher its return over the next day.
Consequence: A trader should buy an unusually large down-day for a one-day rebound and refuse a short at that close.
Why:
- F1: On daily bars, a large daily fall is followed by a rebound the next day. Daily returns were scaled by each coin's own 20-day volatility. In the bottom fifth of these scaled returns, the next day's return beats the coin's drift by +0.46 % (strength 0.095, t 4.9, 3162 non-overlapping cases), about 2.4 times the 0.19 % round trip. Over all bars, the next-day slope on the scaled return is negative (t -4.9, n 15796). These t's pool six coins on the same days, so they overstate the independent evidence.
- F2: The rebound after a large fall does not last. It is +0.17 % at 3 days (t 0.6, n 1032) and -0.19 % at 5 days (t -0.5, n 600).
