---
idea: N1-09_below-falling-long-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close below its 200-day average, and the average falling steeply over the past few weeks -> adapted: "below" is a regime; "steeply" is graded by the 20-bar slope, short side only, with a strong dead zone.
- Comparison: falls by more than its usual drift -> kept: judged against the coin's mean return over all windows together.
- Outcome: keeps falling over the next 10 days -> adapted: holding period dropped; the short is held while the situation lasts, and the result is read at 10 bars.
- Verdict transfer: yes: the test shorts only below the 200-day SMA, more as its fall steepens, and judges the 10-bar fall against usual drift.
Forecast: The regime detector reads the percent distance of the close from its 200-day SMA. When that distance is below 0, the bar is "trending"; otherwise it is flat. In the active regime the forecast comes from the 20-bar percent slope of the 200-day SMA. That slope is standardised over 220 bars and clipped at 0, so only a falling average counts. It then goes through signed_power with exponent 3 and pivot 10, so a mild decline gives almost nothing and a steep one gives a large short. The forecast is zero above the average, or when the average is flat or rising. It is negative and grows with the steepness of the fall below the average, and it never goes above 0.
Config: N1-09_below-falling-long-average_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On active bars, take −forecast/10 × (the coin's 10-bar forward return − the coin's mean 10-bar return over all windows together). Sample one bar in 10 per coin and window, so returns do not overlap, pool them, and test the mean with a t-test.
- Supporting check: The mean 10-bar forward excess return (forward return minus that same all-window mean) on the top quartile of |forecast| bars, non-overlapping, should be negative.
- Confirm: The main-measure mean is above 0 with t ≥ 2 over at least 30 non-overlapping active cases. The supporting check is negative.
- Reject: The main-measure mean is below 0 with t ≤ −2 over at least 30 non-overlapping active cases: the steep-decline shorts lose against usual drift.
- Inconclusive: Any t between −2 and 2, including a mean near zero, or fewer than 30 non-overlapping active cases, neither confirms nor rejects.
