---
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
idea tested: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5969 USD
---
## Findings
- **F1:** The book's gain comes from its long side only. Bars held long earned a mean +0.085 % per bar (t 4.96, 8388 bars), and bars held short earned −0.008 % (t −0.67, 8796 bars). Long trades averaged +9.31 % net (1952 trades) and short trades −0.75 % (1598 trades). Short trades lost in 5 of 8 years.
- **F2:** The idea's slope is carried by its top fifth of forecasts. On 3419 non-overlapping 5-day cases, the top fifth ended +0.99 % above drift (t 2.04). The bottom fifth was only −0.16 % (t −0.41). The book shorts a side that does not fall.
- **F3:** On Fridays and Saturdays, a coin's next-day unusual return rises with its prior 7-day return in units of its 20-day volatility. The slope's t is 5.63 on 4554 days, against t 1.56 on the other 11386 days. The top fifth of prior weeks was followed by +0.94 % (t 5.38), the bottom fifth by +0.18 % (t 1.14).
- **F4:** The Friday/Saturday grading holds on 5 of 6 coins and in 5 of 8 years. By coin, t ranges 1.91 to 4.06, except XMR at −0.09. By year, t is 2.0 to 3.6 in 2020 to 2024, and about 0 in 2018, 2019 and 2025.
- **F5:** Saturdays rise more than other days, by +0.39 % per day (Welch t 4.26). Saturday's mean is positive in 66 % of 144 coin-windows and on all 6 coins (t 1.40 to 2.92).
- **F6:** A coin rebounds the day after a large down day. After the fifth of down days with the largest fall in units of 20-day volatility (mean −1.81), the next day's unusual return is +0.60 % (t 4.19, 1568 days). The next fifth gives +0.33 % (t 2.64), and the small falls give about 0. The slope across all down days is weaker: t 1.94 on 7837 days.
- **F7:** The rebound is uneven by coin and by year. By coin it is strongest on XMR, with a slope t of 3.53 and +0.88 % after big falls (t 4.09). By year it is clear in 2020 and 2021 (+1.45 % and +1.36 %, t about 4.1–4.2) and near 0 in 2019, 2022, 2024 and 2025.
- **F8:** Both one-day moves are large next to cost, but they cover one day, not 5. The +0.94 % weekend move and the +0.60 % rebound are 4.9 and 3.2 times the backtest's 0.19 % round trip. Across up to ~30 angles examined, F3 and F5 stand out most clearly; F6 is weaker.

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score.g1_weekend-continuation-after-strong-weeks` (from F3, F4, F5, F8): On a Friday or a Saturday, a coin's return over the next 1 day is higher the larger its 7-day return was, measured against its 20-day volatility.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score.g2_next-day-rebound-after-large-falls` (from F6, F7, F8): After a down day, a coin's return over the next 1 day is higher the larger that day's fall was, measured against its 20-day volatility.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score.g3_momentum-nearness-score-long-side` (from F1, F2): When a coin's 28-day return is positive and it sits near its 90-day closing high, its return over the next 5 days is higher the higher both are, measured against their usual levels.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
