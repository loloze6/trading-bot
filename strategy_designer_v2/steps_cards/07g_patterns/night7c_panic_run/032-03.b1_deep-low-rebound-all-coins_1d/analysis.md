---
line: 7.g patterns
backtest: 032-03.b1_deep-low-rebound-all-coins_1d
idea tested: 032-03.b1_deep-low-rebound-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3771 USD
---
## Findings
- **F1:** The nearer a coin's close is to its highest close of the past 20 days, the larger its unusual 5-day move. The rank slope is +1.78 % per standard deviation of rank, with day-pooled t 2.30, over 1641 non-overlapping cases on 256 days. It points the same way in fold B (+1.43 %, t 1.26) and fold C (+1.64 %, t 1.64).
- **F2:** Measured from the 30-day high, the same pattern holds. The slope is +1.95 % (t 2.33, 1475 cases, 230 days), and +1.92 % in fold B and +1.52 % in fold C. The quintile closest to the high moves +3.88 % unusually over 5 days (t 2.11, 93 days).
- **F3:** The pattern is not a straight line. Closes in the second-lowest quintile of distance from the 20-day high are followed by a −3.77 % unusual 5-day move (t −3.74, 127 days), in both fold B (−3.95 %, t −3.52) and fold C (−5.76 %, t −3.86). The deepest quintile is flat (−0.53 %, t −0.35), so moderate pullbacks keep falling while deep falls do not.
- **F4:** The tested situation shows no rebound on these folds. The 63 grid cases in the recorded mean_reversion regime move +0.39 % unusually (t 0.19). The 109 grid cases closing at a 30-day low move −1.25 % (t −0.82). The cost of a trade is 0.22 %.
- **F5:** Inside the book, the grading by forecast shows in the trades. Trades in the lowest quarter of entry forecast (mean 3.8) lose −1.96 % net. The other three quarters (mean forecast 7.3 to 16.5) earn +5.6 % to +7.0 % net, with win rates of 71 % to 83 %, on about 84 trades each.
- **F6:** The other angles show nothing that holds after pooling cases of the same day. By weekday, the largest |t| is 1.64. The quintiles of recent range expansion against the 60-day range reach at most t −1.74, and the rank slope on range expansion is t −0.04.

## Ideas
- `032-03.b1.g1_closeness-to-monthly-high` (from F1, F2, F3): In a coin, the nearer its daily close is to the highest close of the past 30 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
