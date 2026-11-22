---
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback_1d
idea tested: 025-02_deeper-fall-bigger-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3662 USD
---
## Findings
- **F1:** The book's loss comes from shorts held well past the bounce. Of 330 trades, all short, the mean gross loss is −4.30 % and 29 % win. The 43 trades held over 5 days lose −16.3 % (21 trades, 6–10 days) and −27.7 % (22 trades, over 10 days) gross, and the worst 10 trades carry 56 % of the total gross loss. The 160 trades of 4–5 days are near flat, at −0.23 %.
- **F2:** The fade is a one-day effect. After a one-day rise of at least 2 usual moves with a negative 90-day return (66 cases), the coin's unusual move is −1.48 % over 1 day (t −2.36), −0.46 % over 2 days (t −0.62), −1.32 % over 5 days (t −1.10) and +2.28 % over 10 days (t 1.28). The book's short bars match this: +0.56 % gain on the situation's own next bar (t 1.99, 62 bars), then −0.33 % the bar after (t −1.70).
- **F3:** The tested gradient runs the wrong way. Over 5 days, the deepest quartile of 90-day falls gives −0.77 % unusual (n 17, t −0.29), while the shallowest gives −5.40 % (n 17, t −2.79). The deepest quartile even rises +8.19 % over 10 days (t 1.94). This matches step 5's slope t of 0.86 and its mean unusual move of −0.25 % per case, which is 1.3 times the 0.19 % cost of a trade, in the losing direction.
- **F4:** The fade holds when the 30-day return is also negative. In that case (42 cases) the unusual move is −2.11 % over 1 day (t −2.68), −1.75 % over 2 days (t −2.12) and −2.92 % over 5 days (t −2.18). When the 30-day return is positive (24 cases) the coin goes on to rise: −0.41 % over 1 day, then +1.83 % over 2 days and +1.56 % over 5 days.
- **F5:** The next-day fade grows slightly with the size of the bounce. By tercile of the one-day rise in usual moves, the 1-day unusual move is −1.11 % (small), −1.61 % (mid) and −1.73 % (big), 22 cases each, with t from −0.87 to −1.78.
- **F6:** One-day rises of at least 2 usual moves outside a negative 90-day return are followed by rises, not falls. Over 417 cases, the unusual move is +1.79 % over 5 days (t 2.62) and +3.94 % over 10 days (t 3.38). Most of these cases sit where the 90-day return could not be computed inside the window, so they are not only rising markets.

## Ideas
- `025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall` (from F1, F2, F4, F5): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, only while its 30-day return is also negative, the larger that one-day rise in usual daily moves, the larger its fall over the next 2 days.
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback` (from F2, F3, F5): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise in usual daily moves, the larger its fall over the next day.
- `025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends` (from F6): In a coin whose 90-day return is positive, the larger a one-day rise in usual daily moves, the larger its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
