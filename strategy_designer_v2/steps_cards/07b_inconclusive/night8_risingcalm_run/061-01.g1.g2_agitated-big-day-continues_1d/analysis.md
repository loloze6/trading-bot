---
line: 7.b inconclusive
backtest: 061-01.g1.g2_agitated-big-day-continues_1d
idea tested: 061-01.g1.g2_agitated-big-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3452 USD
---
## Findings
- **F1:** The tested situation shows no continuation at the plan's 5-day horizon. On the plan's grid in folds B and C, agitated cases give a 5-day slope of +0.0001 (day-clustered t 0.01, 591 cases), against -0.0006 (t -1.49) on all folds.
- **F2:** In the same agitated days the move reverses over the next day, and the reversal grows with the day's size. The 1-day slope is -0.0058 (day-clustered t -2.29, 2,946 cases). The return in the day's direction is -0.6 %, -0.3 %, -0.4 % and -0.5 % for days of 0 to 2 swings, then -2.0 % for 2 to 3 swings (101 cases) and -3.4 % above 3 swings (27 cases).
- **F3:** The agitated 1-day reversal is broad. The slope is negative on all 6 coins (t from -0.20 on XRP to -3.02 on XMR, four of them at or beyond -1.97) and on 10 of the 11 windows with enough cases (only w12 is +0.0006, t 0.07).
- **F4:** The reversal is strongest after down days. After an agitated down day the slope is -0.0128 (t -2.03, 1,439 cases), against +0.0049 (t 1.50, 1,505 cases) after up days.
- **F5:** The reversal fades with the horizon and turns to a small continuation by 7 days. The agitated slope is -0.0059 at 2 days (t -1.48), -0.0075 at 3 days (t -1.11), +0.0001 at 5 days and +0.0152 at 7 days (t 1.39).
- **F6:** The continuation the brief describes shows where the brief places it, in calm markets at 5 days.

## Ideas
- `061-01.g1.g2.b1_agitated-big-day-reverts` (from F1, F2, F3, F4, F5): In an agitated market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further it moves back against that day's direction over the next day.
- `061-01.g1.g2.b2_calm-big-day-continues` (from F1, F6): In a calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving in that day's direction over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
