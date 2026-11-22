---
line: 7.b inconclusive
backtest: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3465 USD
---
## Findings
- **F1:** The test's cases were mostly not sharp rises: because the forecast was re-standardised over 60 bars, a forecast of at least 2 points (median 10.1) was hit on modest up days. Of the 1,064 plan-like cases, 613 had a raw one-day rise of only 0 to 1 usual daily moves (the day's return over the 20-day volatility). Those cases had 10-day unusual moves of -1.09 % (t -1.28, n 306) for 0 to 0.5 moves and -0.37 % (t -0.37, n 307) for 0.5 to 1 moves, which pulled the mean down to -0.30 % (t -0.54).
- **F2:** Among the plan's cases, the 10-day unusual move rises with the raw size of the rise. It is -1.09 % for 0 to 0.5 usual moves, -0.37 % for 0.5 to 1, -2.09 % for 1 to 1.5, +2.26 % (t 1.07, n 92) for 1.5 to 2, and +4.42 % (t 1.86, n 102) above 2. Over 20 days the bin above 2 moves reach +7.83 % (t 2.28).
- **F3:** Measured on the raw size directly, sharp rises in rising coins continue, on non-overlapping 10-day cells. The first day per cell of at least 1.5 usual moves in the trending regime is followed by a 10-day unusual move of +3.34 % (t 3.15, n 457), and of +4.22 % (t 3.12, n 257) for at least 2 moves. Below that, from 1 usual move, the move is only +0.78 % (t 1.03, n 698).
- **F4:** The continuation belongs to rising coins. The same sharp rises of at least 1.5 usual moves in coins whose 90-day return is not positive are followed by -0.41 % over 10 days (t -0.43, n 342), against +3.31 % (t 3.09, n 445) in rising coins.
- **F5:** The effect grows with the horizon. For sharp rises of at least 1.5 moves in rising coins, the unusual move is +1.16 % over 5 days (t 1.96), +3.34 % over 10 days (t 3.15) and +6.01 % over 20 days (t 3.66).
- **F6:** The effect is mixed across years and coins. For sharp rises in rising coins it is negative in 2018 (-4.4 %, n 19), 2022 (-4.6 %, n 14) and 2023 (-1.5 %, n 69), and strongest in 2021 (+8.8 %, t 2.46) and 2024 (+7.6 %, t 3.16). By coin it ranges from -0.5 % in XMR to +8.7 % in ZEC (t 2.34).
- **F7:** Above 1.5 usual moves the effect is not graded further: the correlation between the rise's size and the 10-day unusual move is 0.008. Most of the grading lies between ordinary up days and sharp ones (F2).

## Ideas
- `025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends` (from F1, F2, F3, F4): In a coin whose 90-day return is positive, the larger the day's rise measured against the standard deviation of its last 20 daily returns, the larger its rise over the next 10 days. Up days that are only ordinary against that volatility are followed by no rise, and rises of several usual daily moves are followed by the largest.
- `025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b2_sharp-rises-three-week-continuation` (from F3, F4, F5): In a coin whose 90-day return is positive, the larger the day's rise measured against the standard deviation of its last 20 daily returns, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
