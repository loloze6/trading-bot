---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the coin has fallen over the past 30 days -> kept: a regime rule on the 30-bar return, below 0.
- Comparison: the 30-day net move is small against the 30-day high-low range, and the smaller the more chop -> adapted: "small" becomes graded, so the short grows as net move / range falls below its usual size.
- Outcome: the coin keeps falling, beyond its normal drift, over the next 5 days -> kept: shorts are held 5 bars.
- Verdict transfer: yes: the fall, the chop ratio and the 5-day drift-adjusted fall are all measured as stated, and only the "small" threshold is graded.
Forecast: The forecast is active only on bars where the 30-bar return (PriceEvolutionOnPeriodComponent, 30) is below 0. It is flat on every other bar. On active bars, the chop ratio is |close[t] - close[t-30]| / (30-bar high - 30-bar low) (NetMoveToRangeRatioComponent, period 30, high_low). This ratio is standardised against its own past 60 values (about 10 at its usual size) and capped at 10. A constant offset of -10 is added, and the two are averaged. The forecast is therefore (min(ratio_std, 10) - 10) / 2. It is 0 when the net move is at or above its usual share of the range. It grows smoothly toward -5 (short) as the net move shrinks toward 0 against the range. It never goes long.
Config: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Each case is a short bet: a fall of the forecast of at least 2 points, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows, in the short direction. The measure is the mean of this unusual move over all coins, with its t.
- Supporting check: Take the active grid bars with forecast < 0. Regress the drift-adjusted 5-bar return on the forecast. The slope must be positive: a more negative forecast is followed by a lower return.
- Confirm: The mean unusual move in the short direction has t >= 2 over at least 30 independent cases, and the supporting slope is positive.
- Reject: The mean unusual move in the short direction has t <= -2 over at least 30 independent cases: choppy falls rebound beyond the drift.
- Inconclusive: Any t between -2 and 2, or a confirming t with a non-positive slope. Fewer than 30 independent cases is inconclusive whatever the t.
