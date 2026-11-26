---
line: 7.g patterns
backtest: 032-01.b1.b1.e2_choppy-market-weekly-move-continues_1d
idea tested: 032-01.b1.b1.e2_choppy-market-weekly-move-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3719 USD
---
## Findings
- **F1:** The weekly continuation lives in calm markets, not agitated ones. On the non-overlapping 7-day grid, the slope of the drift-removed next-7-day return on the scaled 7-day move has t 4.09 (n 293) in the lowest third of each coin's 30-day volatility, t 1.86 (n 292) in the middle third and t −0.89 (n 274) in the highest. Split by the 30-day against the 90-day volatility, it has t 3.57 (n 203) when calmer than usual, t 2.86 (n 185) when about the same and t −0.26 (n 183) when more agitated.
- **F2:** Over one day, a coin's daily move scaled by its 30-day swings reverses. The slope of the next day's drift-removed return on it has t −5.26 over 6529 days, and it is concentrated in high volatility: t −5.94 (n 2180) in the highest third of 30-day volatility, −1.84 in the middle and −0.57 in the lowest.
- **F3:** That next-day reversal holds across coins and years. It is negative on all 6 coins (t from −0.67 on XRP to −4.07 on XMR, five of them at or below −1.76) and in every year (t −3.61, −2.86, −4.19 in 2018–2020 and −0.66 in 2021). It is largest after the biggest falls: the lowest fifth of scaled daily moves is followed by +0.65 % the next day (t 4.40, n 1303), 3.4 times the 0.19 % cost of a trade.
- **F4:** The tested continuation is graded only in its top and bottom fifths. Inside choppy bars (ER ≤ 0.3), the top fifth of scaled 7-day moves is followed by +4.56 % beyond drift (t 3.40, n 119) and the lowest by −1.98 % (t −1.62). The slope is similar for ER 0–0.15 (t 2.64, n 323) and 0.15–0.3 (t 3.41, n 289), and is nil above 0.3 (t 0.03, n 211).
- **F5:** The direction of the move flips with the horizon. A 3-day move scaled by 30-day swings continues over the next 3 days (t 3.43, n 2142 non-overlapping cases), while a single day's scaled move points the other way over the same 3 days (t −1.30).
- **F6:** The book's gain is timing, and it comes from its longs. Its mean daily gain per coin-day is 0.080 %, of which the market's own drift is 0.0035 %. Its long days average +0.195 % (n 3703) and its short days −0.007 % (n 3926).

## Ideas
- `032-01.b1.b1.e2.g1_calm-market-weekly-move-continues` (from F1, F4): When a coin's daily swings over the past 30 days are small compared with its swings over the past 90 days, its 7-day move counted in its 30-day daily swings is followed by a move the same way over the next 7 days. The larger that scaled 7-day move, and the calmer the past 30 days against the past 90, the larger the following move.
- `032-01.b1.b1.e2.g2_agitated-market-daily-move-reverses` (from F2, F3, F5): When a coin's daily swings over the past 30 days are large compared with its swings over the past 90 days, its 1-day return counted in its 30-day daily swings is followed by a move the opposite way over the next day. The larger that scaled daily move, and the more agitated the past 30 days, the larger the reversal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
