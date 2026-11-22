---
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
idea tested: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3660 USD
---
## Findings
- **F1:** The effect sits only in the most extreme streaks. In the top decile of streak loss (mean 4.08 usual 4h moves, 528 cases), the unusual 18-bar move is +1.67 % with t 3.67, and +2.09 % over 36 bars with t 3.49. The other nine deciles (losses of 0.7 to 2.5 usual moves) range from −0.63 % to +0.43 %, with no t above 1.31 in absolute value.
- **F2:** The test measured mostly ordinary streaks rather than extreme ones, so the effect was diluted. 5,031 of the 5,674 cases came on streaks of at most 2 bars. The correlation between streak loss and the 18-bar unusual move is only 0.047. The overall mean is +0.05 % with t 0.48, a strength of 0.007.
- **F3:** The overall result is on the side the idea predicts and grows with the forecast. The two highest forecast quintiles give +0.66 % (t 2.89) and +0.50 % (t 1.70) over 18 bars. The three lowest give −0.39 %, −0.23 % and −0.26 %, and the above-minus-below-median check is +0.77 %.
- **F4:** The market's own year-by-year moves drown the effect in the bulk of the cases. Cases outside the top fifth of streak loss swing from −1.83 % (t −4.50) in 2018 and −0.79 % (t −2.46) in 2022 to +1.18 % (t 3.54) in 2020. The top fifth is positive over 18 bars in all eight years, from +0.03 % to +1.03 %.
- **F5:** The rebound after the largest streaks is stronger while the coin's 30-day return is positive. In the top fifth of streak loss, the 18-bar move is +1.28 % (t 2.12, 336 cases) in that state, against +0.56 % (t 1.47, 486 cases) while the 30-day return is negative. Over 36 bars the same split gives +2.62 % (t 3.37) against +0.58 % (t 0.99).
- **F6:** The top fifth of streak loss rebounds on every coin over 18 bars, from +0.33 % (BTC) to +1.11 % (ZEC), with t from 0.38 to 1.54. Its per-case move is several times the 0.19 % cost of a trade, while the average case's unusual move is only 0.3 times that cost.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume.b1_extreme-down-streak-rebound-more-coins` (from F3, F6): When a coin has just fallen in an unbroken streak of four-hour periods whose loss is several times its typical four-hour move over the past 30 days, it rises over the next one to three days, whatever the volume did during the streak. The larger the loss relative to that typical move, the larger the rise.
- `024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume.b2_down-streak-rebound-in-uptrends` (from F1, F4, F5): When a coin has just fallen in an unbroken streak of four-hour periods whose loss is several times its typical four-hour move over the past 30 days, it rises over the next one to three days, whatever the volume did during the streak, the larger the loss relative to that typical move, the larger the rise, only while the coin's own 30-day return is positive.
- `024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume.b3_deepest-streaks-rebound-longer` (from F1, F2, F6): When a coin has fallen in an unbroken streak of four-hour periods whose loss is around four or more times its typical four-hour move over the past 30 days, it rises over the next three to six days. The further the loss goes beyond that typical move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
