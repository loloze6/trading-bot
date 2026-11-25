---
line: 7.g patterns
backtest: 038-01_calm-scaled-weekly-rise-continues_1d
idea tested: 038-01_calm-scaled-weekly-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4008 USD
---
## Findings
- **F1:** In calm bars (folds B, C), the coin's unusual 5-day move rises with its scaled 7-day move on both sides together: slope t 5.29 over 773 non-overlapping cases. In agitated bars the slope t is -0.33 over 591 cases, and the calm-minus-agitated difference in slope has t 3.24 over 1,364 cases.
- **F2:** The falling side carries as much of the calm continuation as the rising side the tested idea kept. For calm cases with a 7-day fall, the slope t is 3.48 (375 cases), against 2.63 for rises (398 cases). The bottom fifth of the scaled 7-day move is followed by an unusual 5-day move of -2.79 % (t -3.51, 148 cases), the top fifth by +2.51 % (t 2.63, 171 cases).
- **F3:** A shorter 3-day lookback grades the calm continuation most sharply. The two-sided slope t is 5.97 (773 cases), and the slope for 3-day falls alone is 4.91 (370 cases). In agitated bars the same slope t is 0.15.
- **F4:** The calm 3-day-fall slope is positive in every year: t 3.06 in 2018, 2.18 in 2019, 0.83 in 2020 and 0.23 in 2021. The 7-day-fall slope flips sign in 2019 (t -1.17) and 2021 (t -0.59). The 7-day-fall slope is positive on all 6 coins (t from 0.55 to 2.37).
- **F5:** The size of the calm fall continuation is not yet sure, measured short with the cases of one day together.
- **F6:** Longer scaled moves also continue in calm bars and not in agitated ones:
- **F7:** The long-only book's trades are carried by a few large winners: mean +3.25 % net against a median of -0.26 % over 1,399 trades. The top quarter of entry forecasts has the worst median, -1.19 %, so the long side's grading does not show in the trades.

## Ideas
- `038-01.g1_calm-scaled-fall-continues` (from F2, F3, F4, F5): In a calm market, the larger a coin's 3-day fall measured against its 30-day daily swing, the larger its further fall over the next 5 days.
- `038-01.g2_calm-short-burst-follows-through` (from F1, F3, F4): In a calm market, a coin's 3-day move measured against its 30-day daily swing carries on in its own direction over the next 5 days, and the larger the scaled move, the larger the follow-through, up or down.
- `038-01.g3_calm-monthly-scaled-trend-continues` (from F6, F1): In a calm market, the larger a coin's 30-day return measured against its 30-day daily swing, the larger its further move in the same direction over the next 5 days, for rises and falls alike.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
