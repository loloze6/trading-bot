---
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
idea tested: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4331 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side (+0.62 % unusual 5-day fall per case, t 2.81, 2312 cases). It is inconclusive only because the grading ran backwards. Cases at forecast −10 or below faded 0.63 % less than cases between −2 and −10. In my recount the −5..−2 bucket faded +1.19 % (t 3.33, n 702), against +0.20 % (t 0.43, n 666) for the full −20 bucket.
- **F2:** The grading inverts because the forecast does not track the bounce's size in raw usual moves. It restandardises the move against its own past 60 values and saturates near 1.6 usual moves. Measured on the raw size (the day's return over its 20-day standard deviation), the cases do follow the idea at the top end. Bounces above 3 usual moves faded +4.77 % over 5 days (t 3.02, n 33), against +0.11 % at 1 to 1.5 moves (t 0.26, n 673) and +1.01 % at 2 to 3 moves (t 1.13, n 224).
- **F3:** On the full 5-day grid of falling coins, rises above 2 usual moves were followed by an unusual fall of 3.90 % (t 2.79, n 78). On the event study (rises deduplicated per 5-day cell) the fall was 4.60 % (t 3.17, n 58). By contrast, rises of 0 to 1 usual moves were followed by only 0.27 % (t 0.80, n 990), and the correlation of bounce size with the later fade among rises is only 0.086.
- **F4:** Much of the main measure's mean is the falling regime's own continued slide, not the bounce. On the grid, down days of 0 to −1 usual moves in falling coins were followed by a 1.07 % unusual fall (t 3.96, n 1167). All falling-coin grid bars together showed +0.33 % (t 1.85, n 3579) over 5 days and +0.59 % (t 2.25, n 3418) over 10 days.
- **F5:** The same large rises in coins with a non-negative 90-day return were followed by further rises, the opposite of falling coins, which the brief names as its test. Rises above 2 usual moves were followed by an unusual rise of 8.69 % (t −2.63 in the short direction, n 131). In the event study, rises of 2 to 3 usual moves were followed by a 3.83 % rise (t −3.31, n 431).
- **F6:** The effect is mixed across periods and fall depths. By year, cases were 2.79 % in 2025 (t 5.51) and 2.21 % in 2022 (t 2.38), against −3.22 % in 2020 (t −3.65). By depth, the shallowest quartile of 90-day falls gave 2.76 % (t 5.08), while the deepest (below −43 %) gave −1.60 % (t −1.35).
- **F7:** The fade over 10 days (+1.04 %, t 3.19, n 2208) is larger than over 5 days (+0.60 %, t 2.74). The test also used all 19 coins over all four folds, so there is no more daily data to add.

## Ideas
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.b1_raw-size-outsized-bounces-fade` (from F1, F2, F3): In a coin whose 90-day return is negative, a one-day rise measured in units of its 20-day standard deviation of daily returns is followed by a fall over the next 5 days. The fall grows steeply with that raw number of usual daily moves: rises of one usual move or less are followed by almost nothing, and the rare rises of several usual moves are given back by several percent.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.b2_outsized-rises-continue-uptrends` (from F5): In a coin whose 90-day return is positive or zero, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a further rise over the next 5 days. The larger the rise in usual daily moves, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
