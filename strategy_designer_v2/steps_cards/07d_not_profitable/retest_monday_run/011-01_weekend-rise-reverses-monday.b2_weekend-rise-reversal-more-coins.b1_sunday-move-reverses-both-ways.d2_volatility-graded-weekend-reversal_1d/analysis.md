---
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4763 USD
---
## Findings
- **F1:** The book fails on its falls, not its gain. Its deepest fall is −23.7 % and lasts 903 days, against a yearly return of +12.3 %, so Calmar is 0.51. Inside that fall, the Sunday cases in the three lowest quintiles of s20/s60 lost −0.60, −0.55 and −1.18 (summed bar gains after costs), while the top two quintiles earned +0.32 and +0.78.
- **F2:** The reversal sits in the high-volatility-ratio cases. By quintile of s20/s60, the signed 2-day return is +0.76 % (t 2.6), +0.13 % (t 0.4), −0.18 % (t −0.5), +0.80 % (t 2.4) and +2.10 % (t 5.0), over about 520 cases each. The book's gain per case after costs is negative in the first three quintiles (−0.01 %, −0.06 %, −0.14 %) and +0.43 % and +1.25 % in the top two.
- **F3:** A rebuilt book that trades the Sunday bets only when s20/s60 is at or above its 60th percentile raises Calmar from 0.51 to 0.84. It does this by cutting the deepest fall from −23.7 % to −10.0 %, with Sharpe 0.90 against 0.74 and a yearly return of +8.3 %. At the 80th percentile, Calmar is 0.93 (fall −7.1 %, Sharpe 0.99, yearly return +6.7 %).
- **F4:** The volatility condition is not an effect of its own. On non-Sunday bars, betting against the 1-day move over the next 2 days earns −0.25 % (t −1.5, n 1490) in the lowest s20/s60 quintile and +0.20 % (t 1.0, n 1646) in the top one. Sunday cases in the top quintile earn +2.10 % (t 5.0). The weekend situation carries the effect, and the condition fits the theory: thin weekend books push price furthest when volatility has just risen.
- **F5:** The book's gain is concentrated in its strongest forecasts. The top quintile of |forecast| has a mean signed return of +1.36 % (t 4.9) and carries a summed gain of 10.0 out of about 14.8. The lowest quintile earns −0.12 at a mean allocation of 0.02.
- **F6:** Both sides lose in the deepest fall: short bets after weekend rises −0.88 and long bets after weekend falls −1.44. Both sides are positive over all cases (+0.79 %, t 5.1 and +0.56 %, t 3.8). Leaving out one side does not repair the falls.
- **F7:** The reversal is spread over both days, with 49 % of the signed 2-day move on Monday.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal.d1_weekend-reversal-in-rising-volatility` (from F1, F2, F3, F4, F6): A coin's Saturday-to-Sunday close-to-close return reverses over the next 2 days (Monday and Tuesday), only while its 20-day daily volatility is above its 60-day daily volatility. Within that state, the move back is larger the further 20-day volatility exceeds 60-day volatility.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal.d2_steep-volatility-graded-weekend-reversal` (from F2, F3, F5): A coin's Saturday-to-Sunday close-to-close return reverses over the next 2 days (Monday and Tuesday). The move back grows steeply, more than in proportion, with how far the coin's 20-day daily volatility sits above its 60-day daily volatility, so the largest reversals come in the cases where recent volatility is furthest above its norm.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
