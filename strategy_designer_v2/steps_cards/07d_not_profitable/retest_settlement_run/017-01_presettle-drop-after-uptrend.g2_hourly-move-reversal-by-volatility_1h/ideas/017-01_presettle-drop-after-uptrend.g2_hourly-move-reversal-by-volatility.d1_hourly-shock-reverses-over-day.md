---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's last 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would hold a position against an unusually large hourly move for about a day rather than an hour, larger as the move is larger relative to recent volatility, so the captured move exceeds the cost of the trade.
Why:
- F1: The book loses on costs it can never cover: 364,283 trades with a median length of 60 minutes lose 0.20 % each before fees and 0.30 % after, and the idea's one-hour move per case is +0.01 % against a 0.19 % round-trip cost. Even the strongest one-hour bucket (moves of 1–2 usual moves) gives only +0.036 % (t 9.2, 83,732 cases), so the Sharpe of -13.77 and Calmar of -0.99 come from turnover (20.77 trades a day), not from a missing effect.
- F2: The same reversal grows with the horizon up to a day. For hourly moves of 1–3 usual moves, the unusual move on non-overlapping grids is +0.030 % at 6 h (t 1.6), +0.124 % at 12 h (t 3.4, 9,382 cases) and +0.326 % at 24 h (t 4.5, 4,877 cases). The 24 h strength is 0.064 and the total move is +0.326 %, which covers the 0.19 % cost. By 48 h it fades to +0.12 % (t 0.85), and the 24 h slope t is 4.18 against -0.20 at 48 h.
- F4: At 24 h both sides reverse and no single coin carries the result. Long after a down hour gives +0.253 % (t 2.55, 2,588 cases) and short after an up hour gives +0.348 % (t 3.46, 2,593 cases). Five of six coins give +0.21 % to +0.58 % (ZEC t 2.58, XRP t 2.37); ETH is weakest at +0.031 % (t 0.19). By window group, w1–w18 give +0.30 % to +0.54 % (t 2.7–3.1) and w19–w24 give -0.05 % (t -0.39).
