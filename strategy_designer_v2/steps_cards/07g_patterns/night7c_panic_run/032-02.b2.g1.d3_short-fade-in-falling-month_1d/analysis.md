---
line: 7.g patterns
backtest: 032-02.b2.g1.d3_short-fade-in-falling-month_1d
idea tested: 032-02.b2.g1.d3_short-fade-in-falling-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4011 USD
---
## Findings
- **F1:** On days when the 20-day return is below 0, the next day's return minus the coin's mean falls steadily as the day's close moves up its high-low range. By close-location quintile it is +0.55 % (t 2.6), −0.06 %, −0.26 %, −0.54 % (t −2.7) and −0.80 % (t −4.2), about 735 cases each. The tested idea's close-location half is real and graded, and it runs both ways: a low close is followed by a rebound.
- **F2:** In the same falling-month days, the day's range multiple works against the idea. The widest-range quintile is followed by +0.35 % (t 1.35), the middle quintile by −0.65 % (t −3.6). The range weight adds size to the forecast exactly where the next-day fall vanishes.
- **F3:** In falling months, the next-day excess return also falls as the day's own 1-day return rises. By quintile it is +0.84 % (t 3.4), −0.11 %, −0.45 % (t −2.8), −0.78 % (t −4.1) and −0.61 % (t −3.0), about 735 cases each. That is a one-day reversal worth about 1.6 % from the lowest to the 4th quintile, against a 0.19 % cost per trade.
- **F4:** Over all days, on non-overlapping 5-day stretches, the 5-day excess return rises with how close the close sits to its 20-day high. By quintile of the distance to the high, from farthest to nearest, it is −0.37 %, −1.77 % (t −2.6), −1.33 % (t −2.3), +0.48 % and +3.50 % (t 4.7), about 285 cases each. The 20-day return gives the same picture: its 4th quintile shows +2.46 % (t 3.5) and its 2nd −2.58 % (t −4.2).
- **F5:** The book is a short bet on the market's own rise. On its worst-decile days the coins rose +6.3 %, and on its best-decile days they fell −7.2%. Its two worst windows, w10 and w11 (mean −0.07 % and −0.14 % a day), are the ones where the coins rose most (+0.40 % and +1.26 % a day).
- **F6:** The book's mean gain per active bar rises with the size of the short forecast, though weakly. The largest-forecast quintile earns +0.17 % (t 1.7) and the 4th earns −0.08 % (t −1.6). Most of the size the forecast carries adds little timing.

## Ideas
- `032-02.b2.g1.d3.g1_falling-month-one-day-close-reversal` (from F1, F2, F6): While a coin's 20-day return is negative, the higher its 1-day close sits within that day's high-low range, the lower its return over the next 1 day, so a close near the day's low is followed by a rise and a close near the high by a fall.
- `032-02.b2.g1.d3.g2_falling-month-daily-return-reversal` (from F3, F1): While a coin's 20-day return is negative, the larger its 1-day return, the more it falls over the next 1 day, and the deeper its 1-day fall, the more it rebounds over the next 1 day.
- `032-02.b2.g1.d3.g3_near-high-five-day-continuation` (from F4, F5): The nearer a coin's daily close sits to its highest high of the past 20 days, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
