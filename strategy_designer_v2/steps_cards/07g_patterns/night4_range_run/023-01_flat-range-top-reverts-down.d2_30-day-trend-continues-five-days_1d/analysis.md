---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3955 USD
---
## Findings
- **F1:** Among flat coins (30-day net move under half the 30-day high-low range), those closing in the bottom fifth of the range (position ≤ -0.3) moved further down over the next 5 days rather than reverting. The mean was -0.22 of a usual 5-day move (t -3.14, 155 non-overlapping cases), and the bottom flat quintile of the 30-day return was also negative (-0.115, t -2.71, 399 cases).
- **F2:** In flat coins, range position correlated positively with the next 5-day unusual move (r 0.058, t 2.20, 1442 cases), and so did the 30-day return (r 0.047, t 1.78). This is the opposite sign to the brief's reversion. Only the bottom of the range carries it: the top fifth averaged -0.058, t -0.71, 134 cases.
- **F3:** A large 1-day rise was followed by further rise over the next 5 days, and large falls were not followed by further falls.
- **F4:** In the trending regime, only the top quintile of the 30-day return continued: +0.137 of a usual move (t 2.47, 433 cases). The bottom quintile gave +0.018 (t 0.33, 401 cases), so the tested idea's edge is all on the rising side.
- **F5:** The book's short trades lost and its long trades carried the profit.
- **F6:** The book lost in the early windows w3–w9 (daily means -0.0022 to -0.0003) and gained in most later windows (w14–w24 up to +0.0033 a day). By year it fell in 2022 (-0.00014) and 2023 (-0.00072 against holding's +0.0015), which fits the Calmar failure (0.29).
- **F7:** Saturday's coin-bar excess return was +0.34 % (t 4.08, 2484 coin-bars). The six coins move together on the same day, so the t is overstated. Saturday is a calendar condition with no grade, so no idea is built on it.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.g1_flat-range-bottom-keeps-falling` (from F1, F2): In a coin whose 30-day net move has been small relative to its 30-day high-low range, the closer its close sits to the bottom of that range, the further it falls over the next 5 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.g2_large-up-day-continues` (from F3): The larger a coin's 1-day rise relative to its usual daily move over the past 20 days, the further it rises over the next 5 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.g3_up-trend-continues-down-trend-doesn-t` (from F4, F5): In a coin whose 30-day net move has been large relative to its 30-day high-low range and whose 30-day return is positive, the larger that 30-day rise, the further the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
