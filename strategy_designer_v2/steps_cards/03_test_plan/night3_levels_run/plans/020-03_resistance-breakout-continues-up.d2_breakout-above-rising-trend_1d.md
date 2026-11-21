---
idea: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days, while the close is above its 50-day average -> kept: a fresh close-cross of a 90-day swing-high level, at least 2 turns clustered within 2% just below the close, and close above SMA50, all as a regime rule.
- Comparison: the further above the 50-day average, the larger the rise -> kept: the position grows with the percent distance of the close above its 50-day SMA.
- Outcome: keeps rising over the next 5 days -> kept: each bet is held 5 daily bars and judged on the 5-day return above the coin's normal drift.
- Verdict transfer: yes: the test buys exactly these breaks above a trending average, sized by that distance, and measures the next 5 days.
Forecast: The regime is "trending" only on a bar that meets three conditions. The close has just crossed upward a 90-day swing-high close level (ResistanceBreakTouchCount, period 90, side 2, band 2%, cross 1 bar, above 0). At least 2 swing highs cluster within 2% of the highest swing-high price below the close (SwingHighClusterCount, period 90, side 2, band 2%, level "below", count, 2 or more). The close is above its 50-day SMA. Every other bar is flat. On a trending bar, the forecast is the percent distance of the close above its 50-day SMA, standardised against its own past 60 values (window 60, min 20) and clipped at 0. It is long only and grows continuously with that distance, near +10 at a usual distance and up to +20. Each bet is held for 5 bars.
Config: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The mean unusual move over the cases. A case is a long bet bar (the forecast rising at least 2 points on a trending bar), read once per 5-bar grid cell of each window. Its value is the 5-day return from the case's close minus the coin's normal 5-day drift over all windows. The test is a one-sample t on these values.
- Supporting check: Across the cases, the slope of the 5-day excess return regressed on the forecast at the case bar is positive (the larger the distance above SMA50, the larger the rise).
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 independent cases, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a slope of 0 or below is also inconclusive, and so is any result on fewer than 30 independent cases.
