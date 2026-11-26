---
line: 7.b inconclusive
backtest: 040-01_rising-swing-scaled-weeks-rise-continues_1d
idea tested: 040-01_rising-swing-scaled-weeks-rise-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3942 USD
---
## Findings
- **F1:** In folds B and C, on the plan's own measure (in profile, forecast > 0, 14-day grid), the slope of the 14-day excess return on the forecast is -0.0021 (t -0.61, 285 cases), and the mean excess return is +0.18 % (t 0.09). The +2.05 % size and the slope's t of 1.13 in the verdict therefore rest on folds A and D, not on these windows.
- **F2:** On the raw swing-scaled 20-day rise, without the 60-day standardisation, the slope in the rising profile is negative at every horizon: -0.029 at 7 days (t -2.41, 440 cases), -0.060 at 14 days (t -2.50, 193 cases), -0.112 at 21 days (t -1.38) and -0.125 at 28 days (t -2.07). Outside the profile it is +0.018 (t 0.27, 108 cases), so the giving-back sits in the rising market.
- **F3:** The effect bends rather than grades. At 14 days, the four lower quintiles of the raw swing-scaled rise (mean 0.19 to 1.65 swings) have excess returns of +5.7 %, +6.6 %, +2.4 % and +2.6 %, while the top quintile (mean 2.73 swings) has -11.2 %. At 7 days the pattern is the same: the lower quintiles show +2.5 % to +5.3 % and the top quintile -5.2 %.
- **F4:** Rises of up to 2 swings are followed by a positive excess move (+3.9 % at 7 days, t 2.27 by day, 348 cases; +4.3 % at 14 days, t 1.18). Inside that range the slope is not reliably positive (+0.025 at 7 days, t 1.17; -0.039 at 14 days, t -0.68). Rises above 2 swings are followed by -5.2 % at 7 days and -10.8 % at 14 days.
- **F5:** The negative 14-day slope on the raw swing-scaled rise holds in every year with enough cases: 2019 -0.055 (t -1.56), 2020 -0.092 (t -2.66), 2021 -0.041 (t -1.48). It also holds in calm markets (-0.048, t -1.82) and in agitated ones (-0.078, t -1.57). It is not one period or one regime.
- **F6:** The result is unclear for two reasons. The tested forecast, standardised over 60 values and clipped at 0, puts its largest values (the top bucket, 114 cases, forecast 18.5) on the stretched rises that give back (-2.0 % excess), while its middle bucket gains +4.6 %. A positive mean move and a negative grading at the top therefore cancel in the slope, and the test already used every fold and coin available.

## Ideas
- `040-01.b1_rising-stretched-rise-gives-back` (from F2, F3, F5, F6): In a rising market, the more of its 20-day daily swings a coin's 20-day rise spans, the lower the coin's return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
