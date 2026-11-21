---
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days, after closing below it the day before -> adapted: the breakout is made graded as the touch count times the close's percent margin above the level. It is non-zero on the crossing bar only.
- Comparison: the more times it turned down there, the larger the rise -> kept: the touch count N of swing-high closes within 2 % of the level scales the forecast.
- Outcome: rises over the next 10 days -> kept: each bet is held for 10 daily bars.
- Verdict transfer: yes: the forecast is long exactly on closes through repeated swing-high closes, sized by their count, and held for the idea's 10 days.
Forecast: The forecast uses one component, ResistanceBreakTouchCountComponent (period 90, side 2, band 2.0, cross_period 1). On a bar whose close rises through a past swing-high close L, having closed at or below L the day before, it is N x (close - L) / L x 100. N is the number of 90-day swing-high closes within 2 % of L. It is 0 on every other bar. It is standardised against its own past 90 values, so it is long only and 0 when no level was just crossed. Its size grows with the number of past turns at the level and with the margin of the close above it.
Config: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The mean unusual move over the cases. A case is a forecast rise of at least 2 points, read once per 10-bar grid cell. The unusual move is the coin's 10-bar return from the case's close minus the coin's normal 10-bar drift (holding the coin), pooled over coins and windows, with Welch/one-sample t.
- Supporting check: Recompute N from the closes. The mean unusual move of cases with N >= 3 must exceed that of cases with N <= 2 (difference above 0).
- Confirm: The mean unusual move is above 0 with t >= 2 on at least 30 cases, and the supporting difference is positive.
- Reject: The mean unusual move is below 0 with t <= -2 on at least 30 cases.
- Inconclusive: Any t between -2 and 2, fewer than 30 cases, or a confirming main measure whose supporting difference is not positive.
