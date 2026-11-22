---
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d
idea tested: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4661 USD
---
## Findings
- **F1:** Before any cost, the book's short bets lose money. Over 5 days the cases' total move in the short direction is −0.21 % (t −1.05, 2989 cases), against a trade cost of 0.22 %. Over 3 days it is −0.33 % (t −2.22) and over 10 days −0.57 % (t −1.99). The 4260 short trades, held 11.1 days on average, lose 3.69 % gross and 3.79 % net each. The failure therefore comes from the move the book captures, not from fees.
- **F2:** The book is short on 49 % of bars. On those bars it loses 0.042 % a day. Shorting coins whose drift is upward costs 0.100 % a day, and timing gains back only 0.058 %. The idea's unusual move (+0.54 % per case, strength 0.040) is too small to cover a normal drift of −0.75 % in the short direction.
- **F3:** The fade reverses with the depth of the 90-day fall, against the brief's reading.
- **F4:** Bounces far above the 90-day low lose, in the direction the idea predicts.
- **F5:** The book loses when the coin is already rising over 30 days. Short bars with a positive 30-day return lose 0.11 % a day (t −2.31, summed −5.35). Cases in that quartile fall −0.95 % over 5 days (t −2.14) in the short direction. Cases with a 30-day return between −23 % and −12 % gain +1.71 % (t 4.17).
- **F6:** The losses cluster in recovery years.

## Ideas
- `025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins.d1_bounces-fade-in-shallow-downtrends` (from F1, F2, F3, F6): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the smaller the coin's 90-day fall (the closer its 90-day return to zero), the larger the fall.
- `025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins.d2_deep-fall-bounces-keep-rising` (from F1, F3, F6): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move is followed by a further rise over the next 10 days, and the deeper the coin's 90-day fall, the larger that rise.
- `025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins.d3_bounces-after-monthly-upturn-continue` (from F4, F5, F6): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move is followed by a rise over the next 5 days, and the larger the coin's 30-day return before that day, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
