---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: "several times" made graded, so the touch count of the crossed 90-day swing-high level multiplies the close's margin above it (ResistanceBreakTouchCountComponent, period 90, cross_period 1).
- Comparison: a larger 20-day return before the break and more holds of the level give a larger rise; a flat or falling month is not a buy -> adapted: the 20-day return adds to the size, and a falling month (20-day return not above 0) is gated out by the regime.
- Outcome: price keeps rising over the next 5 days -> kept: each bet is held 5 daily bars and judged on the 5-bar return.
- Verdict transfer: yes: the forecast is long only on fresh closes above repeatedly-held 90-day levels after a rising month, and it grows with touches, margin and run-up, so its 5-day excess return confirms or rejects the idea directly.
Forecast: Each daily bar is in the trending regime only when the close has just crossed above a 90-day swing-high close level (the break reading is above 0) and the 20-day return is above 0. On all other bars the forecast is 0. In the trending regime the forecast is the equal-weight mean of two parts. The first is the break reading: the touch count of the level times the percent margin of the close above it, standardised over 90 bars. The second is the 20-day percent return, standardised over 60 bars and clipped at 0. The forecast is always positive in that regime and grows with more touches, a wider margin and a stronger run-up. It is never short.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move over the cases. A case is a long bet, meaning a rise of the forecast of at least 2 points. The unusual move is the coin's 5-bar return from the signal bar's close minus the coin's normal 5-bar drift (holding the coin), on non-overlapping 5-bar grid cells inside each window. Measured by the t of its mean.
- Supporting check: The slope of the cases' unusual move regressed on the forecast at entry is above 0, so a larger break after a larger run is followed by a larger rise.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2. Also a t of 2 or more with a slope at or below 0, or fewer than 30 cases, whatever the estimate.
