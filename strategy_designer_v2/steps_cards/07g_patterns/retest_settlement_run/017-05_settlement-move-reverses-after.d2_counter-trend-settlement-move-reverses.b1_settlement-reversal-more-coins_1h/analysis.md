---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
idea tested: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5754 USD
---
## Findings
- **F1:** The biggest drops in a coin's 24 hours are followed by a rebound, and the rebound is the one move here that is larger than a trade's cost. On the 24-hour grid, in the bottom fifth of 24-hour falls, the next 24 hours run +0.141 of a usual 24-hour move above the drift (t 6.45, 3591 cases). Averaged across coins per day it is +0.106 (t 2.86, 934 days). It is positive in 7 of 8 years; 2022 is the exception at -0.053. The other four fifths of falls give +0.021 to -0.035. At roughly 5.4 % for a usual 24-hour move (from the 3.12 % 8-bar move), +0.141 is about 0.76 % per case, more than three times the 0.22 % trade cost.
- **F2:** The 24-hour reversal is concentrated where short-term volatility is high. In the top third of 24-hour over 168-hour volatility, the 24-hour return continues by -0.037 of a usual move (t -3.25, 11503 cases). In the bottom third it is +0.001 (t 0.15).
- **F3:** Sharp 2-hour falls also rebound, but by less than a trade costs. On the 8-hour grid, the bottom fifth of 2-hour returns is followed by +0.035 of a usual 8-hour move over 8 hours (t 4.49, 22037 cases). The other fifths give +/-0.014 or less. In money that is about 0.11 % per case, under the 0.22 % cost.
- **F4:** The tested reversal depends on the time of day, not on funding. A 2-hour move against the 24-hour trend is followed over 8 hours by:
- **F5:** The 08:00 continuation is negative in all 8 years, at t -1.5 to -4.5 in 7 of them; 2024 is +0.002. Measured as the size of the 2-hour move continuing, it is largest in the top third of 2-hour move size: +0.071 (t 4.35), against +0.042 and +0.019 in the lower two thirds. Over all 08:00 bars, without the trend condition, the 2-hour move does not continue (+0.009, +0.000, -0.006).
- **F6:** The book enters almost entirely at 07, 15 and 23 UTC. The 07 entries, which sit inside the morning continuation of F4, lose the most: -0.31 % net per trade over 24256 trades. The 15 entries lose -0.12 % over 20092 trades and the 23 entries -0.28 % over 23684.
- **F7:** The losses sit on the short side. Short trades lose -0.51 % before fees (34024 trades), while long trades gain +0.22 % (34438 trades). Before costs the book earns only 0.055 bp per coin-hour, against a yearly return of -16.1 %.
- **F8:** The 2 hours after 21:00 UTC rise by +0.056 of a usual 2-hour move. Averaged across coins per day the t is 3.78 (2917 days); all other 2-hour blocks give -0.001 (t -0.18). It is positive in 7 of 8 years (2022 -0.078) and in 19 of 19 coins, 15 of them with t above 1.9. At about 0.09 % per case it is below the trade cost.

## Ideas
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins.g1_deep-daily-fall-rebounds` (from F1, F2, F7): The larger a coin's fall over the past 24 hours, the higher its return over the next 24 hours, and this rebound is larger when the coin's volatility over the past day is high compared with its past week.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins.g2_morning-counter-trend-moves-continue` (from F4, F5, F6): During the hours from 03:00 to 11:00 UTC, a coin's 2-hour move that runs against its 24-hour trend keeps going the same way over the next 8 hours, and the larger that 2-hour move, the larger the continuation.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins.g3_us-hours-counter-trend-reversal` (from F4, F6): During the hours from 14:00 to 24:00 UTC, a coin's 2-hour move that runs against its 24-hour trend is given back over the next 8 hours, and the stronger the 24-hour trend, the larger the move back.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins.g4_sharp-short-fall-rebounds` (from F3, F7): The larger a coin's fall over the past 2 hours, the higher its return over the next 8 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
