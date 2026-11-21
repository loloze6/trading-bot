---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: "several times" becomes graded by the level's touch count times the close's margin above it, measured on the break bar.
- Comparison: only while the 60-day return is positive; the larger the 10-day return before the break, the larger the rise -> kept: the 60-day condition is a regime rule, and the position grows with the 10-day return.
- Outcome: the price keeps rising over the next 5 days -> kept: each bet is held 5 daily bars.
- Verdict transfer: yes: the test measures the 5-day rise after the idea's breaks, inside rising quarters, sized by the run-up.
Forecast: The regime is "trending" on bars where both of these hold; every other bar is flat. First, ResistanceBreakTouchCount (90 bars, side 2, band 2 %, cross 1 bar) is above 0: today's close crossed a swing-high close level. Second, the 60-day price change is above 0. On those bars the forecast is the equal-weight mean of two parts. One is the break strength (touches x percent above the level), standardised over 90 bars. The other is the 10-day return, standardised over 60 bars and clipped at 0. The forecast is long only and grows with the level's touch count, the break margin and the size of the 10-day run. It is zero away from a break, in a falling quarter, and from the run-up part after a falling fortnight.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Each case is a long bet, a rise of the forecast of at least 2 points, read once per 5-bar grid cell. For each case, take the coin's 5-day return from the case bar's close minus the coin's normal 5-day drift over all windows. Compute the mean over all cases, before costs, with its t.
- Supporting check: Across the cases, the slope of the unusual 5-day move on the case's forecast size is positive, with slope t >= 1.
- Confirm: The mean unusual 5-day move is above 0 with t >= 2 over at least 30 independent cases, and the supporting check passes.
- Reject: The mean unusual 5-day move is below 0 with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, or a confirming main measure whose slope check fails. Fewer than 30 cases pooled over all coins and windows is inconclusive whatever the t.
