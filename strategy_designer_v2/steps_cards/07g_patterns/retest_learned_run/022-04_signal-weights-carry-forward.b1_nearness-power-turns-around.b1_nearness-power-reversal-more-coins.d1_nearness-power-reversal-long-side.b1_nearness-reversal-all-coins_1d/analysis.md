---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6299 USD
---
## Findings
- **F1:** The tested forecast adds almost nothing to the coin's own drift: per 5-day grid cell, the excess return is not graded across forecast bins (0–2: +0.01 %, t 0.02; 2–5: +0.71 %, t 1.58; 5–10: −0.01 %, t −0.02; 10+: +0.70 %, t 1.83). On days in a position the book moves with its coin (correlation 0.68), so its +20.5 % a year is mostly the long side's drift (+0.71 % per case against an unusual move of −0.07 %).
- **F2:** The book's trades earn more the longer they are held, which is drift exposure rather than timing. The shortest quarter of trades (2.3 days) earns +2.1 % net and the longest quarter (55 days) earns +11.8 % net, while win rates stay flat at 0.55–0.63.
- **F3:** The weekday effect in 5-day excess returns does not survive clustering by date, so it is not a finding. Counted per coin cell, Tuesday is +2.2 % (t 4.4) and Sunday is −2.45 % (t −5.9). Averaged across coins per date, every weekday's t is between −1.2 and 1.0 (Tuesday +0.95 %, t 0.86; Sunday −0.26 %, t −0.23; about 74 dates each).
- **F4:** The next-day excess return after a Friday bar is +0.36 % (t 2.40, 414 dates, date-clustered) and positive in 7 of 8 years. This is the only one of 7 weekdays tested to reach t 2, it is a fixed calendar condition with no grading, and it does not stand out from the many angles examined.
- **F5:** The short reversal after 5-day moves does not hold up. Pooled over cells, the 5-day return's rank correlation with the next 5-day return is −0.069 (n 4579). Scaled by volatility, its quintiles are flat (−0.12 % to +0.60 %, every |t| < 1.2). Clustered by date, its product with the excess return has t 0.71 with the opposite sign. Its yearly rank correlation flips sign, from +0.26 (2018) and +0.17 (2021) to −0.14 (2022) and −0.13 (2023).
- **F6:** Large daily moves, the level of volatility and nearness to the 90-day high grade nothing over the next 5 days:

## Ideas
- No ideas: Across the forecast, the trades, the weekday, the year, recent returns, large moves, volatility and nearness to highs, no pattern was both graded and still clear of chance after clustering by date: the only t above 2 (Friday, F4) is a fixed calendar condition among many tests, and the strong pooled weekday and 5-day reversal results (F3, F5) disappear once dates are clustered.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
