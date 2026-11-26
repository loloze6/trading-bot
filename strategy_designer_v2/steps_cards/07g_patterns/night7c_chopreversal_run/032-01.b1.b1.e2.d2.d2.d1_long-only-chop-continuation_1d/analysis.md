---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation_1d
idea tested: 032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4371 USD
---
## Findings
- **F1:** A coin's large down days tend to be followed by a bounce the next day. In the lowest quintile of the day's return scaled by the 30-day daily volatility, the next day's return averages +0.141 of a daily swing (t 2.29 with same-day cases taken together; 1292 cases on 389 days). The other quintiles give +0.041, +0.028, −0.038 and +0.031, none with a t above 0.75. Both folds shown point the same way: fold B +0.191 (t 2.48), fold C +0.097 (t 1.03).
- **F2:** In choppy months (ER30 ≤ 0.30), the past week's move continues on both sides rather than reversing. The continuation is +1.3 % (t 1.57), +1.2 % (t 0.73) and +4.1 % (t 2.41) by tercile of the scaled 7-day move. The tested long side alone (30-day and 7-day returns both up) averages +4.1 % in each fold, with t 1.86 in fold B and t 1.45 in fold C.
- **F3:** The short-side mirror does not carry the same weight. Choppy down-months with a down-week are followed by −3.4 % unusual moves (simple t −3.23). With same-day cases taken together, the raw move is only −2.2 % (t −1.24, 166 cases on 69 days). It is not graded: −4.2 %, −2.1 % and −3.7 % from the largest to the smallest fall. Fold B gives only t −0.39.
- **F4:** In trending months (ER30 > 0.30), the weekly move reverses only after the smaller moves: +3.7 % (t 2.03) and +3.2 % (t 1.36) in the two lower terciles of the scaled 7-day move, and −1.8 % (t −0.64) in the top tercile. This runs against grading.
- **F5:** There are calendar effects, but none is graded and neither carries a usable effect. The day after a Thursday close averages +0.168 of a daily swing (t 2.19, 153 days). The day after a Wednesday close averages −0.133 (t −1.45), negative in both folds. The book's Thursday returns average −0.17 % (simple t −3.07).
- **F6:** Volatility compression is unstable across folds. The lowest quartile of 30-day over 60-day volatility gives +2.0 % unusual 7-day moves overall (t 0.94): +7.8 % in fold B (t 2.90) but −1.6 % in fold C (t −0.57).
- **F7:** The book's trades pay more as the entry forecast rises: mean net profit of 3.8 %, 5.0 % and 6.9 % by forecast tercile, with medians of 0.8 %, 1.8 % and 3.1 %. Book daily returns are positive in 8 of the 12 windows shown.

## Ideas
- `032-01.b1.b1.e2.d2.d2.d1.g1_next-day-rebound-after-sharp-falls` (from F1): The larger a coin's fall over the past day, measured in its usual daily swings over the past 30 days, the larger the rebound in its price over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
