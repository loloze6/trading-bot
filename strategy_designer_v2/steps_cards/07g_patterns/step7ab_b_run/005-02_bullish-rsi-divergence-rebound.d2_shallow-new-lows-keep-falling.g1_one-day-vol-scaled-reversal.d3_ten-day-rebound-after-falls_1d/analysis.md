---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3184 USD
---
## Findings
- **F1:** The book is almost only exposure to the coin. It was long on 98.2 % of bars for both BTC and ETH. Its mean gain per bar (BTC 0.104 %, ETH 0.073 %) is below its gain from the coin's own rise (BTC 0.135 %, ETH 0.118 %), so its timing is negative: -0.032 % per bar on BTC and -0.046 % on ETH.
- **F2:** The idea's unusual move is -0.20 % per case over 10 days (strength -0.013, 553 cases), against a round trip of 0.11 %. The total move of +1.06 % is mostly the coin's normal drift of +1.26 %, which is why the book's Sharpe of 0.43 trails holding by 0.21.
- **F3:** The 10-day excess return after a vol-scaled 1-day move is not graded across quintiles of that move. The quintile of the largest falls gives +1.59 % (t 1.38) and the quintile of the largest rises gives +0.12 % (t 0.09), with the middle quintiles at -0.99 % and -1.98 %. The pooled slope t is -0.62 over 515 cells.
- **F4:** The sign of the reaction to a vol-scaled 1-day move flips with the horizon, which reads as noise rather than a structure:
- **F5:** None of the other context measures grades the next 10 days' excess return. Their pooled slope t's are:
- **F6:** Splitting by trend does not rescue the fall-rebound effect. Above the 50-day mean the slope t is 0.28 (215 cells); below it, -1.35 (204 cells).
- **F7:** The year drives most of the spread. Mean 10-day excess returns run from -4.13 % (2018) and -3.39 % (2022) to +3.60 % (2020), each over about 70 cells. This is far larger than any spread from the forecast or from the context measures.
- **F8:** The book's best and worst days are the coin's own moves:

## Ideas
- No ideas: Across about 35 angles (the move's size at 5, 10 and 20 days; trend, momentum, volatility, distance from highs, weekday, year; the book's positions, days and trades), no pattern grades the coin's next move clearly enough to stand out from chance. The book's gain is the coins' drift, net of negative timing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
