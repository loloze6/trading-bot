---
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
idea tested: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4421 USD
---
## Findings
- **F1:** The book's profit comes from the long side only. Long trades entered in the rising regime averaged +6.66 % net (median +0.87 %, 57 % winners, 4594 trades). Short trades entered in the falling regime averaged −3.13 % net (median −1.46 %, 37 % winners, 4359 trades). The book's best 2 % of days (mean +5.5 %, n 58) came with a net long share of 0.34, while its worst 2 % (mean −5.0 %, n 57) came with a net long share of 0.00.
- **F2:** In the falling regime the fade is not graded across rises; it appears only for the largest ones. The mean unusual 5-day move on non-overlapping grid bars is −0.26 % (t −0.74, n 948) for day-rises of 0–1 usual moves, −0.33 % (t −0.43, n 264) for 1–2 moves, −2.38 % (t −1.64, n 70) for 2–3 moves and −7.43 % (t −3.65, n 27) above 3 moves. This explains why most short bets lose.
- **F3:** In the rising regime, rises are followed by continuation that grows with the rise. The mean unusual 5-day move is +2.10 % (t 3.02, n 357) for 1–2 usual moves, +4.77 % (t 3.21, n 92) for 2–3 moves and +12.3 % (t 1.90, n 64) above 3 moves. The Spearman rho of rise size against the 5-day move for rises above 1 move is 0.10 (p 0.02). The yearly mean was positive in 7 of 8 years, with 2025 at −0.77 %.
- **F4:** When the 90-day return is negative, the 20-day return predicts the next 5 days in the opposite direction. By per-coin 20-day-return quintile, from lowest to highest, the mean unusual 5-day moves are +0.50 % (t 1.40, n 885), −0.58 % (t −1.51), −1.27 % (t −3.33), −1.40 % (t −3.19) and −1.17 % (t −1.54, n 272). A falling coin that has recovered over the past weeks tends to slip back.
- **F5:** When the 90-day return is positive, the 20-day return predicts the next 5 days in the same direction. The lowest two quintiles give −0.06 % and −1.01 % (t −2.00), and the highest two give +1.11 % (t 2.37, n 714) and +1.51 % (t 2.45, n 937).
- **F6:** In the falling regime, mild down days of 0 to −1 usual moves are followed by a further unusual 5-day move of −0.91 % (t −3.32, n 1108), negative in 6 of 8 years. Larger drops are not graded the same way: 1–2 moves gives +0.49 % and 2–3 moves gives +1.87 %, so no graded idea follows from this.
- **F7:** Weekday and volatility patterns did not stand out once correlation across coins was removed. With each day averaged across coins first, the largest weekday t is 1.91 (Friday, +0.30 %, n 414). Volatility terciles inside each regime are not monotonic (falling regime: −1.02 %, −0.09 %, −0.64 %).

## Ideas
- `025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins.g1_falling-coin-recoveries-fade` (from F4, F2): In one coin whose 90-day return is negative, the higher its 20-day return, the lower its return over the next 5 days: a recovery over weeks inside a long fall is given back.
- `025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins.g2_rising-coin-momentum-continues` (from F5, F3, F1): In one coin whose 90-day return is positive, the higher its 20-day return, the higher its return over the next 5 days.
- `025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins.g3_sharp-rises-extend-uptrends` (from F3, F1): In one coin whose 90-day return is positive, the larger its one-day rise measured in its usual daily moves, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
