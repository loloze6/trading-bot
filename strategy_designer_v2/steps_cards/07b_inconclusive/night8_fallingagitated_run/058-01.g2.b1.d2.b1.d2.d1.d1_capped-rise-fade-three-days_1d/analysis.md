---
line: 7.b inconclusive
backtest: 058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3722 USD
---
## Findings
- **F1:** The give-back the idea predicts happens on the next day and is gone by the third. On the 3-day grid in folds B and C, the unusual move of the short cases is +1.44 % over 1 day (t 2.84, 169 days, 329 cases), +1.03 % over 2 days (t 1.26) and +0.84 % over 3 days (t 1.06), falling to +0.64 % at 5 days (t 0.70). The test's 3-day horizon therefore measured the move after most of the signal had already been diluted by the market, which is why its result (+0.35 %, t 0.82) is on the predicted side but unclear.
- **F2:** Counted once per bar on a 1-day grid, the next-day unusual move is +0.93 % (t 2.00, 193 days, 417 cases), with a total move of +0.75 % per case, about 3.4 times the 0.22 % cost of a trade. The following day adds nothing: the second day's unusual move is −0.06 % (t −0.11). The fall is a one-day effect.
- **F3:** The one-day give-back grows with the raw rise against the 30-day swing, though weakly.
- **F4:** The strategy's standardised forecast does not grade the 1-day move. Its larger half falls +0.88 % against +0.99 % for its smaller half, and the correlation of forecast and move is −0.06. On the 3-day horizon its top quartile is negative (−0.72 %, t −0.46) while the middle quartiles are +1.74 % and +2.01 %. The forecast's 60-value standardisation scrambles the grading the idea states.
- **F5:** The 3-day effect is mixed across periods and coins.
- **F6:** No more data is available than the test used. It already ran all 19 coins on daily bars over folds A to D, so the tested idea cannot simply be re-run on more data.

## Ideas
- `058-01.g2.b1.d2.b1.d2.d1.d1.b1_capped-rise-fade-next-day` (from F1, F2, F3, F4, F5): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next day, only while that rise stays within about one usual swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
