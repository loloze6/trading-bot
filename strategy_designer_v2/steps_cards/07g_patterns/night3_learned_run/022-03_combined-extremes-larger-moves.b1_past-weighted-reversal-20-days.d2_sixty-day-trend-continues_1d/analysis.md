---
line: 7.g patterns
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
idea tested: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4139 USD
---
## Findings
- **F1:** Over the next 20 days, the 60-day return's continuation is weak and does not grow with its size. In this record, the mean unusual move in the forecast's direction is +0.04 to +0.14 usual moves in every quartile of relative volatility, and only the highest-volatility quartile reaches t 1.97 (192 cases). Within that quartile the sign changes by year: t −2.07 in 2022, then t +2.30 to +3.21 in 2023-2025.
- **F2:** Splitting the forecast by side and by volatility shows that relative volatility, not the trend, carries the direction. Longs after 60-day rises gain +0.15 usual moves when relative volatility is high (255 cases) and lose −0.06 when it is low (263). Shorts after 60-day falls gain +0.14 when it is low (306) and lose −0.13 when it is high (224). So high relative volatility is followed by rises whatever the trend's sign.
- **F3:** Relative volatility as a graded signal (20-day volatility over its 60-day median) has a slope t of 3.27 on 20-day standardised moves (1048 cases) and 2.45 on 5-day moves (4396 cases). But its quintiles are not ordered: the quintile means are +0.04, −0.19, −0.11, +0.13 and +0.18 usual moves. Its yearly sign also changes: t +4.19 in 2022 and +3.97 in 2023, against −2.90 in 2021 and −2.82 in 2025.
- **F4:** On the start-of-window grid, reversal after a large day measured against volatility looks strong over 20 days: slope t −4.69 for the raw return, t 3.59 for the volatility-scaled reversal on 1048 cases, and stronger at high relative volatility (t 3.82, 479 cases). The same measure on grids shifted by 7 and 13 days gives t −2.04 and t +0.70 (1116 cases each). Its yearly sign also changes: t −4.17 in 2019 against t +4.37 in 2025. Its 10-day version has t 0.42 on 2443 cases. It depends on the grid and the period rather than on the market.
- **F5:** Standardised 1-day moves differ by weekday: Friday +0.046 usual moves (t 4.08, 4814 cases), Tuesday and Thursday about +0.04 (t 2.9), Wednesday −0.057 (t −3.34), Monday −0.035 (t −2.48). At about 0.05 of a 1-day move, that is about 0.2 %, below or at the 0.22 % cost of a buy and a sell. Each weekday is also a fixed condition rather than a graded situation.
- **F6:** The book earns 2.9 bps a day. Its daily returns correlate only 0.19 with the coin's, and per coin it ranges from −9.0 bps (AAVE) to +15.5 bps (TRX). On the book's best 1 % of days the coin rose 10.4 % on average. On its worst 1 % the coin fell only 0.8 %: the losses come from short positions during rises and from being sized up into reversals, more than from the coin's own falls.
- **F7:** Signals after a large 5-day move, after a 20-day return, by 20-day volatility level and by nearness to the 20-day high show no graded slope above t 2.6 at 5 or 20 days. None of these slopes holds both directions across their quintiles.

## Ideas
- No ideas: Over about twenty angles (forecast by side and volatility, five price signals at two horizons, weekdays, years, coins, grid offsets, the book's tails), nothing stands out from chance enough to support a graded idea. The strongest pattern, relative volatility (t 3.27), reverses sign by year with t near ±3, and the large-day reversal (t 3.59) changes sign when the grid is shifted by 7 days. The weekday effect is a fixed condition, not a graded situation, and its move is no larger than a trade's cost.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
