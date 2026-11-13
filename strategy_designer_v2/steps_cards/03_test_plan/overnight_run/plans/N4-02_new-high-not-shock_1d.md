---
idea: N4-02_new-high-not-shock
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a day whose close makes a new 20-day closing high -> adapted: an on/off condition held as a regime "while the close is the highest of the last 20 closes"
- Comparison: size of that breakout up day, ordinary or small versus outsized -> kept: the day's percent return, scaled against the coin's own last 60 daily moves
- Outcome: the rise over the next ten days is as large after small breakout days as after outsized ones -> adapted: the position holds only while the high holds, so the ten-day hold is dropped; the 10-bar forward rise is read from the price record
- Verdict transfer: yes: the test sets the 10-day rise after each new high against that day's size, which is the idea's claim.
Forecast: The forecast is zero unless the close is the highest close of the last 20 days. That condition comes from DonchianBreakoutComponent(20, sf 20) in the detector, read as a value of at least 19.99. On those bars the forecast is the day's one-bar percent return, PriceEvolutionComponent(period 1). It is standardised against the mean absolute size of the 60 daily moves before it. A breakout day of typical size gives about +10 (a 100 percent long position). An outsized day gives up to +20, and a small up day gives close to 0. The forecast is long only by construction, since a new closing high is always an up day. Position size grows linearly with how outsized the breakout day is.
Config: N4-02_new-high-not-shock_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On bars where the forecast is positive, compute each bar's 10-bar forward return minus the coin's mean 10-bar return over all windows together. Compare the mean of this excess return between the top and the bottom half of the forecast, pooled over coins. Use a t-statistic that counts overlapping 10-bar returns once, clustering breakout runs that lie within 10 bars of each other.
- Supporting check: Run an equivalence test (two one-sided t-tests) on the same top-minus-bottom difference against bounds of ±1 percentage point of 10-day return.
- Confirm: The difference has |t| < 2. Both one-sided tests against ±1 pp reach t ≥ 2, so the difference is shown to lie inside ±1 pp.
- Reject: The top-minus-bottom difference has t ≥ 2, meaning outsized days are followed by larger rises. Or it has t ≤ -2, meaning size subtracts. Either way, breakout size matters.
- Inconclusive: |t| < 2 but the equivalence tests do not both reach t ≥ 2. Any result with fewer than 100 independent breakout clusters across all coins and windows, or fewer than 40 per half, is also inconclusive.
