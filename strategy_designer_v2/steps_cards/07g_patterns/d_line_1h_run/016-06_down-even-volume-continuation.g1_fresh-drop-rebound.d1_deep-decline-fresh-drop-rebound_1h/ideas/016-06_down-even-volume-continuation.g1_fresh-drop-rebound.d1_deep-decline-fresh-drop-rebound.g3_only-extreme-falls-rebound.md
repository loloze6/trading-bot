---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, its rebound over the next 3 days grows with how extreme the combined depth of its 3-day fall and its fresh 1-day drop is relative to its recent swings, and the coin keeps falling after mid-sized combined falls.
Consequence: Buy only the most extreme combined declines, scaled by their extremity, and refuse the mid-sized dips that make up most of the tested signal's trades.
Why:
- F4: The tested rebound lives only in the top fifth of the forecast: active cases in the top forecast quintile earn +0.0112 excess 72-bar return (t 3.30, 553 cases), while the 2nd and 3rd quintiles lose −0.0065 (t −1.79) and −0.0082 (t −2.14), and active cases overall return −0.0015 against +0.0014 for inactive ones.
- F5: Across all grid cases, the past 72-bar return gives a U-shape: the middle quintile is followed by −0.0071 excess (t −3.20, 1107 cases), the top quintile by +0.0055 (t 1.85) and the bottom by +0.0016.
- F6: The book still loses: mean daily return is −0.000787 against +0.001179 for holding (Sharpe −1.04, 2,898 book-days, correlation with holding 0.67), on 61,365 trades with a median length of 8 hours and a mean of −0.47% before fees and −0.57% after; per bar the position's gain is 0.000005 against a market part of 0.000013, so its timing is negative.
