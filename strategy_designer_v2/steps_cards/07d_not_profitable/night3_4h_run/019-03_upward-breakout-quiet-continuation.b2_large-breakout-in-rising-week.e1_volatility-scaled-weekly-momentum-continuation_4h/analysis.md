---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3738 USD
---
## Findings
- **F1:** The book fails on size. Per case over 3 days, the total move is +0.18 % and the unusual move +0.17 % (strength 0.017 against a usual move of 8.17 %, 5544 cases), while a buy and a sell cost 0.19 %. That is 0.9 times the cost, so the mean daily return is 0.00045 against the 0.0005 required, and the Sharpe of 0.41 trails holding's by 0.14.
- **F2:** The move is carried almost entirely by the strongest weeks. On the 18-bar grid, cases with forecast size above 10 gain +0.67 % over 3 days, net of drift in the signal's direction (n 2513). Cases with size 2 to 5 lose -0.31 % (n 835). Cases with size 5 to 10 gain +0.05 % (n 1355). So most of the bets placed on mid-sized weeks pay the cost for nothing.
- **F3:** The move outlasts the 3-day horizon. Strong-week cases (forecast above 10) gain +0.67 % net of drift over 3 days, +0.73 % over 6 days and +1.67 % over 12 days. For the top positive bucket alone the excess rise is +0.72 %, +0.94 % and +2.30 %. Holding 3 days captures under half of the move and pays the cost on each re-entry.
- **F4:** The effect exists only when the 30-day return points the same way as the 7-day signal. With agreement, the gain net of drift is +0.65 % over 3 days and +1.51 % over 12 days (n 2503). With disagreement, it is +0.05 % and -0.21 % (n 1349).
- **F5:** The short side earns nothing once the coins' drift is counted. Shorts have a total move of -0.13 % per case over 3 days, against +0.77 % for longs (about 2640 cases each). Summed short gains before costs are negative on BTC (-0.70), XMR (-0.94) and XRP (-0.84).
- **F6:** The deepest fall of the chained book is 63 %. It deepened steadily from w2 (-29 %) to w10 (-63 %), and in w4, w6 and w10 the coins rose (+0.28 %, +0.23 %, +0.40 % per day) while the book lost (-0.02 % to -0.06 % per day). Calmar is 0.14.
- **F7:** Trading leaves little after cost. Gross gain per unit traded is 13 to 52 bps on five coins and -5 bps on XMR, against about 9.5 bps paid per unit traded. Turnover is 0.19 to 0.34 of the book per coin per day.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation.d1_vol-scaled-week-rising-month` (from F1, F3, F4, F5, F6): The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days, only while its 30-day return is positive.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation.d2_extreme-weeks-carry-momentum` (from F1, F2, F3, F7): The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days, the rise growing faster than the return itself so that the strongest weeks for their volatility carry most of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
