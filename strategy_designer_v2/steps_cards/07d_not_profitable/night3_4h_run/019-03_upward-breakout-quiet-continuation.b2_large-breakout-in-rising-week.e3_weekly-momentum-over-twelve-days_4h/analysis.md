---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3571 USD
---
## Findings
- **F1:** The short side is what sinks the book: on summed bar gains its short positions have a mean daily gain of -0.0485 % (Sharpe -0.48, deepest fall -92 %), while its long positions earn +0.082 % a day (Sharpe 0.76, Calmar 0.41 against the whole book's 0.018, deepest fall -61 % against -81 %).
- **F2:** Short signals do not even capture a move before costs: on the 72-bar grid the 766 short cases have a total move of -0.95 % in their direction, while the 637 long cases have +2.71 %; the idea's unusual move (+0.81 % for shorts) exists only because the coins' normal drift is upward.
- **F3:** The long side's gain is graded by the forecast's size: long grid cases by quartile of |forecast| move -0.89 %, +3.20 %, +3.13 % and +5.13 % over 72 bars, while short quartiles move -1.27 %, -3.73 %, +0.10 % and +1.18 % in their direction, so no grade holds there.
- **F4:** The book's gain sits in longs taken while the coin's 30-day return is positive: their bar gains sum to +13.35 (mean +0.046 % per bar, 29,013 bars), against -0.66 for longs against the 30-day trend and -5.03 for shorts against it; long grid cases with a positive 30-day return move +3.42 % over 72 bars (t 3.06, 321 cases).
- **F5:** Within longs in a rising 30-day trend, the gain grows with recent volatility against its 30-day level: the mean bar gain is +0.003 % in its quietest third, +0.017 % in the middle third and +0.109 % in the loudest third (about 10,000 bars each); on the grid, quiet-ratio cases move -0.27 % (t -0.28, 324 cases) and loud ones +2.26 % (t 1.96, 324 cases), the opposite of the brief's quiet-range premise.
- **F6:** The book's deepest fall is -81.5 % over 480 days from w12 to w16; its long side also lost in w12 to w15 (-0.13, -0.06, -0.50, -0.06 summed), and its shorts lost in every window from w10 to w18, so the fall is shorts plus longs held through a broad decline (w14: holding -0.52).
- **F7:** The book trails holding (mean daily return 0.033 % against 0.118 %, Sharpe 0.27 against 0.55), and a book keeping only the positions on the side of the 30-day trend reaches a mean of 0.068 % and a Sharpe of 0.67 before any further change.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days.d1_upward-weekly-momentum-in-uptrend` (from F1, F2, F3, F4, F6, F7): The larger a coin's 7-day rise, measured in units of its own 4h volatility, the more the coin rises over the next twelve days, only while its 30-day return is positive.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days.d2_loud-momentum-in-uptrend` (from F4, F5, F3): The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days, only while its 30-day return is positive, and the more so the higher its 3-day volatility of 4h returns stands above its 30-day volatility.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days.d3_widening-ranges-in-uptrend` (from F5, F4): The more a coin's 3-day volatility of 4h returns exceeds its 30-day volatility while its 30-day return is positive, the more the coin rises over the next twelve days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
