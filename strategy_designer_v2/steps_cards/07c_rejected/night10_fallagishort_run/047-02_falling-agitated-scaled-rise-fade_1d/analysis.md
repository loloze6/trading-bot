---
line: 7.c no effect
backtest: 047-02_falling-agitated-scaled-rise-fade_1d
idea tested: 047-02_falling-agitated-scaled-rise-fade
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5977 USD
---
## Findings
- **F1:** In the falling agitated profile, the size of an up day does not grade what follows on any horizon. On up days the slope of the next move's unusual part on the scaled rise is +0.0003 at 1 day (t 0.05, 177 cases), +0.0014 at 2 days (t 0.12, 100 cases) and -0.015 at 5 days (t -0.25, 25 cases). Step 5's own measure agrees: -0.07 % per short case, t -0.14 over 316 days.
- **F2:** The one graded reading, at 3 days, is an artefact of one grid. Starting on the plan's grid (offset 0), the slope is -0.052 (t -3.30, 60 cases). On the same 3-day horizon from offsets 1 and 2, the slope turns positive: +0.018 (t 1.10, 50 cases) and +0.017 (t 0.67, 66 cases).
- **F3:** Pooled over all three offsets, the 3-day grading on up days holds in no coin and in one year only. By coin the slopes are BCH -0.025 (t -1.02), LTC +0.002 (t 0.12) and XMR -0.010 (t -0.38). By year, only 2020 is negative (-0.039, t -2.76, 76 cases). 2018 (+0.022, t 0.83) and 2021 (+0.015, t 0.44) point the other way.
- **F4:** The supporting check passed on very few independent days. The largest scaled rises (forecast at or below -10) fell 4.08 % more than usual over 3 days, but on only 13 cases over 6 days (day-clustered t 1.07). The rises with a scaled size above 1 fell 5.36 %, on only 10 cases over 4 days (t 1.21).
- **F5:** What the market did after up days in this profile was an ungraded drift down, strongest after the smallest rises:
- **F6:** In this profile the graded reversal lives on the long side, which is outside this research's box.
- **F7:** Outside the profile, up days carry no reversal either. The slope is -0.0003 at 1 day (t -0.18, 1,463 cases) and +0.0035 at 3 days (t 0.71, 498 cases). The forecast and the scaled rise were near-identical (correlation -0.92 to -0.99), so the forecast measured the brief's situation faithfully.
- **F8:** Even a real fade would be small against the cost of a trade. Per case, the total move was -0.26 % against a cost of 0.35 % per trade, and the coins' normal drift ran 0.19 % against the short side. The book lost accordingly: Sharpe -0.12 and -1.9 % a year.

## Ideas
- No ideas: The theme's effect is not in the data on the short side. In falling agitated markets, the fall after an up day does not grow with the size of the rise (F1, F5). Its one graded reading depends on the grid's starting day, the coin and one year (F2, F3, F4). The brief's graded reversal appears only after down days, as a long rebound (F6), which is outside this research's short-only box.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
