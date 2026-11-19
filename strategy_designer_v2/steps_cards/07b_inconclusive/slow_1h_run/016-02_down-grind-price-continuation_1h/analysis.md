---
line: 7.b inconclusive
backtest: 016-02_down-grind-price-continuation_1h
idea tested: 016-02_down-grind-price-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3131 USD
---
## Findings
- **F1:** The main measure's small positive mean comes from one year. Over all 2,762 grid bars it is a gain of 0.00151 with t 0.95, but 2018 alone gives 0.0218 (t 4.58, n 417). With 2018 left out, the gain is -0.0021 (t -1.26, n 2,345), and the other seven years split three positive and four negative, none with |t| above 1.72.
- **F2:** The forecast hardly varies once a fall has happened, so the test is close to "short after any 3-day fall". Its standard deviation is 0.76 around -10.0, with an interquartile range of -10.41 to -9.63. Its Spearman correlation with the excess 72-hour return is -0.015 (p 0.43).
- **F3:** The grind share itself does not grade the outcome, and its strongest grinds lean the wrong way. Recomputed, the five share quintiles from least to most grind give excess 72-hour returns of -0.0023, -0.0060, -0.0022, -0.0031 and +0.0003, with Spearman rho +0.020 (p 0.30).
- **F4:** Short grid bars are followed by an excess 72-hour return of only -0.0015 (t -0.96, n 2,762), against +0.0014 (t 0.89, n 2,921) on flat bars. Any continuation after a fall is too small to stand out from the coins' own moves.
- **F5:** The size of the 3-day fall matters more than how it was built, and it points to reversal. Spearman rho between the past 72-hour return and the excess next-72-hour return is -0.062 (p 0.0015). The largest-fall tercile is followed by +0.0076 and +0.0017 (the low and high forecast halves), while the two smaller-fall terciles are followed by -0.0013 to -0.0097.
- **F6:** The gain is positive when the coin's 30-day return is negative (0.0051, t 2.11, n 1,181), but this does not grade with the grind share. Inside that regime the share terciles give -0.0066, -0.0019 and -0.0060, with rho 0.003. The regime's excess return is mostly 2018 (-0.0175, t -3.02), and the other years are mixed (-0.0055 to +0.0028).
- **F7:** The plan's 72-hour horizon is not where the effect hides. The same gain over 24 hours is -0.0002 (t -0.22), and over 168 hours it is 0.0012 (t 0.46).

## Ideas
- `016-02_down-grind-price-continuation.b1_down-grind-on-more-coins` (from F1, F2, F4): When a coin has fallen over the past 3 days, the larger the share of that fall made by many small hourly losses in the same direction, rather than by its few biggest hours, the more the coin keeps falling over the next 3 days.
- `016-02_down-grind-price-continuation.b2_large-falls-partly-reverse` (from F5, F3): When a coin has fallen over the past 3 days, the larger that 3-day fall, the more the coin rises back over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
