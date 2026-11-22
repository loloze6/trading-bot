---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4596 USD
---
## Findings
- **F1:** The tested idea's long side carries all of the book, and its short side gives nothing back. Long trades average +11.24 % net (t 10.75, 3077 trades) and short trades −1.60 % (t −8.29, 3838 trades). On the 5-day grid in the trending regime, the unusual move in the forecast's direction is +1.16 % after a 30-day rise (t 2.73, 1581 cases) against +0.25 % after a 30-day fall (t 0.88, 1539 cases).
- **F2:** Contrary to the brief, the coin's place in its 30-day high-low range predicts continuation, not a return to the middle. In the bars outside the trending regime, the 5-day unusual move rises with the close's position in the range: slope +0.0253 (t 2.88, n 3097), from −1.08 % in the lowest fifth (t −2.60) to +0.11 % in the highest. Over 10 days the slope is +0.0657 (t 3.66, n 1548).
- **F3:** The same continuation from the range position holds on all bars together. The slope is +0.0245 over 5 days (t 3.87, n 5434) and +0.0523 over 10 days (t 4.23, n 2680). It is still there inside the trending regime (slope +0.0209, t 2.21, n 2337), so a regime rule does not create it.
- **F4:** Outside the trending regime, a coin whose 30-day return is negative but whose close has climbed back above the middle of its range falls hardest. Its 5-day unusual move is −2.05 % (t −4.17, 399 cases). Below the middle after a fall it is −1.07 % (t −3.50, 1194 cases), and above the middle after a rise it is +0.93 % (t 2.48, 933 cases).
- **F5:** Across all bars, 30-day momentum pays at moderate net-move-to-range ratios, not only above the 0.5 rule. The 5-day unusual move in the 30-day direction is +1.02 %, +1.23 % and +1.13 % in the second to fourth fifths of the ratio (t 3.04, 3.73, 2.24, about 1087 cases each). It is +0.13 % in the flattest fifth (t 0.44) and +0.59 % in the highest (t 1.45).
- **F6:** The range-position continuation outside the trending regime fades over time. In the range position's direction it is +1.37 % to +2.67 % a year in 2018–2021 (t up to 3.88) and between −0.17 % and +0.30 % in 2022–2025 (all |t| < 0.6).
- **F7:** Saturday is the only weekday that stands out across the many weekdays examined. On the mean of the coins each day, Saturday returns +0.47 % (t 2.96, 414 days) for holding the coins and +0.21 % (t 2.93) for the book; no other weekday reaches t 2.1.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.g1_range-position-continues-ten-days` (from F2, F3, F6): The higher a coin's close sits inside its own 30-day high-low range, the higher its return over the next 10 days, and the lower it sits, the further it falls.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.g2_failed-rebound-after-monthly-fall` (from F4, F2): In a coin whose 30-day return is a fall, the higher its close has climbed back inside its 30-day high-low range, the further it falls over the next 5 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.g3_rising-trends-continue-long-side` (from F1, F5): In a coin whose 30-day net move is large relative to its 30-day high-low range, the larger its 30-day rise, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
