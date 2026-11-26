---
line: 7.b inconclusive
backtest: 062-01_choppy-calm-fall-continues_1d
idea tested: 062-01_choppy-calm-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2042 USD
---
## Findings
- **F1:** On folds B and C the tested measure points the idea's way but is too thin to clear the bar: 93 short cases at 5 days on 62 days, mean short excess +1.20 % with t 1.14. Every other horizon points the same way, also without clearing the bar: 1 day +0.30 % (t 1.33, 476 cases), 3 days +0.68 % (t 0.92), 10 days +2.30 % (t 0.62). Step 5's own result, +0.61 % with t 0.97 on 269 cases, matches this.
- **F2:** The effect is graded as the idea says. The two larger |forecast| quartiles give +2.41 % (t 1.09) and +2.72 % (t 1.22), against +0.46 % and -0.77 % for the two smaller ones. Across all in-profile grid bars, the most negative quintile of the swing-scaled 5-day return is followed by a raw 5-day excess of -2.73 % (t -1.39, 34 cases), against +2.38 % for the top quintile. So the ordering is monotone, but no single cell is sure.
- **F3:** The effect is mixed across coins and periods rather than concentrated in one place:
- **F4:** The cases are few because the choppy calm profile is rare. Only 1,031 of 8,331 coin-days (12 %) are in it on the six coins, and only 93 five-day cases fall in folds B and C. The limit is the number of cases, not the direction. More coins with daily data in the same folds (ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO) would add cases without narrowing the idea.

## Ideas
- `062-01.b1_choppy-calm-falls-all-coins` (from F1, F2, F4): In a choppy, calm market, a coin whose 5-day return is more negative, measured against its 30-day daily swing, falls further over the next 5 days. The larger the swing-scaled 5-day fall, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
