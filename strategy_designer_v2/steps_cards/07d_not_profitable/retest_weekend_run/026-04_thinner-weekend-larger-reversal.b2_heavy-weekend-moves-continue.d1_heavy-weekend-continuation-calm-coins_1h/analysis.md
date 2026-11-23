---
line: 7.d confirmed, not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4228 USD
---
## Findings
- **F1:** The Calmar fails (0.67 against 0.75) because of one late fall: the deepest fall of the book is −12.5 %, running 304 days from w22 to w24. Those three windows each lose (window sums −4.3 %, −3.9 %, −3.2 %). Their 51 weekend cases move −1.65 % in the bet's direction over 48h, against +1.18 % for the 344 cases of w1–w21, and 2025 alone loses −1.43 % per case.
- **F2:** The losses are concentrated in large bets on large weekend moves.
- **F3:** Cutting size does not repair the Calmar: the gain sits in the largest positions.
- **F4:** The continuation exists only when the heavy weekend move extends the coin's move of the five weekdays before it.
- **F5:** The signal's information is front-loaded.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week` (from F4, F1, F2): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 48 hours when it extends the coin's own move over those five weekdays. The continuation is the larger the larger the weekend move, the heavier the weekend volume against the weekdays, and the larger the preceding five-day move in the same direction.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation` (from F5, F1): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the first 12 hours of Monday. The continuation is the larger the larger the move and the heavier the weekend volume against the weekdays.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
