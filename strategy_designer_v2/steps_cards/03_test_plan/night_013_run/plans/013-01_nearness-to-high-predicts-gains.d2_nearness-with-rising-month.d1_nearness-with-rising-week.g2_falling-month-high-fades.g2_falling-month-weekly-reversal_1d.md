---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's 30-day return is negative -> kept: a regime rule on the 30-bar return below 0; other bars are flat.
- Comparison: the larger its 7-day return -> kept: the 7-bar return, graded, sets the position's size.
- Outcome: lower return over the next 7 days, falling as the bounce grows -> kept: a short position that grows with the 7-bar return, judged over 7 bars.
- Verdict transfer: yes: the config holds the exact condition and the graded relation, so a confirm or a reject carries back to the idea.
Forecast: On each daily bar, the regime detector computes the 30-bar return (PriceEvolutionComponent, period 30). When it is below 0, the bar is `mean_reversion`; otherwise it is `unknown`, and the forecast is 0 (flat). In `mean_reversion`, the forecast uses the 7-bar return (PriceEvolutionComponent, period 7). Standardise divides it by its mean absolute value over the previous 60 bars and scales it so that value maps to 10, capped at ±20. The result is then negated. So a 7-day bounce in a falling month gives a short position that grows with the bounce. A 7-day fall in a falling month gives a long position that grows with the fall. A flat week gives about 0. The position jumps from flat only when the 30-day sign condition switches on or off, which is the idea's own condition.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Take the non-overlapping 7-bar grid of each window (positions 0, 7, 14, ...). Keep the grid bars whose `regime` is `mean_reversion`. On those bars, regress the coin's 7-bar forward return on the `forecast`, pooled over coins and windows. The forward return is measured minus that coin's mean 7-bar return over all its windows. The measure is the slope's t-statistic.
- Supporting check: The book's mean daily timing gain must be above 0. This is the book's mean daily return before costs minus its gain from the market's own rise.
- Confirm: The slope has t ≥ 2 and the supporting check passes. A positive slope means a larger negated 7-day return comes before a higher excess return, so a larger bounce comes before a lower one.
- Reject: The slope has t ≤ -2: larger bounces in falling months come before higher excess returns.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive, including estimates near zero. So is t ≥ 2 when the timing gain is not above 0. The test needs at least 100 independent grid cases in `mean_reversion`, pooled across coins; with fewer, the result is inconclusive.
