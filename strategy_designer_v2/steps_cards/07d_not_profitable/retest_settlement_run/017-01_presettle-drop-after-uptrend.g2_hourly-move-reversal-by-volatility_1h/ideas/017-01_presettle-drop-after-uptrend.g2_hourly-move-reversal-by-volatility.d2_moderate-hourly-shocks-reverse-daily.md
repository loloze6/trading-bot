---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Among hourly moves of up to a few times a coin's 24-hour volatility, the larger its last 1-hour return relative to that volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would fade moderate hourly shocks over a day, larger as the shock is larger, and would not fade the most extreme hourly moves, which do not reverse.
Why:
- F2: The same reversal grows with the horizon up to a day. For hourly moves of 1–3 usual moves, the unusual move on non-overlapping grids is +0.030 % at 6 h (t 1.6), +0.124 % at 12 h (t 3.4, 9,382 cases) and +0.326 % at 24 h (t 4.5, 4,877 cases). The 24 h strength is 0.064 and the total move is +0.326 %, which covers the 0.19 % cost. By 48 h it fades to +0.12 % (t 0.85), and the 24 h slope t is 4.18 against -0.20 at 48 h.
- F3: Within the 24-hour horizon the effect is graded, but only up to about three usual moves. At 24 h the unusual move is +0.120 % for moves of 0–1 usual moves, +0.299 % for 1–2 and +0.445 % for 2–3; moves of 3–4 give -0.002 % and moves above 4 give -0.53 %. At 12 h, 3–4 gives -0.16 % and above 4 gives -0.60 %. So the largest shocks do not reverse, yet the uncapped linear forecast bets hardest on them.
- F5: The cumulative move does not carry the reversal; the single-hour shock does. A 6-hour summed scaled move of 2–3 usual moves continues instead of reversing: -0.195 % at 6 h (t -3.4) and -0.377 % at 12 h (t -3.5).
