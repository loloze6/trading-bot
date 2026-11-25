---
line: 7.g patterns
backtest: 032-02.b2_volatile-low-next-day-rebound_1d
idea tested: 032-02.b2_volatile-low-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5292 USD
---
## Findings
- **F1:** Over all 8330 coin-days of folds B and C, where the close sits inside the day's high-low range predicts the next day's excess return with the opposite sign (Spearman −0.095, p 2.5e-18). Closes in the lowest fifth of the range are followed by +0.53 % (t 2.15, 1659 cases, 614 days) and closes in the highest fifth by −0.37 % (t −1.84, 1663 cases).
- **F2:** The F1 relation is negative in every one of the six coins and in every year. By coin, rho runs from −0.074 for ZEC to −0.146 for XMR, all with p ≤ 0.005. By year, 2018 is −0.10, 2019 −0.13, 2020 −0.16 and 2021 −0.04 (p 0.09).
- **F3:** The F1 rebound after a close near the day's low appears only when ranges are wide, and the 1-day spread from lowest-fifth to highest-fifth close is about 0.9 % to 1.6 %, five to eight times the 0.19 % cost of a trade.
- **F4:** Among the 320 closes above the prior 30-day high, the further above the high the close sits, the lower the next day's excess return (Spearman −0.205, p 0.0002).
- **F5:** After a down day of 1.5 or more of its 20-day standard deviation, the next-day rebound appears only when the month's ranges are wide against the past 90 days.
- **F6:** The tested situation itself is rare, and in these folds its slices do not stand out from chance.

## Ideas
- `032-02.b2.g1_close-location-next-day-reversal` (from F1, F2): The lower a coin's daily close sits within that day's high-low range, the more the coin rises over the next 1 day, and the higher the close sits in the range, the more it falls.
- `032-02.b2.g2_volatile-close-near-low-rebound` (from F3, F1): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days, the lower its close sits within the day's high-low range, the larger its rise over the next 1 day.
- `032-02.b2.g3_stretched-breakout-next-day-fade` (from F4): When a coin closes above its highest high of the prior 30 days, the further the close sits above that high, the more the coin falls over the next 1 day.
- `032-02.b2.g4_volatile-big-drop-next-day-rebound` (from F5, F6): When a coin's daily ranges over the past 30 days are wide compared with the past 90 days, the larger its 1-day fall measured against its 20-day volatility, the larger its rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
