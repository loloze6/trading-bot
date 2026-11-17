---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4692 USD
---
## Findings
- **F1:** The 7-day moves after a falling month run below the coin's own average, which the idea does not explain because it only says to stand aside there: on bars with a 30-day return at or below 0, the mean excess 7-bar return is -0.79 % (t -3.10, 2244 non-overlapping cases), against +0.83 % (t 2.66, 2157 cases) on the active bars.
- **F2:** Inside that falling-month state, the shortfall sits in the middle of the decline, not at its extreme. By per-coin quintile of the 30-day return, the mean excess 7-bar return is +0.48 % (t 0.59, n 314) for the deepest falls (median -33 %), -2.22 % (t -3.76, n 301) and -2.15 % (t -3.15, n 302) for falls with medians of -22 % and -15 %, and -1.06 % (t -1.58, n 308) for the mildest (median -3 %). The distance below the 60-day high gives the same shape: +0.81 % (t 1.10) at the deepest gap, -2.03 % (t -3.12) and -1.74 % (t -3.00) at gaps with medians of 36 % and 27 %.
- **F3:** The tested gain is concentrated at the very top of the range, not spread across it: among active bars, only the top quintile of the 365-bar range position earns a clear excess, +3.00 % over 7 bars (t 3.09, n 434), while the other four quintiles earn +0.08 % to +0.56 % (all t below 1). The top forecast quintile likewise earns +3.48 % (t 3.84) against -0.69 % to +0.81 % below it.
- **F4:** Over all bars, regardless of the 30-day regime, closeness to the 60-day high orders the next 7 days: the nearest quintile (median gap 0.8 %) earns +1.66 % excess (t 2.85, n 728), while the quintiles with median gaps of 25 % and 15 % earn -1.18 % (t -2.83) and -1.11 % (t -2.60).
- **F5:** The book's profit comes from long holdings and is lost on quick flips: trades lasting a median of 1 day average -3.9 % after fees with 13 % winners, and 3-day trades average -3.0 % with 24 % winners. Trades of a median of 38 days average +53.9 % with 86 % winners (about 950 trades per quintile).
- **F6:** The book earns less than holding the coins but much more smoothly: a mean daily return of 0.073 % against holding's 0.128 %, a Sharpe of 1.25 against 0.58, and a correlation of 0.62 with holding over 2898 days. The weekday and volume-ratio splits I looked at did not stand out once the cross-coin correlation and the number of angles are allowed for. The weekday t-statistics are not clustered by day, so I do not count them as findings.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling` (from F1, F2, F4): While a coin's 30-day return is negative, the further its close sits below its 60-day high, the lower its return over the next 7 days relative to its own average, through the range of ordinary declines.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g2_gain-sits-at-the-high` (from F3, F5): The closer a coin's daily close sits to its 52-week high while its 30-day return is positive, the higher its return over the next 7 days, with the gain rising steeply as the close reaches the high itself.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g3_nearness-to-60-day-high` (from F4, F1): The closer a coin's daily close sits to its 60-day high, the higher its return over the next 7 days, whatever its 30-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
