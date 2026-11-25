---
line: 7.b inconclusive
backtest: 032-03_deep-fall-low-exhaustion-rebound_1d
idea tested: 032-03_deep-fall-low-exhaustion-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3719 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but is far from the bar: the mean unusual 5-day move is +0.59 % (t 0.56, 155 case days, 236 cases), and in folds B and C alone it is +1.10 % (t 0.59, 76 days, 129 cases); at the same spread, t 2 would need about 13 times as many case days.
- **F2:** The rebound in the cases is strongest before the plan's horizon and fades by it: the unusual move is +1.95 % at 1 day (t 1.52), +2.70 % at 3 days (t 2.09), +1.10 % at 5 days (t 0.59) and +1.21 % at 10 days (t 0.49), on the same 129 cases and 76 days.
- **F3:** Inside the cases, the depth of the raw 30-day fall sorts the outcome the way the idea's grading says, with a Spearman of ret30 against the 5-day unusual move of −0.25. The deepest third rose +4.93 % over 5 days (t 1.14, 19 days) and +10.3 % over 10 days (t 1.60). The shallowest third fell −4.63 % (t −1.75) and −9.86 % (t −3.04, 18 days).
- **F4:** Across every new 30-day close low, not only the strategy's cases, lows reached after the smallest 30-day falls keep falling over 10 days. In the wide-range regime the shallowest third moved −10.6 % (t −2.64, 16 days); outside it, −7.6 % (t −2.13, 27 days). At 5 days the figures were −4.7 % (t −1.83) and −3.0 % (t −1.89). The deepest third in the regime stayed near zero, at −0.45 % over 5 days and +0.27 % over 10 days.
- **F5:** The rebound is mixed across coins and years. Per case over 5 days, BTC moved +2.4 %, XMR +5.3 % and ZEC +4.3 %, against ETH −0.9 %, LTC −0.6 % and XRP −3.3 %. By year, only 2021 is clearly positive (+4.4 %, t 2.15); 2018 was −1.4 % and 2020 −1.6 %.
- **F6:** The strategy's own forecast grades the move only weakly: the lowest forecast third moved −2.4 %, the middle +2.6 % and the highest +3.0 %. The supporting Spearman is 0.066, against the raw 30-day fall's −0.25 in F3, which suggests the 60-day standardisation blurs the grading.

## Ideas
- `032-03.b1_deep-low-rebound-all-coins` (from F1, F5): In a coin whose daily high-low ranges over the past 30 days are wide compared with its own past year, a close at a new 30-day low is followed by a rise over the next 5 days. The larger the coin's 30-day fall into that low, the larger the rise.
- `032-03.b2_deep-low-three-day-rebound` (from F2, F3): In a coin whose daily high-low ranges over the past 30 days are wide compared with its own past year, a close at a new 30-day low is followed by a rise over the next 3 days. The larger the coin's 30-day fall into that low, the larger the rise.
- `032-03.b3_shallow-fall-low-breakdown` (from F3, F4): In a coin whose daily high-low ranges over the past 30 days are wide compared with its own past year, a close at a new 30-day low is followed by a further fall over the next 10 days. The smaller the coin's 30-day fall into that low, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
