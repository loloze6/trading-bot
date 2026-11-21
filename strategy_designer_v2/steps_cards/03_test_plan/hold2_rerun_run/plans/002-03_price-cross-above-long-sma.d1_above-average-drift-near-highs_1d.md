---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its long moving average, near its recent high, after a strong recent rise -> kept: a regime on close at or above SMA(200), with the 20-day range position and the 20-day rise both graded
- Comparison: drift larger the closer to the high and the stronger the rise, fading on pullbacks -> kept: the long position grows with the range position and the rise, and shrinks towards 0 as the close falls from its high
- Outcome: price keeps drifting upward while above the long average (no horizon stated; convention 20 daily bars) -> adapted: "while above" is held as the regime, and no holding period is set
- Verdict transfer: yes: the forecast is the idea's graded long, so gains rising with its size confirm the idea and losses rising with its size reject it
Forecast: When the close is at or above its 200-day SMA (regime `trending`), the forecast is the equal-weight mean of two standardised (60/20) parts, each clipped at 0. The first is where the close sits in its 20-day close range: positive in the upper half, largest at the 20-day high. The second is the 20-day percent rise: positive when price rose. The forecast is long only and runs from about 0 to 20. It grows as the close nears its 20-day high and as the 20-day rise strengthens. It falls towards 0 as the close pulls back from its high. It is exactly 0 (flat) whenever the close is below its 200-day SMA.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: On a non-overlapping 20-bar grid in each window, the forward 20-bar return minus the coin's mean 20-bar return over all windows is regressed on the forecast at t. The measure is the t of the slope, pooled over coins and windows.
- Supporting check: The book's timing gain must be above 0. This is its mean daily return minus its gain from the market's own rise, before costs.
- Confirm: The slope t is 2 or more and the timing gain is positive.
- Reject: The slope t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A slope t of 2 or more with a timing gain of 0 or less is also inconclusive. At least 100 grid cases with forecast above 0 are needed, and about 860 cases in total; with fewer, the result is inconclusive.
