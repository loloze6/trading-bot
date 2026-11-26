---
line: 7.b inconclusive
backtest: 031-03.g1_volume-surge-leads-two-week-drift_1d
idea tested: 031-03.g1_volume-surge-leads-two-week-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3229 USD
---
## Findings
- **F1:** At the plan's 14-day horizon the slope sits on the predicted side but is carried by the top fifth of forecasts alone. That fifth has a demeaned move of +2.13 % (231 cases, t 1.23). The other four fifths average −0.53 % (921 cases) and run −1.01 %, −0.18 %, −0.74 %, −0.20 % from the bottom up, so the move in the signal's direction is near zero: +0.53 % per case, day-grouped t 0.57 over 207 days, against the verdict's +0.03 % with t 0.04.
- **F2:** The effect changes sign across years. The 14-day slope t is −1.28 in 2019 and −1.06 in 2021, but +1.97 in 2023 and +2.80 in 2024. The top fifth's 14-day move ranges from −7.1 % in 2018 to +8.6 % in 2024 and +9.1 % in 2020.
- **F3:** No coin carries the effect and none is clear on its own: five of six coins have a positive 14-day slope (t 0.49 to 1.19, 192 cases each), while XMR's is −0.36. The pooled t of 1.53 is a small common lean that 192 cases per coin cannot show.
- **F4:** The lean is short-lived. The slope t is 2.55 over 7 days (2443 cases), 1.62 over 10 days (1691), 1.53 over 14 days (1152), −0.54 over 21 days (720) and −0.97 over 28 days (576).
- **F5:** Over 7 days the grading lives on the falling-volume side. Among negative forecasts the slope t is 2.12 (1300 cases), and the bottom fifth's demeaned move is −1.04 % (489 cases, t −1.90). Among positive forecasts the slope t is −0.04 (1143 cases), and the top fifth is only +0.18 % (t 0.25).

## Ideas
- `031-03.g1.b1_volume-surge-more-coins` (from F1, F3): The more a coin's mean daily volume over the last 14 days has risen above its mean daily volume over the last 30 days, the more its price rises over the next 14 days; the more that volume has fallen below its 30-day mean, the more its price falls over the next 14 days.
- `031-03.g1.b2_volume-drought-one-week-fall` (from F4, F5): The more a coin's mean daily volume over the last 14 days has fallen below its mean daily volume over the last 30 days, the more its price falls over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
