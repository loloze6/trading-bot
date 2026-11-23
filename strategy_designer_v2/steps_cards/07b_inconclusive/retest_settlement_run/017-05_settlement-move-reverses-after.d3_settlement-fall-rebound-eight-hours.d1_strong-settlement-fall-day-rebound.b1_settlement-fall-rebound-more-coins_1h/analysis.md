---
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h
idea tested: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4334 USD
---
## Findings
- **F1:** The main measure is on the predicted side but small: the 13,768 settlement-fall cases (forecast ≥ 2) end their 24 hours +0.075 % above the coin's normal drift with t 1.58. The rebound is clearer early, at +0.155 % with t 5.5 over 8 hours, then fades to −0.024 % with t −0.37 over 48 hours.
- **F2:** The effect lives entirely in coins in a rising month. When the coin's 30-day return is positive, the cases' unusual 24-hour move is +0.379 % with t 4.95 (n 4,884), and their total move is +0.561 % with t 7.3, 2.5 times the 0.22 % trade cost, a strength of 0.071. When the 30-day return is negative, the unusual move is −0.093 % with t −1.54 (n 8,884), which drowns the pooled result.
- **F3:** Inside a rising month the effect is graded by the depth of the fall. The unusual 24-hour move rises from +0.065 % (t 0.40) for forecasts of 2–4 to +0.629 % (t 5.1, n 1,849) for falls at the cap of 20. It also grows with the 30-day rise itself, from −0.035 % in the lowest quartile to +0.717 % and +0.645 % in the two highest quartiles (t 4.65 and 3.34).
- **F4:** The settlement clock is not what carries the rebound. Falls of at least 1.5 usual 2-hour moves at any hour rebound +0.354 % over 24 hours (t 9.4, n 27,018). Most non-settlement hours give +0.4 % to +0.8 %, for example hour 0 at +0.70 % (t 6.9) and hour 12 at +0.80 % (t 4.3), while the 15:00 and 14:00 hours just before settlement are among the weakest at +0.146 % and −0.020 %.
- **F5:** The same rising-month graded rebound appears at any hour, so it is a dip-in-uptrend effect rather than a funding one. With a positive 30-day return, a fall of at least 1 usual move gives +0.224 % with t 4.5 (n 12,612), graded from +0.090 % for falls of 1–1.5 usual moves to +0.540 % for falls beyond 3.
- **F6:** The effect is not stable across years. The pooled cases lose −0.60 % (t −5.2) in 2022 and −0.35 % (t −3.5) in 2025, and even in a rising month 2022 gives −0.13 % and 2025 gives −0.18 %, against +0.87 % to +1.05 % in 2020–2021.

## Ideas
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins.b1_settlement-fall-rebound-uptrend` (from F1, F2, F3, F6): The return over the 24 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it, only while the coin's 30-day return is positive. Inside that state, the larger the fall against the coin's usual 2-hour move, the larger the rise.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins.b2_uptrend-two-hour-dip-rebound` (from F4, F5, F3): In a coin whose 30-day return is positive, a fall over the past 2 hours at any hour of the day is followed by a rise over the next 24 hours. The larger the fall against the coin's usual 2-hour move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
