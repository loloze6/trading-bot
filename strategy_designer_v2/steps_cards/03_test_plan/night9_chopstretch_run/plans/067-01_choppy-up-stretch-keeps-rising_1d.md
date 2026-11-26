---
idea: 067-01_choppy-up-stretch-keeps-rising
brief: 067_choppy-average-stretch-carries-forward
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a choppy market, the close's stretch above its 20-day average, in 20-day standard deviations of daily returns -> kept
- Comparison: the stretch judged against the coin's own 20-day swing -> kept
- Outcome: the coin rises more over the next 10 days, the larger the stretch, on both sides -> kept
- Verdict transfer: yes: the forecast is the idea's own stretch, signed and graded, inside the choppy profile, held over its 10-day horizon.
Forecast: The forecast uses one indicator, `MovingAverageDistanceComponent` (SMA, period 20, base "usual_moves", vol_period 20). It reads (close − SMA20) / SMA20 / s20, where s20 is the standard deviation of the last 20 daily returns. That value is standardised over its last 60 values, with at least 20 needed. The forecast is positive when the close is above its 20-day average and negative when below. Its size grows linearly with the stretch, up to the ±20 cap. It is zero at the average. There is no other gate: step 3's code adds the choppy profile and keeps the book flat outside it.
Config: 067-01_choppy-up-stretch-keeps-rising_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window, on bars where the forecast is not 0 (inside the choppy profile). Regress the coin's next-10-bar return minus its normal 10-bar drift on the forecast. The drift is the coin's mean 10-bar return over all windows. Report the slope's t, with cases on the same date summed together.
- Supporting check: Split the cases into longs (forecast > 0) and shorts (forecast < 0). On each side, the mean excess return taken in the forecast's direction must be positive.
- Confirm: The slope's t is 2 or more, and the supporting check is positive on both the long side and the short side.
- Reject: The slope's t is −2 or less: larger stretches are followed by a return toward the average.
- Inconclusive: Any of these counts as inconclusive: - a slope t between −2 and 2; - a slope t of 2 or more but with one side's mean not positive; - fewer than 100 grid cases in total, or fewer than 30 on either side.
