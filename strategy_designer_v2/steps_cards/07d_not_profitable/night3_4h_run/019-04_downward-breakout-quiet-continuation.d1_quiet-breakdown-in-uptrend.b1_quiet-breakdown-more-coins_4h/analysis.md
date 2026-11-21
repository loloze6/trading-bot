---
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
idea tested: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4767 USD
---
## Findings
- **F1:** The book's regime points the wrong way. On downward breaks (n 1965, one per 18-bar grid cell) the coin then rises more than its usual drift while its 30-day return is positive: the unusual 18-bar move is +0.60 %, t 2.9, so the short loses. While the 30-day return is not positive, the same breaks are followed by a fall: -0.34 %, t -2.2, n 2938.
- **F2:** The narrowness gradient is real and runs the way the idea says. Across all downward breaks, the unusual 18-bar move goes from -1.04 % (t -3.9, n 981) in the narrowest fifth of the two-day range (about 1.5 times the 30-day mean bar range) to +1.30 % (t +4.0, n 981) in the widest fifth (about 4.7 times). The correlation of range width with the unusual move is +0.12.
- **F3:** The narrow-break fall is concentrated in falling months. While the 30-day return is not positive, the narrowest fifth falls -1.35 % unusual (t -4.4, n 649, strength 0.13) and -0.81 % in total, about 6 and 3.7 times the 0.22 % round-trip cost. While the 30-day return is positive, the same narrowest fifth gives only -0.43 % (t -0.9, n 332).
- **F4:** In rising months, a downward break out of a wide two-day range is followed by a rise, and it grades by width. The unusual 18-bar move across the third, fourth and widest fifths is +0.40 %, +1.13 % (t 2.6) and +1.88 % (t 3.5, n 394), with a total move of +2.4 % (about 11 times the cost) and +3.8 % over 36 bars.
- **F5:** The book shorts the cases that rise. Because its width is standardised over its own past values (median post-pipeline value 5.97), 865 of its 1606 active cases sit in the three wider fifths. There the coin's unusual move is +0.39 %, +1.07 % (t 2.2) and +1.51 %. This is why the book's Sharpe is -0.39, its trades win 29 % of the time and its mean daily return is -0.00005.
- **F6:** Downward breaks that come after the deepest 3-day falls (lowest fifth of the 3-day return, n 981) are followed by an unusual rise of +1.43 % (t 4.2) and +3.1 % in total over 36 bars. Their two-day range is wide (median 3.6 times the mean bar range), which is the same rebound as in F4.
- **F7:** Upward breaks carry no narrowness gradient: the correlation of range width with the unusual move is 0.002, and the fifths run from -0.13 % to +0.68 % with no order.

## Ideas
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.d1_quiet-breakdown-in-downtrend` (from F1, F2, F3): When a four-hour bar closes below the lowest low of a coin's preceding two-day narrow stretch, the coin falls over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the fall, only while the coin's 30-day return is negative.
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.d2_wide-breakdown-rebound-uptrend` (from F1, F4, F5, F6): When a four-hour bar closes below the lowest low of a coin's preceding two days, the coin rises over the next three days, and the wider those two days' range was compared with the coin's 30-day average four-hour range, the larger the rise, only while the coin's 30-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
