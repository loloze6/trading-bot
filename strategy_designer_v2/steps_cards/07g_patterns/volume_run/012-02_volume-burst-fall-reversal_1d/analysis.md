---
line: 7.g patterns
backtest: 012-02_volume-burst-fall-reversal_1d
idea tested: 012-02_volume-burst-fall-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5515 USD
---
## Findings
- **F1:** On down days of any size, the next 3 days' excess return rises with the day's volume against its 30-day average. Pooled log-volume-ratio slope 0.0129, t 4.05, controlling for the fall's size, whose own coefficient is 0.0003 (t 0.16). Non-overlapping 3-day grid, 2023 cases.
- **F2:** The effect sits in the top fifth of volume among down days. Those cases gain +2.26% in excess over 3 days (t 4.35, n 405); the lower four fifths average between -0.19% and -0.38%.
- **F3:** Fall size does not gate the effect. The log-volume slope is positive for falls of 2 or more usual moves (0.032, t 3.02, n 157), for falls of 1 to 2 (0.043, t 4.28, n 373) and for falls under 1 (0.0076, t 2.24, n 1493). So the plan's sharp-fall gate threw away most of the signal.
- **F4:** The same volume ratio on up days predicts nothing. The slope is -0.0005 (t -0.27, n 2260), and the top volume fifth of up days averages -0.33%. The pattern is specific to heavy-volume selling.
- **F5:** The down-day volume effect is positive in all 6 coins: slopes 0.002 to 0.019, t from 0.38 for BTC to 2.41 for ZEC. It is positive in 7 of 8 years, with 2023 flat at -0.0001. It already shows over the next day: slope 0.0042, t 4.57, n 6478.
- **F6:** The brief's long lower wick does not add to the rebound. Among falls of 2 or more usual moves, the 3-day excess return falls with wick share (slope -0.022, t -0.85, n 432). The deepest-wick third averages -0.18%, against +0.74% for the shallowest.
- **F7:** The volume effect is concentrated where the coin's 20-day volatility is low or middling. On the 3-day grid, the log-volume slope is 0.0066 (t 2.64) and 0.0104 (t 3.35) in the lower two volatility terciles. It is -0.0014 (t -0.35) in the highest tercile, n about 1428 each.
- **F8:** One-day excess returns are higher on Thursdays and Fridays than on Mondays and Wednesdays in all 6 coins. The differences run 0.31% to 0.73% (Welch t 1.68 to 3.09), and the gap has the same sign in 7 of 8 years, all but 2022. This is a calendar effect, not a graded one, so no idea is written from it.

## Ideas
- `012-02_volume-burst-fall-reversal.g1_heavy-volume-down-day-rebound` (from F1, F2, F3, F4, F5, F6): On a day the coin closes lower, the larger that day's volume relative to its 30-day average volume, the larger the coin's rise over the next 3 days, whatever the size of the fall.
- `012-02_volume-burst-fall-reversal.g2_calm-market-volume-flush-rebound` (from F1, F7): While the coin's 20-day volatility is low or moderate, the larger a down day's volume relative to its 30-day average volume, the larger the coin's rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
