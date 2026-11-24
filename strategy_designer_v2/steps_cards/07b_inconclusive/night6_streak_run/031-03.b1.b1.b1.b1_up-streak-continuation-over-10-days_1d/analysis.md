---
line: 7.b inconclusive
backtest: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d
idea tested: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4330 USD
---
## Findings
- **F1:** On the plan's own 1920 cases (725 days), the unusual move reaches the bar at shorter horizons and fades at longer ones: +0.62 % with t 2.14 over 3 days, +0.87 % with t 2.14 over 5 days, +1.26 % with t 1.88 over 10 days, +1.94 % with t 1.74 over 20 days (1746 cases, 666 days), and the strength falls from 0.072 to 0.064, so the 10-day test sits just past where the effect shows clearly.
- **F2:** The streak's grading shows at 5 days and nowhere else. On the plan's cases the unusual move rises from the bottom to the top forecast third over 5 days (+0.50 %, +0.82 %, +1.30 %; top third t 1.98, 342 days). It is flat over 3 days (+0.70 %, +0.56 %, +0.61 %) and over 10 days (+1.24 %, +1.25 %, +1.29 %), and reversed over 20 days (+2.78 % against +0.69 %). The 10-day supporting check passed by only +0.05 %.
- **F3:** Most of the effect comes from the size of the 30-day return rather than from the streak. On the plan's cases, the top 30-day-return third earns +1.93 % over 3 days (t 3.22, 230 days), +2.07 % over 5 days (t 2.53) and +2.43 % over 10 days (t 1.97). The bottom third earns −0.19 %, −0.01 % and +0.93 %. Over 5 days the top-minus-bottom difference is +1.58 % (Welch t 2.69, on a 5-day case grid).
- **F4:** On 5-day grid bars with a positive 30-day return, signal and no-signal bars move alike within each 30-day-return third: top third +1.38 % with a streak against +1.31 % without (354 to 428 cases each). The no-signal bars alone rise with the 30-day return: −1.21 %, +0.08 %, +1.31 % across the thirds.
- **F5:** The effect is mixed across years and coins, which keeps its t under 2. The 10-day unusual move is −6.1 % in 2018, −2.95 % in 2022 and −0.36 % in 2025, against +3.7 % to +4.7 % in 2020–2021 and +1.9 % to +2.9 % in 2023–2024. Only 47 % of cases are positive (median −0.93 %), and BTC, LTC, XMR, TRX, UNI and NEAR are each near 0 (|t| < 0.5).

## Ideas
- `031-03.b1.b1.b1.b1.b1_up-streak-continuation-over-5-days` (from F1, F2): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it keeps rising over the next 5 days, only while its 30-day return is positive.
- `031-03.b1.b1.b1.b1.b2_30-day-return-continuation` (from F3, F4, F5): The larger a coin's 30-day return, the more it keeps rising over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
