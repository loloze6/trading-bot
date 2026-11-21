---
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 0974d5467d9f
---
Fidelity:
- Situation: a 4h close below the lowest low of the preceding two days (12 bars), while the 30-day (180-bar) return is positive -> kept: a regime rule fires on bars where the close is below the prior 12-bar low and the 180-bar return is above 0.
- Comparison: the width of the two-day stretch against the coin's 30-day average 4h range -> kept: high-low of bars t-12..t-1 divided by the mean bar range over 180 bars, graded.
- Outcome: the coin rises over the next three days (18 bars), more when the stretch was wider -> kept: long, held 18 bars, sized by the width ratio.
- Verdict transfer: yes: the test measures the idea's own break, trend condition, width ratio and horizon.
Forecast: The forecast is zero unless two things hold on the bar. The first is that the 4h close is below the lowest low of the 12 bars before it. The second is that the 180-bar return is positive. On such bars the forecast is long. Its size is the stretch-width ratio: the high-low range of the prior 12 bars divided by the mean bar range over the last 180 bars. This ratio is standardised against its own past 180 values, so a stretch of usual width gives about +10 and a wider one up to +20. The forecast is never negative. Each bet is held for 18 bars.
Config: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Across all cases (forecast bets, one per 18-bar grid cell, all coins and windows pooled), take the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift (holding the coin). Measure its mean and the t of that mean.
- Supporting check: Split the cases at the median forecast at entry, which is the standardised width. The wider half's mean unusual move minus the narrower half's must be greater than 0 (Welch t > 0).
- Confirm: The mean unusual move is positive with t >= 2 and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 with a wider-minus-narrower difference that is not positive. At least 100 independent cases are required, otherwise the result is inconclusive.
