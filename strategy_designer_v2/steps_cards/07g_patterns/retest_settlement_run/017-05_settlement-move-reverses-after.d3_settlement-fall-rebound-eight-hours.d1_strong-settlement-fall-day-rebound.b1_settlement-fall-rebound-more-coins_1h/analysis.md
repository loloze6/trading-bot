---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h
idea tested: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4895 USD
---
## Findings
- **F1:** Among the coins' most volatile thirds of days (recent 7-day hourly volatility over its 60-day level), a 24-hour fall is followed by a graded 24-hour rebound. The unusual move is +1.47 % (t 4.9, 807 non-overlapping cases) after a fall of more than 2 usual 24-hour moves and +0.98 % (t 6.1, 1387 cases) after a fall of 1 to 2. Small moves are followed by +0.16 % and +0.08 %, and rises of 1 to 2 usual moves by −0.49 % (t −3.3).
- **F2:** That high-volatility rebound after 24-hour falls held in 7 of 8 years, with 2022 flat at +0.18 % (t 0.3) and the others between +0.61 % and +2.90 %. It was positive in 83 % of windows. At +1.47 % per case it is 6.7 times the 0.22 % cost of a trade, against +0.08 % (0.3 times) for the tested settlement idea.
- **F3:** In the least volatile third, the same 24-hour falls carry on falling. The unusual move is −0.69 % (t −2.7, 390 cases) after a fall of more than 2 usual moves and +0.64 % (t 2.8, 398 cases) after a rise of more than 2. Falls of more than 1 usual move were followed by −1.39 % (t −4.3) in 2023 and −1.49 % (t −4.7) in 2024, so the reversal belongs to the volatile regime only.
- **F4:** Across all coins, the strength of the 24-hour reversal on the 24-hour grid is graded. It is +0.122 of a usual move (t 4.0, 1953 cases) after falls of more than 2 usual moves and +0.059 (t 4.0, 4337 cases) after falls of 1 to 2. Between −1 and +2 usual moves it is −0.012 to −0.034.
- **F5:** The settlement clock adds nothing to the 2-hour-fall rebound. After a fall of more than 3 usual 2-hour moves, the next 24 hours' unusual move is +0.40 % (t 3.0) at the 00:00/16:00 settlement bars against +1.04 % (t 15.6) at all other hours. Falls of more than 1 usual move rebound at almost every hour of the day, with hour-23 bars (+0.33 %, t 4.3) no different from hours 8, 11 or 12 (+0.44 % to +0.48 %).
- **F6:** The hours starting 20:00 and 21:00 UTC rise on average by +0.050 % (t 8.7) and +0.047 % (t 8.3) per hour across about 37,000 bars each. This holds in all 19 coins and in 7 of 8 years, with 2022 negative (t −5.2). It is larger in the high-volatility third (+0.079 %, t 5.9) than in the low (+0.024 %), but it is far below the 0.22 % cost of a trade.
- **F7:** Volume does peak near the 16:00 settlement, at 1.43–1.48 times its 30-day mean in hours 14–16. But the 00:00 settlement hour reaches only 1.10, the same as 12:00 (1.09), so the volume pattern follows the US session rather than the funding clock.

## Ideas
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins.g1_volatile-regime-daily-fall-rebound` (from F1, F2, F4, F5): When a coin's recent volatility is high against its own longer-run volatility, its fall over the past 24 hours is followed by a rise over the next 24 hours. The deeper the fall against its usual 24-hour move, and the higher that volatility, the larger the rise.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins.g2_calm-regime-daily-move-continuation` (from F3, F4): When a coin's recent volatility is low against its own longer-run volatility, its move over the past 24 hours continues in the same direction over the next 24 hours. The larger the move against its usual 24-hour move, the larger the continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
