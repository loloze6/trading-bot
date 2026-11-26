---
line: 7.b inconclusive
backtest: 032-02_monthly-low-exhaustion-rebound_1d
idea tested: 032-02_monthly-low-exhaustion-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1928 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls just short of the bar: the mean unusual 3-day move is +2.20 % with t 1.97 over 163 cases on 86 days. In folds B and C the same measure gives +3.83 %, t 1.96, over 70 cases on 28 days, with the same sign at every horizon (1 day +3.51 % t 1.84, 5 days +4.13 % t 1.76, 10 days +7.68 % t 2.42).
- **F2:** The evidence is limited by how few distinct days the cases fall on, not by the size of the move. The 163 cases fall on only 86 days, and in folds B and C 70 cases fall on 28 days, because coins hit monthly lows together. The move per case is large: a strength of 0.269 of the usual move in the verdict and 0.41 in folds B and C, a median of +3.05 %, and 11.4 times the 0.19 % cost of a trade.
- **F3:** The effect is mixed across periods. In 2018 (w14), 32 cases on 11 days lose -2.22 % (t -1.29). In 2019, 2020 and 2021 the cases gain +6.55 % (t 1.87, 6 days), +12.14 % (t 8.24, 3 days) and +9.24 % (t 2.13, 8 days). Only 54 % of cases are positive.
- **F4:** The rebound is spread across coins rather than carried by one: the 3-day unusual move is positive in 5 of 6 coins (LTC +9.65 % t 2.36, ZEC +5.25 % t 1.91, BTC +2.49 % t 1.08, XMR +1.14 %, XRP +9.47 % on 3 cases). ETH is the exception, flat at -0.31 %.
- **F5:** The move is graded as the idea says. The 3-day unusual move rises across forecast terciles from +3.08 % to +3.77 % to +4.62 %, and in the verdict the deeper half beats the shallower half by +3.88 %.

## Ideas
- `032-02.b1_monthly-low-rebound-more-coins` (from F1, F2, F4, F5): In a falling, agitated market, when a coin closes below the lowest close of its previous 30 days, it rebounds over the next 3 days, and the further the close sits below that prior 30-day low, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
