---
line: 7.b inconclusive
backtest: 046-01_calm-scaled-rise-second-day-continues_1d
idea tested: 046-01_calm-scaled-rise-second-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 3.4951 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: the day-clustered slope t is 1.88 against a confirm bar of 2, and the forecast-weighted mean excess second-day return is +0.13 % (passed), over 4720 bars on 1642 days. In the visible folds B and C alone, the same slope has t 1.48 (2354 cases, 768 days), with a mean excess second-day return of +0.16 %.
- **F2:** The effect is broad and weak rather than located anywhere. The slope is positive in all four visible years (t 0.11 to 1.24), in 9 of 12 windows and in 4 of 6 coins (largest ETH, t 1.83). No year, window or coin reaches t 2, so no subset holds it on its own.
- **F3:** The follow-through comes on the second day, not the first, as the brief says. The first-day slope has t 0.36, the second-day slope t 1.48, and days 2 to 4 together t 1.86. No other horizon shows the effect clearly more strongly than the plan's.
- **F4:** The second-day excess return is carried by the largest rises.
- **F5:** No market profile holds the effect.
- **F6:** The idea's size is far below a trade's cost. The unusual move per case is -0.03 % (t -0.24, 1281 days), and the total move is +0.10 % against a cost of 0.19 % per trade. Even if confirmed on more data, this one-day second-day move would not pay as a book on its own.

## Ideas
- `046-01.b1_calm-rise-second-day-all-coins` (from F1, F2, F3, F4): In a calm market, the larger a one-day rise is against the coin's 30-day daily swing (the standard deviation of its daily returns), the larger the coin's rise on the second day after it, from the close one day after the rise to the close two days after.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
