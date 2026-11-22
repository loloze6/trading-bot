---
idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 9111077ea370
---
Fidelity:
- Situation: the coin has risen over the past 30 days, then falls in an unbroken streak of 4h bars on declining volume -> adapted: "after the streak" made "while the streak lasts"; the 30-day rise above 0 and a down streak of 2 or more bars whose volume falls (least-squares slope) form a regime.
- Comparison: the larger its 30-day rise, the larger the rise that follows -> kept: inside the regime, the position grows with the 180-bar percent rise.
- Outcome: the coin rises over the next three days -> kept: 18 bars, long.
- Verdict transfer: yes: the regime is the idea's own condition, the size is its 30-day rise, and the outcome is the 18-bar return against the coin's drift.
Forecast: The regime is active on a bar when two things hold. The 180-bar (30-day) return is above 0. The bar closes a down streak of at least 2 bars, and volume fell across that streak (`DownStreakVolumeFadeComponent` above 0). On those bars the forecast is the 180-bar percent rise, standardised against its own past 180 values and clipped at 0, so it is long only and larger the larger the 30-day rise. On every other bar the forecast is 0.
Config: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The mean unusual move of the cases. A case is a bet: a rise of the forecast of at least 2 points, read once per 18-bar grid cell of each window. For each case, the unusual move is the 18-bar return from the signal's close minus the coin's normal 18-bar drift, which is its mean over all windows.
- Supporting check: Split the cases at the median forecast. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The main measure's mean is above 0 with t ≥ 2, over at least 30 cases, and the supporting check passes.
- Reject: The main measure's mean is below 0 with t ≤ -2, over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive main measure with t ≥ 2 whose supporting check fails is also inconclusive. Fewer than 30 cases is inconclusive whatever the t.
