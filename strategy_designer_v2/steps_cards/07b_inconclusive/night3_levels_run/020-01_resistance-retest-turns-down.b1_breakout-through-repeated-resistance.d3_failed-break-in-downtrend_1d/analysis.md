---
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend_1d
idea tested: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3431 USD
---
## Findings
- **F1:** The tested result is on the predicted side but small and far from the bar: the mean drift-removed 10-day short-side move is +0.55 % per case (t 0.86, 627 cases), a strength of 0.043 of the coin's usual 14.5 % move. Because the coins' normal drift runs against a short (-1.17 % per 10 days), the total move is -0.63 %, below zero and so below the 0.19 % cost of a trade.
- **F2:** The grading the idea predicts runs the wrong way.
- **F3:** The effect sits in the smallest breaks, closes barely beyond the level. The lowest quartile of the break reading (touches x percent above the level, mean 0.34, first-day rise 3.0 %) gives +2.25 % over 10 days (t 2.26, 157 cases) and +3.57 % over 20 days (t 2.41, 143 cases). The other three quartiles are near zero: -0.05 % to +0.04 % over 10 days, and -0.6 % to +1.4 % over 20 days.
- **F4:** The move needs time to show. Over 5 days no break quartile exceeds +0.6 % (t at most 0.69). Over all cases the short-side move grows from +0.28 % at 5 days to +0.56 % at 10 days and +1.32 % at 20 days (t 1.46, 562 cases).
- **F5:** The effect is mixed across coins and periods, which drowns it in the full sample.
- **F6:** Size against cost: the small-break cases' unusual move of about 2.25 % over 10 days, and 3.6 % over 20, is 12 to 19 times the 0.19 % cost. Net of the -1.17 % drift against a short, the total move is still about +1.1 % over 10 days, so this part of the idea is large enough to pay, unlike the full sample (F1).

## Ideas
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend.b1_failed-break-more-coins` (from F1, F5): When a coin closes above a price where it turned down several times in the past 90 days after falling over the past 20 days, it tends to fall over the next 10 days, and the deeper its 20-day fall, the larger the decline.
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend.b2_marginal-break-fails-slowly` (from F2, F3, F4, F6): When a coin closes above a price where it turned down several times in the past 90 days after falling over the past 20 days, it tends to fall over the next 20 days, and the closer that close stays to the broken level, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
