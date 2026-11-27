---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1_high-close-after-fall-fades_1d
idea tested: 061-01.b1.b1.b1.d1_high-close-after-fall-fades
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5042 USD
---
## Findings
- **F1:** The book's losses come from shallow 5-day falls. Its 18 trades entered after a 5-day return between -5 % and -2 % lost 3.27 % each on average (−58.9 % summed). Its 22 trades entered after a 5-day fall deeper than 10 % earned 5.84 % each (+128.4 % summed). The profile's grid cases say the same over 5 days: deeper than −10 % gives an unusual move of +17.9 % (n 11, t 3.08), −10 % to −5 % gives +13.6 % (n 6, t 3.17), and −2 % to 0 % gives −6.9 % (n 3, t −2.39).
- **F2:** The size of the book's bet sorts its trades in order. The smallest third of entry |forecast| lost 1.90 % per trade (−49.4 % summed), the middle third earned 1.12 %, and the largest third earned 3.97 % (+103.3 %), over 26, 27 and 26 trades.
- **F3:** The deepest fall is −2.29 %, lasting 469 days from the peak in w9 to the trough in w13. With a yearly return of +2.4 %, it alone puts Calmar at 0.71, under 0.75. Inside it, trades lost −14.0 % summed in w11 and −56.6 % in w12. The losing trades of w12 and w17 had entered after a mean 5-day return of −6.0 %, the winners after −17.2 % (22 against 5 trades).
- **F4:** The book trades too little because a close in the top quarter of the range is rare. Only 4.4 % of grid bars are in the profile, and the book holds a position on 4 % of coin-days, with 79 trades (0.0096 trades per day). Widening the close to anywhere in the upper half of the range, after a negative 5-day return, more than doubles the 5-day cases (22 against 9) with a larger unusual move: +12.1 % (t 3.35) against +8.5 % (t 1.79). The added band, a close between 0.5 and 0.75 of the range, alone gives +14.6 % (n 13, t 2.81).
- **F5:** A deep fall without a high close is not the effect, so the depth of the fall is a valid grade of this idea, not an idea of its own.
- **F6:** The effect lives in the choppy agitated profile.

## Ideas
- `061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall` (from F1, F2, F4, F5, F6): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the deeper that 5-day fall, the larger the fall.
- `061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded` (from F1, F2, F3, F5): In a choppy, agitated market, when a coin's daily close sits near the top of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the fall grows with the depth of that 5-day fall, a shallow 5-day fall being followed by only a small one.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
