---
line: 7.b inconclusive
backtest: 031-03.g1.b1.d2_rising-volume-rally-continues_1d
idea tested: 031-03.g1.b1.d2_rising-volume-rally-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3923 USD
---
## Findings
- **F1:** The test's result leans the way the idea predicts but falls short of the bar: the forecast-weighted 14-day excess return is +4.0 % with a day-clustered t of 1.71, over 655 cases on 141 distinct days, and the test already used every coin and every fold available.
- **F2:** The 14-day horizon is where the effect is clearest; neighbouring horizons are not clearer (7 days: +1.4 %, t 1.09; 28 days: +8.0 %, t 1.63, 127 days).
- **F3:** The effect changes sign from year to year, so it is not steady over time: 2018 −17.6 % (t −4.53, 10 days), 2019 −2.1 %, 2020 +5.4 %, 2021 +10.6 %, 2022 −5.0 % (t −1.73), 2023 +5.0 %, 2024 +6.9 %, 2025 −0.6 %, with no year reaching t 2 on the positive side.
- **F4:** The effect is mostly market-wide, not specific to each coin: on days when 6 or more coins swell together it is +7.0 % (t 2.20, 407 cases, 44 days), but when only 1–2 coins swell it is −5.0 % (t −1.31, 51 days) and with 3–5 coins −0.9 % (t −0.31), so a single coin's own swell predicts nothing beyond what the whole market does.
- **F5:** The grading the idea requires is weak and does not rise steadily: by forecast quartile the excess is +1.3 %, +1.6 %, +6.3 % and +3.8 % (Spearman 0.078), and by volume-ratio quartile +1.8 %, +1.7 %, +5.3 % and +4.3 %, so the strongest swells are not the ones followed by the largest moves.
- **F6:** No single coin or price setting shows the effect clearly on its own: no coin reaches t 2 (the highest is NEAR at 1.59, while AAVE, LINK, LTC and XMR are slightly negative); the past 30-day-return quartiles (+2.1 %, +12.5 % with t 3.10, +1.0 %, +6.4 %) and distance-to-high quartiles (+0.6 %, +2.7 %, +8.6 % with t 2.53, +4.3 %) peak in a middle band without a graded pattern; and the 60-day-return split (up +6.0 %, t 1.36; down −3.1 %, t −0.83) is not clear either.

## Ideas
- No ideas: The result is on the predicted side, but no more data exists beyond the 19 coins and four folds already used, and the findings show no part of one coin's own data where the effect is clear and graded (it comes from market-wide swells, F4, and swings by year, F3), so no amended idea is supported.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
