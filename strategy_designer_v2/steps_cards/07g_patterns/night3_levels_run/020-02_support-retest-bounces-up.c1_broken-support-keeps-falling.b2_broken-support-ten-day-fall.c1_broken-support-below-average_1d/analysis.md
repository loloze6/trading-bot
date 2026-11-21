---
line: 7.g patterns
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3961 USD
---
## Findings
- **F1:** The tested short signal hardly moves the coin. On the 10-day grid, cases with a forecast of -2 or below were followed by an unusual move of only -0.059 of a usual move (627 cases), against +0.027 for weaker forecasts and +0.037 for a flat forecast. The short's edge was smaller than the coin's normal drift against it. Every coin's trades lost on average after fees, from -0.39 % (ETH, 361 trades) to -4.57 % (XRP, 432 trades), and 33 % to 42 % of trades won.
- **F2:** The book's worst days are simply the coin's strongest up days. In its lowest decile of daily returns the book lost 5.4 % on days the coin rose 6.2 %, and in its highest decile it gained 5.0 % on days the coin fell 6.0 %. The 5 days before were near flat in both (-0.8 % and -0.3 %). No pattern in the bars announced the losses: they are the short position's own exposure.
- **F3:** The strongest pattern was a close far above its 20-day average, and it is not strong enough to count. The top quintile of that distance was followed by a 10-day unusual rise of 0.197 of a usual move (t 2.84, 282 cases; raw +4.6 %), and the top-minus-bottom t was 2.60. It does not hold up in four ways:
- **F4:** The other angles show the same weak, unordered continuation. The 10-day return's top quintile was followed by +0.153 of a usual move (t 2.44, 312 cases), but the top-minus-bottom t was 1.86. The quintiles of distance from the 30-day high, 30-day return, 20-day volatility, 1-day and 3-day returns and the day's range have top-minus-bottom t between -0.63 and 1.69. No single coin's rank correlation between distance from the 20-day average and its 10-day move reaches significance (p 0.22 to 0.77).
- **F5:** Below the 50-day average the coin's 10-day unusual move was -0.040 of a usual move (872 cases), against +0.042 above it (819 cases). That is a difference of about 0.08 of a usual move, small next to the 0.11 to 0.20 standard deviation of a coin's 10-day return.

## Ideas
- No ideas: About nine conditions were looked at over three horizons, and the best pattern was continuation after a close far above the 20-day average (t 2.84 in one quintile). It is unordered across quintiles, reverses at 20 days and changes sign in three of eight years, so it cannot be told apart from chance after that many looks; no other angle came close.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
