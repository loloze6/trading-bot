---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 50-day SMA has just crossed below its 200-day SMA and the gap is still widening, the coin's price rises over the following ten daily bars more than its usual drift, because the fresh death cross marks the exhaustion of the selloff.
Consequence: Refuse new shorts on a fresh, still-widening death cross and consider it a zone where rebounds are more likely than continuation.
Why:
- F1: Bars where the 50-day SMA had only just fallen below the 200-day SMA (raw spread between -40 and +1, the fourth octile) were followed by a 10-bar return 2.18% above the coin's mean, with t = 2.76 and 58.4% up. This was the only spread octile that cleared |t| > 2, and its sign is the opposite of what the death-cross short expects.
- F2: Inside that near-cross zone, the rebound came mostly when the spread was still widening downward over the past 10 bars: +3.46% 10-bar excess, t = 3.17, 62.9% up, n = 1066. When the spread was already narrowing the excess was +0.84%, t = 0.75. The pattern held in both early and late windows (t = 1.86 and 2.12) and pointed the same way in all six coins (+1.3% to +5.6%).
- F5: The short book's 10-bar excess depended on the year, not on the cross. While the forecast was short it was +6.2% (t = 4.23) in 2020, +4.8% (t = 2.45) in 2021, +2.2% (t = 2.35) in 2023 and +3.3% (t = 2.89) in 2024, in the coin's favour against the short. It helped the short only in 2018 and 2022. This lines up with the trades: 143 to 272 trades per coin, win rates of 19% to 28%, and mean net losses of -8.5% to -14.9% per trade.
