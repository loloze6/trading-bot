---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 5 days above its usual drift, the effect lying in days wider than the norm.
Consequence: A trader should take only the long side after wide-range days, sized by how far the range exceeds its norm, and should not short coins on narrow days.
Why:
- F1: The book was short more often than long (9616 short coin-bars against 7557 long), because the forecast turns negative whenever the day's range is narrower than usual; the shorts lost (mean gain −0.0088 % per bar, allocation −0.109) while the longs earned (+0.0426 % per bar, allocation +0.187).
- F2: The positions were small (mean |allocation| 0.14), so the book earned only 0.0101 % a day across 99 % of coin-days in a position, against the required 0.05 %; this gap and the losing shorts in F1 explain the failed mean on days in a position.
- F3: The effect sits on the wide side only. On the 5-day grid, the 4th and 5th range-ratio quintiles have excess returns of +0.81 % (t 1.99, n 568) and +0.76 % (t 1.53, n 569), while the narrowest quintile is near zero (−0.25 %, t −0.55, total +0.39 %); narrow days give no clean short.
- F7: Rebuilt books with costs, against holding (Sharpe 0.56, Calmar 0.17, mean in position 0.117 %):
