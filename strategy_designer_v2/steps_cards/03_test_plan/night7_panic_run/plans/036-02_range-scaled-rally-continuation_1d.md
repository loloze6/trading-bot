---
idea: 036-02_range-scaled-rally-continuation
brief: 036_scaled-rallies-continue-next-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: f9d41455da54
---
Fidelity:
- Situation: a coin's 3-day return is large against its 30-day mean daily high-to-low range -> adapted: "large" made graded through a damped dead zone, so the position grows with the range-scaled 3-day rise and is zero for no rise.
- Comparison: the 3-day return against the average daily range of the past 30 days -> kept
- Outcome: the price keeps rising over the next 7 days, more after larger scaled rises -> kept
- Verdict transfer: yes: the forecast is the range-scaled 3-day rise itself, held for 7 days, so the result speaks for the idea in both directions.
Forecast: The forecast is the 3-day return divided by the 30-day mean daily range as a fraction of the close (`MeanAbsScaledReturnComponent`, period 3, window 30, base "mean_relative_range"). It is put on the forecast scale by `standardise` (60/20). It then goes through `signed_power` with exponent 2 and pivot 10, so ordinary rises are damped towards 0 and large ones are amplified. Last, it is clipped at a minimum of 0. The forecast is positive after a 3-day rise and grows with the square of the scaled rise, up to the +20 cap. It is zero after a flat or falling 3 days. It is never negative.
Config: 036-02_range-scaled-rally-continuation_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use the non-overlapping 7-bar grid of each window and keep the cells with forecast > 0. On those cells, take the slope of the coin's next-7-bar return minus its mean 7-bar return over all windows, regressed on the forecast. Report the slope's t.
- Supporting check: On the same cells, the mean of the next-7-bar return minus the coin's mean 7-bar return is above 0, with t ≥ 2. Cases on the same day are summed into one.
- Confirm: The slope's t is 2 or more, and the supporting check passes (mean excess return > 0 with t ≥ 2). There must be at least 100 cases.
- Reject: Either the slope's t is -2 or less, or the mean excess return has t of -2 or less. There must be at least 100 cases.
- Inconclusive: Any other result: a slope t between -2 and 2, or a positive slope with a mean-excess t under 2. Fewer than 100 positive-forecast grid cells across coins and windows is also inconclusive.
