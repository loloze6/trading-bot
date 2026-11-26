---
line: 7.d confirmed, not profitable
backtest: 032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts_1d
idea tested: 032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3896 USD
---
## Findings
- **F1:** The book did not trade the idea's "while": 2,950 of the 6,653 held coin-bars in folds B, C (44 %) were held after the regime had ended, because of the 7-bar minimum holding. Those bars earned +1.55 in summed bar gains against +7.72 on the 3,703 in-regime bars, and the off-regime shorts lost (1,451 bars, mean −0.071 % a bar, sum −1.03).
- **F2:** The book's gain comes from bars where the position's side still agrees with both the 7-day and the 30-day move (3,127 bars, mean +0.284 % a bar, sum +8.88). Once the 7-day move has turned against the position, held bars lose: −0.047 % a bar on 1,154 bars when the month also disagrees, −0.006 % on 1,234 bars when the month still agrees. These are the bars an exit on the week turning would remove.
- **F3:** The book's deepest fall is −26.7 %, a 388-day episode from w11 to w15. In it the book lost 10.1 % in w12, where holding lost 2.7 %, and was flat (−0.9 %) in w14, where holding fell 52 %. In folds B, C alone the book's Calmar is 1.37 (yearly +36.7 %); the failing 0.59 comes with folds A, D, so the falls, not the gain, are what the repair must cut.
- **F4:** The short side carries the weak part of the book. Held shorts earn +0.126 % a bar in the regime against +0.290 % for held longs. Shorts lose on BTC (sum −0.29) and XMR (−0.04), while longs pay on every coin (BTC +1.63, ETH +1.89, XRP +1.64, ZEC +1.61).
- **F5:** The follow-through is weakest when the 30 days made almost no net progress. In the lowest quartile of the 30-day efficiency ratio (mean 0.04), held bars earn +0.058 % a bar, against +0.203 %, +0.244 % and +0.237 % in the three higher quartiles (1,253 bars each). In that quartile the month's sign, which sets the side, is nearly noise.
- **F6:** Held-bar gain falls as the 30-day volatility rises against its own 180-day median: +0.64 %, +0.38 %, +0.25 % and +0.08 % a bar from the calmest to the most agitated quartile (381 bars each). I did not measure what the 7-day move does in calm states without the signal, so this is not used as a repair.

## Ideas
- `032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break` (from F1, F2, F3): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings is followed by a move the same way, day by day, only on the days the 30 days are still choppy and the 7-day move still points the same way as the 30-day net move. The larger the scaled 7-day move, the larger the following daily moves, and the follow-through stops on the first day either the chop or the agreement ends.
- `032-01.b1.b1.e2.d2.d1.d2_chop-continuation-month-strength-graded` (from F5, F2): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, and its 7-day move points the same way as its 30-day net move, the following 7 days continue that move. The larger the 30-day net move is against the sum of its daily moves within the choppy range, and the larger the scaled 7-day move, the larger the continuation.
- `032-01.b1.b1.e2.d2.d1.d3_chop-continuation-long-side-only` (from F4, F1, F3): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, and both its 7-day and its 30-day moves are up, the coin rises over the next 7 days. The rise is larger the larger the up 7-day move counted in 30-day daily swings, while the chop and the agreement last.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
