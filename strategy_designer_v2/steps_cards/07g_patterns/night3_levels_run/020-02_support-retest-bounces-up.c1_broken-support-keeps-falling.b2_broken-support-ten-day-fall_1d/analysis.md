---
line: 7.g patterns
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3515 USD
---
## Findings
- **F1:** The book's result is mostly the market's direction, not timing. It gained in the two falling years, 2018 (+0.229 % a day while the coins fell -0.347 %) and 2022 (+0.173 % against -0.180 %). It lost in every year the coins rose: 2020 (-0.323 % against +0.423 %), 2021 (-0.181 % against +0.409 %), 2023, 2024 and 2025.
- **F2:** The forecast's own grading adds little. Over 10 days, the drift-adjusted return of the negative-forecast cases is -1.30 %, -1.06 %, -0.47 %, -1.17 % and +0.80 % from the most to the least negative quintile (about 233 cases each). That is roughly flat over the four strongest quintiles, against a usual 10-day move of about 14.5 %.
- **F3:** Closes with no past turning-up low above them (forecast zero, so the close sits above every 90-day swing low) were followed by +1.41 % over 10 days beyond drift (527 cases), against -0.64 % for the negative-forecast closes (1164 cases). All 6 coins point the same way, but no coin reaches t 2 (t 0.27 to 1.62), and the years split: t +2.96 in 2019, -3.03 in 2023.
- **F4:** Short-term momentum on the daily bars is weak and unstable.
- **F5:** No other angle stands out once the number of looks (about 30) is counted:

## Ideas
- No ideas: Every pattern beyond the market's own direction is either within chance after about 30 looks or changes sign from year to year (best: 10-day momentum at t 2.54, split 4 to 4 across years), so no finding is firm enough to rest a new idea on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
