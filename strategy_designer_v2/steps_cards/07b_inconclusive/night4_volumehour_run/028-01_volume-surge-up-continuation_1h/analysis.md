---
line: 7.b inconclusive
backtest: 028-01_volume-surge-up-continuation_1h
idea tested: 028-01_volume-surge-up-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3381 USD
---
## Findings
- **F1:** The tested effect is zero rather than weak. Step 5's mean excess 6-hour return over 8827 long-bet cases is +0.0036 % with t 0.14, which is 0.000 of the coin's usual 6-hour move (1.98 %). The total move of +0.04 % per case is 0.4 times the 0.11 % cost of a trade, so the book lost money (Sharpe -0.13, mean daily return -0.016 %).
- **F2:** The effect does not grow with the forecast, so the strongest cases carry nothing. Across forecast bins the mean excess 6-hour return is +6.8 bp (t 0.94, n 951) for 2–3, -2.8 bp (t -0.42) for 3–5, -4.5 bp (t -0.60) for 5–8, -2.3 bp (t -0.26) for 8–12, and +0.4 bp (t 0.12, n 4580) for the extreme 12–20 bin.
- **F3:** The idea's own range of horizons, 1 to 6 hours, was not measured in the wrong place, because every horizon is near zero. On the same cases the mean excess return is +1.2 bp at 1 hour (t 1.02), -1.8 bp at 2 hours (t -1.13), -2.6 bp at 3 hours (t -1.34) and 0.0 bp at 6 hours (t 0.01), with n 8098 at each.
- **F4:** The effect changes sign from year to year rather than sitting in one period:
- **F5:** The effect is the same in both coins. The mean excess 6-hour return is -0.7 bp (t -0.22, n 3962) for BTC and +0.7 bp (t 0.18, n 4136) for ETH.
- **F6:** Among hours rising at least 3 usual hourly moves, continuation does not grow with volume, against the idea's grading. The 2-hour signed excess is:
- **F7:** Down-hours of at least 3 usual moves tend, if anything, to be followed by rebounds, also not graded by volume. The signed 6-hour excess is -35.7 bp (t -2.09, n 237) at volume ratio 1.5–3, -8.4 bp (t -0.58) at 3–5 and -6.0 bp (t -0.42) above 5. This is a single cell among 32 tested, so it is too thin to found an idea on.

## Ideas
- No ideas: The tested measure is essentially zero (t 0.14 on 8827 cases, F1), the plan already used all folds for BTC and ETH, and no coin, year, horizon, forecast strength or volume level shows the effect consistently (F2–F7), so the clear answer is that volume-confirmed up-hours in BTC and ETH do not continue over the next two to six hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
