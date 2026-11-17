---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4183 USD
---
## Findings
- **F1:** The book loses because its shorts pay the coins' own rise: the active short averaged -0.32 of the book (mean over all bars), which cost -0.000453 per bar from the coins' mean daily rise, while timing earned only +0.000415 per bar and fees took 0.000078, leaving a gain of -0.000042 per bar.
- **F2:** The losses sit in the deepest, fastest falls, where the coin bounces the next day:
- **F3:** On the 7-day grid in the falling month, the depth effect is not monotone, so the linear slope fails (t 0.86):
- **F4:** Leaving out the bars with a 30-day return below -30% turns the book's mean gain per active bar from -0.000082 (t -0.37, bar Sharpe -0.05, n 18804) into +0.000828 (t 3.13, bar Sharpe 0.55, n 11665). Leaving out the bars more than 45% below the high gives +0.000396 (t 1.66).
- **F5:** The worst 5% of bars came right after sharp drops, with the book more heavily short:
- **F6:** The short works only in calm coins: timing per bar falls from +0.0018 in the lowest 20-day-volatility quartile (2.3% daily) to -0.000001 in the highest (7.6% daily), and gain falls from +0.0006 to -0.0006.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling.d1_slow-slide-not-crash` (from F2, F3, F5, F1): While a coin's 30-day return is negative, the further its close sits below its 60-day high, the lower its return over the next 7 days relative to its own average, through the range of ordinary declines, except that the larger its 7-day loss, the more this weakness turns into a rebound over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling.d2_calm-decline-keeps-falling` (from F6, F1, F4): While a coin's 30-day return is negative, the further its close sits below its 60-day high, the lower its return over the next 7 days relative to its own average, through the range of ordinary declines, the more so the lower its 20-day volatility.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling.d3_crash-week-rebounds` (from F2, F3, F5): While a coin's 30-day return is negative, the larger its 7-day loss, the higher its return over the next 7 days relative to its own average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
