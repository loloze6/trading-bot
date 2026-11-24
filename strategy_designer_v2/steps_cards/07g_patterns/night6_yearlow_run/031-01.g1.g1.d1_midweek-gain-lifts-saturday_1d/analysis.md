---
line: 7.g patterns
backtest: 031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d
idea tested: 031-01.g1.g1.d1_midweek-gain-lifts-saturday
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4172 USD
---
## Findings
- **F1:** Across all weekdays, not only before Saturday, a coin's return over the 5 days ending the day before predicts the next day's excess return in units of its 20-day volatility. The slope is 0.055 with t 2.73 over 2538 days, and the latest day's own move has a slope of −0.018 (t −0.88). The same skip-the-last-day lookback holds at 2, 3, 7, 10 and 14 days, with slopes 0.034–0.045 and t between 1.85 and 2.32.
- **F2:** The grading sits on the rising side. Above a zero 3-day (skip-one) return, the slope is 0.066 (t 2.28, 1981 days); below zero it is 0.017 (t 0.35, 1946 days). Only the top quintile of that return is followed by a positive next-day excess: +0.24 %, t 1.70, 1179 days, against −0.08 % to −0.11 % for quintiles 1–3.
- **F3:** The continuation is not confined to the Friday-before-Saturday bar. On the pooled 4-day lookback, the slope is also positive for the Monday target (0.138, t 2.27) and the Tuesday target (0.105, t 1.55). By signal weekday, the skip-3-day slope is positive on 5 of 7 days, with t 2.05 on Friday and t 2.20 on Sunday.
- **F4:** The effect is uneven across coins and years, so it is fragile. The skip-3-day slope has t 2.23 for BTC, 2.36 for ETH, 2.35 for XRP, 1.73 for ZEC, 1.11 for XMR and 0.11 for LTC. Six of eight years are positive, but 2022 (t 0.06), 2023 (t −0.09) and 2025 (t −1.06) carry nothing.
- **F5:** The book's whole gain comes from Saturday, with a mean book return of +0.24 % on Saturdays and 0 on every other day except Friday (−0.03 %). The 2 % largest book days (41 gains, 17 losses) carry 95 % of the book's total return. 2023 was the only losing year: a Sharpe of −0.78 and a mean trade of −0.42 %.
- **F6:** Nothing else I checked stood out. The prior day's own move does not grade the next day: no quintile reaches |t| 1.6. Volatility tercile does not either: the high tercile gives +0.16 % at t 1.11. The position in the 60-day range does not grade the 5-day excess return (slope t 1.13, 414 days), which is the brief's near-the-low angle shortened.

## Ideas
- `031-01.g1.g1.d1.g1_lagged-weekly-gain-continues-daily` (from F1, F2, F3, F4): The higher a coin's return over the 5 days ending the day before, the more it rises over the next day, on the rising side of that return only. The larger the gain, the larger the next day's rise, whatever the weekday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
