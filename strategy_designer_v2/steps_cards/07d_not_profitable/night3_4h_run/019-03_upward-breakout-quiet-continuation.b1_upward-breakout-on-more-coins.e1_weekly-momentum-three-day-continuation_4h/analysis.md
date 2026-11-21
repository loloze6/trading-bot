---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4663 USD
---
## Findings
- **F1:** The check failed on Calmar (0.65 against 0.75). The deepest fall is 35.2 % over 206 days, running from w21 to w23, while holding the coins fell 42.7 % over the same stretch. Every window from w4 to w24 has a fall of 13 to 35 %.
- **F2:** In each of the four deepest falls, both the long and the short bars lost money. In the deepest fall the longs lost 4.0 bps per bar over 10797 bars and the shorts 1.7 bps per bar over 12643 bars. The book is caught on both sides when the market turns.
- **F3:** On the 18-bar grid, the idea's move depends on whether the forecast agrees with the coin's 30-day return. Where they agree, the move beyond the drift is +73.7 bps for longs in a 30-day rise (t 3.58, 2968 cases) and +58.0 bps for shorts in a 30-day fall (t 3.65, 2902 cases). Where they disagree, it is −34.0 bps for longs in a 30-day fall (t −1.68, 1661 cases) and +20.7 bps for shorts in a 30-day rise (t 1.03, 1564 cases).
- **F4:** The agreement effect is graded. Ranked by how far the 30-day volatility-scaled return agrees with the forecast's side, the move beyond the drift by quintile is −25, 0.3, 96.5, 55.5 and 70.9 bps (t −1.33, 0.01, 3.98, 2.47, 2.89; about 1820 cases each).
- **F5:** The size explains why the gain is thin. Over all cases the move is 18 bps against a 22 bps round trip (0.8 times the cost). The agreeing cases carry 58 to 74 bps beyond the drift, about 2.6 to 3.3 times the cost, and 126 bps of total move for longs in a 30-day rise.
- **F6:** The book's bars show the same split. Longs in a 30-day rise earn 4.39 bps net per bar (55535 bars), while longs in a 30-day fall lose 0.37 bps (29644 bars). Shorts in a 30-day rise lose 1.60 bps (27445 bars) and shorts in a 30-day fall earn only 0.03 bps (55313 bars). Across all shorts the net is −0.89 bps per bar, against +2.52 bps for longs.
- **F7:** The gain sits in the top forecast quintile, at 5.40 bps net per bar. Quintiles 0 to 2 lose 0.33 to 0.71 bps per bar, after fees of 0.18 to 0.48 bps per bar.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation.d1_weekly-momentum-with-monthly-agreement` (from F1, F2, F3, F4, F5, F6): The larger a coin's return over the past 7 days, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift, only while its return over the past 30 days points the same way as its 7-day return.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation.d2_weekly-momentum-in-monthly-uptrends` (from F2, F3, F5, F6, F7): The larger a coin's return over the past 7 days, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift, only while its 30-day return is positive.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation.d3_aligned-week-and-month-momentum` (from F3, F4, F5, F6): The more a coin's 7-day and 30-day returns, each measured against its 30-day volatility, both point up, the more the coin rises over the next three days, by more than its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
