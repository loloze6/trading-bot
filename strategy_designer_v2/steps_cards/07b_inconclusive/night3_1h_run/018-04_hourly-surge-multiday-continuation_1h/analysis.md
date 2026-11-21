---
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation_1h
idea tested: 018-04_hourly-surge-multiday-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3388 USD
---
## Findings
- **F1:** The test measured the idea mostly where it is absent: of the 3205 cases, 2743 were forecast rises at 0.5 to 2 multiples of the usual daily move, because the plan reads "while" instead of "first reaches". On those cases the 120-hour unusual move is -0.62 % (0.5 to 1 multiple, t -1.61), -0.15 % (1 to 1.5, t -0.56) and +0.65 % (1.5 to 2, t 1.25). Over 24 hours, all cases together drift down, at -0.27 % (t -3.20). Together this gives the test's flat -0.01 % (t -0.06).
- **F2:** Measured where the idea says, at the hour the 24-hour return first reaches 2 multiples (first per 120-hour cell), the 5-day unusual move is +0.70 % per case (t 2.53, 1888 cases), a strength of 0.059. The total move is +1.35 %, 7 times the 0.19 % cost of a trade. At 3 multiples it is +1.12 % (t 2.69, 947 cases).
- **F3:** Among those first crossings the size of the multiple does not grade the move. The slope of the 5-day unusual move on the multiple is -0.0042 and the Spearman correlation is -0.025. The 2 to 2.5 band carries the effect (+0.97 %, t 3.05, 1447 cases), while 2.5 to 3 gives -0.43 % (t -0.70) and above 4 gives -0.95 % (t -0.41).
- **F4:** The coin's 7-day return before the crossing grades the effect. The 5-day unusual move rises from -0.72 % (t -1.49) in its lowest quarter to +0.95 % (t 2.20) and +0.71 % (t 1.65) in the middle quarters, and to +1.74 % (t 2.17, 463 cases) in its highest quarter. The lowest quarter's total move is -0.07 %, below the cost, while the highest quarter's is +2.41 %.
- **F5:** The effect is mixed across periods and coins. It is negative in 2018 (-2.43 %, t -2.68) and 2022 (-0.50 %), and strong in 2020 (+2.56 %, t 3.34) and 2024 (+1.74 %, t 2.67). By coin, it ranges from ZEC at +2.09 % (t 2.22) to BTC and LTC near zero (+0.15 %, +0.03 %). So it holds mainly when the coin is already rising, consistent with F4.

## Ideas
- `018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise` (from F1, F2, F4, F5): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while its 7-day return is positive. The larger that 7-day return, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
