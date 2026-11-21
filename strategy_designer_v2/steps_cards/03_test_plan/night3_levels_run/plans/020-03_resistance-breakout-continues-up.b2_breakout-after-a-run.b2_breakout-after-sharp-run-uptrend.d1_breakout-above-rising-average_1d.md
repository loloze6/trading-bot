---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: "several" is made graded, as the crossed swing-high level's touch count times the close's margin above it (90 bars, on the bar of the break).
- Comparison: only while the 60-day return is positive and the close is above its 50-day average, and the further above that average the larger the rise -> kept: a regime gates on both, and the forecast grows with the percent distance above the 50-day SMA.
- Outcome: the price keeps rising over the next 5 days -> kept: each bet is held 5 bars and judged on the 5-bar return against the coin's drift.
- Verdict transfer: yes: the test buys exactly these breaks under these conditions, sized by distance above the average, and measures the 5-day rise that follows.
Forecast: The regime is "trending" only on a bar where three things hold: the close has just crossed above a 90-bar swing-high close level (ResistanceBreakTouchCount, side 2, band 2 %, cross_period 1, above 0), the 60-bar return is above 0, and the close is above its 50-bar SMA. On every other bar the forecast is 0. On a trending bar the forecast is the equal-weight mean of two standardised values. The first is the break's touch count times its percent margin. The second is the percent distance of the close above its 50-bar SMA. Both are positive in this regime, so the forecast is long only. It grows with the distance above the average and with how many times the level held. Each break is a bet held for 5 bars.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all its windows. A case is a bet bar, read once per 5-bar grid cell. The measure is the mean of these unusual moves over all coins, with the t of that mean.
- Supporting check: Across cases, the Spearman rank correlation between the case's forecast and its unusual move is above 0.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a rank correlation of 0 or below is also inconclusive. Fewer than 30 cases in total is inconclusive whatever the t.
