---
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation_1d
idea tested: 010-01_rsi-above-share-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3433 USD
---
## Findings
- **F1:** The forecast's link to the next 14 days holds only when the coin's own 30-day volatility is below its median. There the slope of next 14-day excess return on the forecast has t = 2.55 (n = 266 non-overlapping samples). In the high-volatility half it is t = -0.79 (n = 118). Pooled over all samples it is t = 1.65 (n = 384).
- **F2:** The book's gain is almost all timing, not the market's own rise. Mean gain per bar is 0.00102, of which the market part is 0.000032 and the timing part 0.000989, with a mean position of only 0.026.
- **F3:** Long bars carry the book, short bars do not, and this holds in both volatility halves. Long bars earn 0.00188 per bar in low volatility (t = 2.81, n = 1858) and 0.00190 in high volatility (t = 2.55, n = 935). Short bars earn 0.00040 (t = 0.64) and -0.00003 (t = -0.04).
- **F4:** Long trades win through a long right tail, while short trades mostly lose. Longs have a median of -1.1 %, a 90th percentile of +42.4 % and 45 % winners. Shorts have a median of -4.4 %, a 90th percentile of +20.7 % and 36 % winners.
- **F5:** Most angles on the bars themselves show nothing distinguishable from chance, and nothing else stands out after this many angles. No |t| above 1.8 appeared for 7-day returns by past 7-day return, 30-day volatility or daily range quintile, or for 14-day returns on past 14, 30 or 60-day returns. Wednesday's next-day excess return of -0.0039 (t = -2.38, n = 830) is the one weekday of seven to clear |t| = 2, and it comes mostly from a single year, 2019 (t = -3.41).

## Ideas
- `010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets` (from F1, F2): The larger the share of the past 30 days that a coin's 14-day RSI has spent above 50, the higher the coin's return over the next 14 days. This holds when the coin's 30-day volatility of daily returns is low relative to its own history.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
