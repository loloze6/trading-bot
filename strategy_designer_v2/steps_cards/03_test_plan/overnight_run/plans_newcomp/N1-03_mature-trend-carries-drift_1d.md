---
idea: N1-03_mature-trend-carries-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day SMA for more than about 20 consecutive bars -> adapted: the count of consecutive bars above SMA(200) is graded, not cut at 20, and the position grows with it.
- Comparison: the next 20-bar return against the coin's average 20-bar return -> kept.
- Outcome: price keeps rising over the next 20 bars, and does worse than average in the first 5–20 bars after a cross -> kept.
- Verdict transfer: yes: a longer stay above the SMA gets a larger long and a fresh cross gets almost none, so the age-to-return relation the idea claims is what gets tested.
Forecast: One indicator, MovingAverageAgeComponent with period 200 and max_bars 120 (the convention). Its value is +n after n consecutive closes above the 200-day SMA and -n after n below. It is standardised against its own past 320 values (min_periods 80), then clipped at 0, so the forecast is long only. Below the SMA the forecast is 0. Just after a cross it is near 0. It grows steadily with the age of the above-SMA episode and reaches the +20 cap at long ages (at or near 120 bars). It is never negative.
Config: N1-03_mature-trend-carries-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: For each bar, take the coin's forward 20-bar return minus its mean 20-bar return over all 24 windows pooled (the holding benchmark). Regress this excess return on the forecast, pooled across coins. Overlapping returns are counted once by using non-overlapping 20-bar blocks or HAC errors with 19 lags.
- Supporting check: On bars where the recorded age is 5 to 20, the mean forward 20-bar excess return should be below 0. This is the early-cross underperformance the idea claims.
- Confirm: The slope of the excess return on the forecast is positive with t ≥ 2. The position-weighted mean excess return is also above 0.
- Reject: The slope is negative with t ≤ -2, meaning older above-SMA episodes are followed by worse-than-average 20-bar returns.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive, including results near zero. The test needs at least 30 non-overlapping 20-bar blocks with forecast > 0 across all coins; with fewer, the result is inconclusive whatever t is.
