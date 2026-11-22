---
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
idea tested: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4223 USD
---
## Findings
- **F1:** The tested idea finds nothing in the bars: its 14681 cases end 24 hours later +0.01 % above drift (t 0.21), its top half does worse than its bottom half (-0.002 %), and the hours it bets on most (a rise of more than 4 usual moves on more than 4 times the usual volume) are followed by -0.15 % over 2 hours (t -0.98, 459 cases) and -0.65 % over 24 hours (t -0.56, 43 cases).
- **F2:** A coin's 24-hour move reverses over the next 24 hours, and more so the larger it was: the unusual 24-hour move, in usual moves, falls by 0.039 for each usual move of the past 24 hours (t -4.5, 15086 non-overlapping cases); the slope is negative in all six coins (t from -0.76 for BTC to -3.58 for XMR) and in 7 of 8 years.
- **F3:** The reversal in F2 sits mostly after falls: the decile with the largest 24-hour fall is followed by +0.83 % above drift over 24 hours (t 5.05, 1509 cases), and the decile with the largest rise by -0.31 % (t -2.24); the bottom quintile is positive in every coin (+0.31 % BTC to +0.78 % XRP); a 72-hour past move predicts nothing (slope +0.007, t 0.75).
- **F4:** An hour falling more than 2.5 usual moves is followed by a rebound over the next 2 hours, and the larger its fall times its volume ratio, the larger the rebound (slope t 3.24, 2515 cases). Falls of more than 4 usual moves on more than 4 times the usual volume are followed by +0.65 % (t 3.15, 472 cases). The rebound is positive in all six coins (ZEC +0.59 %, t 3.68; XRP +0.39 %, t 2.66; BTC +0.04 %) and in 7 of 8 years. Rises of the same size are followed by -0.03 % (t -0.68, 2597 cases).
- **F5:** Calendar patterns stand out but are not graded. 24 hours from a Friday bar end +0.52 % above drift (t 5.0, 2158 cases), positive in all six coins and in 6 of 8 years. The 2 hours from 20:00 UTC end +0.07 % (t 5.43), below the cost of a trade of 0.19 %. Monday and Thursday are followed by about -0.35 % (t near -2.96).
- **F6:** The book's trades do not grow with the entry forecast: the mean gross trade is +1.23 % in the lowest quintile and +0.21 % in the fourth (forecast 20). The book trails holding in LTC (-0.0000 vs +0.0007 a day) and XMR (-0.0004 vs +0.0011 a day), and its Sharpe trails holding's by 0.05.

## Ideas
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins.g1_daily-move-reverses-next-day` (from F2, F3, F1): The more a coin has fallen over its past 24 hours, measured in its usual 24-hour moves over the past 30 days, the more it rises over the next 24 hours; the more it has risen, the more it falls.
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins.g2_heavy-volume-hourly-fall-rebounds` (from F4, F1): After an hour in which a coin falls far more than its usual hourly move over the past 30 days, the price rises over the next 2 hours, and more the larger that hour's fall times its volume relative to its 30-day average hourly volume.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
