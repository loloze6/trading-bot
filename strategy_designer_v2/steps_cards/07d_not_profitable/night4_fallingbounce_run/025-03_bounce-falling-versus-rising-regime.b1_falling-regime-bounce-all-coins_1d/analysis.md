---
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
idea tested: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4249 USD
---
## Findings
- **F1:** The Calmar failure comes from the short side. Chained alone, the short positions return −7.1 % a year with a deepest fall of −65 % (Sharpe −0.23). The long positions return +34 % a year with a deepest fall of only −25 % (Sharpe 1.35). The whole book returns 21 % a year with a −59 % fall, so its Calmar is 0.36.
- **F2:** The book's deepest fall ran −59 % over 1014 days, across w15 to w23. Over that stretch the short positions lost −0.70 in summed daily gain and the long positions only −0.06, so the shorts carried almost all of it.
- **F3:** Inside the book's six deepest falls the book was short more often than elsewhere (41 % of bars against 32 %). Its shorts lost there (−0.075 % per bar against +0.19 % elsewhere). The coins were also far less extended over 90 days (mean 90-day return +14 % against +66 %).
- **F4:** On the 5-day grid, the short signals made in the falling regime fade only while the coin is still deep in its fall. In the most negative quarter of 30-day returns (mean −28 %) the unusual 5-day move is −3.9 % (t −3.29, 135 cases). In the quarter whose 30-day return is already positive (mean +21 %) it is +1.3 % (t +1.15, 134 cases). The grading is monotone across the four quarters (−3.9, −1.5, −0.1, +1.3 %).
- **F5:** The same grading holds for distance from the 90-day low. Bounces that start within about 6 % of that low are followed by −4.3 % (t −2.42, 37 cases), and those within 14 % by −3.5 % (t −2.07, 36 cases). Bounces from a coin already 60 % above its low are followed by +4.2 % (t +1.60, 37 cases), which is a move against the short.
- **F6:** The cost of a trade does not explain the failure. The idea's total move per case is 0.73 % against a 0.22 % cost per trade, 3.3 times it. The loss lies in shorts taken into bounces that had already turned into recoveries.

## Ideas
- `025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins.d1_bounce-fades-inside-deep-fall` (from F1, F2, F3, F4): In one coin, the 5-day return after a one-day rise of several usual daily moves is lower when its 90-day return is negative than when its 90-day return is positive. The gap widens as the rise gets larger, only while its 30-day return is still negative, and it grows the deeper that 30-day fall is.
- `025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins.d2_bounce-near-the-low-fades` (from F4, F5, F2): In one coin whose 90-day return is negative, a one-day rise of several usual daily moves is followed by a lower 5-day return the closer the coin's close stands to its lowest close of the past 90 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
