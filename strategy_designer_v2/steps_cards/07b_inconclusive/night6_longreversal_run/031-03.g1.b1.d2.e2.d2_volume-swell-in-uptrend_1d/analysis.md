---
line: 7.b inconclusive
backtest: 031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend_1d
idea tested: 031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4514 USD
---
## Findings
- **F1:** The test's forecast cannot show a grade. It is 0 on at least a quarter of the trending grid cases, its median is only 1.71, and 10.5 % of cases sit at the cap of 20. The 14-day excess return is −0.50 % at a forecast of 0 (519 cases) and +3.61 % at a forecast above 2 (574 cases), but among forecasts above 0 the slope's t is only 0.52 (647 cases). So the main measure's t of 1.65 is a step between "no swell" and "swell", diluted by a saturated scale.
- **F2:** Inside the uptrend, the raw volume ratio (14-day mean volume over 30-day mean, minus 1) does grade the 14-day excess return. By quintile it rises from −1.57 % to −1.02 %, +4.29 %, +3.96 % and +6.68 % (about 149 cases each; slope t 1.90, 746 cases). Most of that grade is the step from shrinking to swelling volume: among ratios above 0 alone the slope's t is 0.32 (427 cases).
- **F3:** The volume-ratio effect is clearer without the 50-day condition than with it. Its slope's t is 2.95 over all grid cases (1,530), against 1.90 inside the uptrend (746 cases). Below the 50-day mean the slope's t is 2.38 (784 cases). There the lowest-ratio quintile is followed by −6.13 % (t −2.85, 197 cases) and the highest by +1.36 % (t 0.48, 119 cases). So the regime condition halves the cases and leaves out the strongest side, falling prices on shrinking volume.
- **F4:** The plan's horizon is the right one. The forecast's slope has t 0.82 over 7 days (2,462 cases), 1.65 over 14 days (1,166 cases) and 1.18 over 28 days (567 cases). With forecast above 0, the mean excess return over 7 days is +1.96 % (t 2.01).
- **F5:** The effect is uneven across years, which is what keeps the t under 2. The slope's t is −2.05 in 2018 (37 cases), −0.81 in 2021 (166), +1.73 in 2023 (212) and +2.81 in 2024 (248).
- **F6:** The effect is not limited to strong uptrends. Inside the uptrend, the ratio's slope has t 2.10 in the lowest third of distance above the 50-day mean and 1.13 in the highest third (208 cases each). In the default six coins its t is 1.92 (359 cases), and in the other thirteen 1.45 (387 cases).
- **F7:** The effect is large against the cost of a trade, so the issue is noise, not size. The unusual move is +2.94 % per case (t 2.63, 593 days), 0.117 of a usual 14-day move, which is 13.2 times the 0.22 % cost of a trade. The tested book already passes step 6, with a Sharpe of 1.07.

## Ideas
- `031-03.g1.b1.d2.e2.d2.b1_volume-swell-predicts-two-weeks` (from F2, F3, F4, F7): The higher a coin's mean daily volume over the last 14 days stands against its mean daily volume over the last 30 days, the higher its return over the next 14 days.
- `031-03.g1.b1.d2.e2.d2.b2_fading-volume-in-downtrend` (from F3, F4): The more a coin's mean daily volume over the last 14 days sits below its mean daily volume over the last 30 days, the more its price falls over the next 14 days, only while its close sits below its mean close of the last 50 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
