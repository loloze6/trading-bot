---
line: 7.b inconclusive
backtest: 032-03.b1.b2_violent-decline-rebounds_1d
idea tested: 032-03.b1.b2_violent-decline-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3688 USD
---
## Findings
- **F1:** The test's result is on the predicted side but small and mixed: the pooled slope of 5-day excess return on the forecast is positive (0.00043, t 0.73, 1013 cases), but the mean in-regime 5-day excess return is negative (−0.67 %; size −0.89 %, t −1.42 over 441 days). On folds B and C the 5-day slope is +0.0020 (t 1.49, 375 cases) with a mean excess of −1.47 %, and the forecast quintiles do not rise monotonically (−3.5 %, −1.1 %, −0.9 %, −1.4 %, −0.5 %).
- **F2:** Inside the wide-range 28-day-fall regime, the past 7-day return grades the next move much more clearly than the 28-day fall does. The slope of excess return on the 7-day return is −0.049 at 1 day (t −4.63, 1875 cases, 568 days), −0.061 at 2 days (t −3.05), −0.068 at 3 days (t −2.39) and −0.130 at 5 days (t −2.77, 353 cases, 118 days). The deeper the last week's fall, the larger the rebound.
- **F3:** The 28-day-fall grading shows best at the shortest horizon and fades with length. Its slope t is 2.53 at 1 day (1961 cases), 1.56 at 3 days, 1.49 at 5 days, 0.56 at 10 days and −0.26 at 20 days. At 1 day the quintiles rise monotonically from −0.62 % to −0.46 %, −0.36 %, +0.08 % and +0.30 %, and the slope is positive in every year (t 0.46, 0.56, 1.91, 1.90 for 2018 to 2021).
- **F4:** The level effect works against the idea. In-regime bars keep falling relative to the coin's drift at every horizon (mean excess −0.21 % at 1 day, −1.15 % at 3 days, −1.47 % at 5 days, −3.25 % at 10 days). The drag is concentrated in DOGE (−13.7 % per 5 days, 14 cases) and ADA (−5.4 %, 33 cases), while BTC, XMR and ZEC sit near 0 (+0.3 %, +0.3 %, +0.2 %). This is why the supporting check fails even where the grading is positive.
- **F5:** The size cannot pay as tested. The total move is −0.07 % per case against a 0.22 % trade cost. At 5 days, however, the 7-day-return slope of F2 (−0.13) implies roughly +1.3 % more per extra 10 % of weekly fall, which exceeds the cost.

## Ideas
- `032-03.b1.b2.b1_violent-decline-weekly-drop-rebound` (from F2, F4, F5): Among coins that have fallen over the past 28 days with daily high-low ranges wider than the coin's own usual range over that period, the larger the fall over the past 7 days, the larger the rise over the next 5 days.
- `032-03.b1.b2.b2_violent-decline-next-day-rebound` (from F3, F1): Among coins that have fallen over the past 28 days with daily high-low ranges wider than the coin's own usual range over that period, the larger the 28-day fall, the larger the rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
