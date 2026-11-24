---
line: 7.g patterns
backtest: 031-03.b1.b1.e2_short-trend-strength-continuation_1d
idea tested: 031-03.b1.b1.e2_short-trend-strength-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4587 USD
---
## Findings
- **F1:** Across coins, a coin's 30-day return scaled by its 60-day daily volatility sorts its 5-day excess return far more than the tested 10-day rise does: the top two sextiles gain +1.28 % (t 2.14, 894 grid bars) and +1.18 % (t 2.67, 894) over the coin's normal drift, while the second and third sextiles lose -1.58 % (t -4.39) and -1.34 % (t -4.04); these t's are not clustered by day, so they overstate the evidence.
- **F2:** The same ordering shows in how far a coin sits below its 60-day high, scaled by its volatility: coins nearest their high gain +1.40 % over 5 days beyond drift (t 2.36, 995 bars), against -0.77 % (t -2.55) and -0.63 % (t -2.08) in the middle sextiles (t's not clustered by day).
- **F3:** The tested 10-day scaled rise grows steadily with the next 5 days' excess return only from its second sextile upward, from -1.31 % (t -3.85) to +0.68 % (t 1.57). Its lowest sextile, the largest 10-day falls, is followed by a +1.35 % rebound (t 4.11, 995 bars, not clustered by day); that break explains the step-5 slope t of 1.98 and the -0.01 % size.
- **F4:** Over one day, falls are followed by graded rebounds: after a fall of 1.5 to 2.5 daily volatilities the coin earns +0.50 % beyond drift the next day (t 3.26, 1318 bars), after 0.5 to 1.5 volatilities +0.23 % (t 2.54, 6397), and after a flat day -0.12 % (t -3.07, 14301). These t's are pooled over coins and not clustered by day; the 0.50 % is about 2.3 times the 0.22 % cost of a trade.
- **F5:** The book's mean gain of 0.089 % per coin-bar splits into 0.047 % from the market's own rise and 0.042 % from timing, at a mean allocation of 0.32. Its yearly gain follows the market: it is below holding in the rising years (2021: 0.169 vs 0.612 %/day) and loses less in the falling ones (2018: -0.048 vs -0.349 %/day).

## Ideas
- `031-03.b1.b1.e2.g1_month-scaled-trend-continuation` (from F1, F2, F3, F5): The larger a coin's 30-day rise relative to its daily volatility over the past 60 days, the more it keeps rising over the next 5 days beyond its normal drift.
- `031-03.b1.b1.e2.g2_one-day-fall-rebound` (from F4, F3): The larger a coin's one-day fall relative to its daily volatility over the past 60 days, the more it rebounds over the next day beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
