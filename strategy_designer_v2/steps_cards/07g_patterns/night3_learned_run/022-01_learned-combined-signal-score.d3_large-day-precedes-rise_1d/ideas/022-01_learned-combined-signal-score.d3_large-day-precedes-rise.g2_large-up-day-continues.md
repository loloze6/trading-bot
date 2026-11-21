---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's rise over its last day, measured against its usual daily move over the past 60 days, the higher its return over the next 5 days, beyond the following day.
Consequence: Treat an unusually large up day as a reason to lean long the coin for the next 5 days, and treat a large down day as no such reason.
Why:
- F3: The tested idea's 5-day lean after large days is carried by large up days, not large down days. The top fifth of signed scaled 1-day returns is followed by +1.43 % excess over 5 days (t 2.78, 540 cases), the bottom fifth by +0.18 % (t 0.46, 540). Within up days, the largest third against the smallest differs by +1.31 % (t 1.68, 1316 cases); within down days by +0.17 % (t 0.28, 1381).
- F4: The 5-day rise after large up days is not the next day's move. From the close one day after the signal to day 5, the top fifth still earns +1.30 % excess against +1.51 % from the signal's close. Signed top-minus-bottom fifths differ by similar amounts in both halves of the windows: +1.48 % (t 2.00, 1344 cases) and +1.58 % (t 1.55, 1355).
- F5: The 5-day continuation after large up days is concentrated in the more volatile coins. Signed top-minus-bottom fifths over 5 days are +3.51 % on XRP (t 1.87) and +3.52 % on ZEC (t 1.54), against +0.27 % on BTC, +0.40 % on ETH and +0.52 % on LTC (|t| < 0.7, about 450 cases each).
