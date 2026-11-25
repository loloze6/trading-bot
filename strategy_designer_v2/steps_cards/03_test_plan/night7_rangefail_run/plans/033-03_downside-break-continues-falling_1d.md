---
idea: 033-03_downside-break-continues-falling
brief: 033_range-position-predicts-drift
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin closes below its 20-day low -> kept: a regime is active only while the close is below the lowest low of the prior 20 days.
- Comparison: the further the close sits below that low -> kept: inside the regime, the short grows with the percent depth of the close under the prior 20-day low.
- Outcome: it falls over the next 5 days -> kept: the short is held for 5 daily bars.
- Verdict transfer: yes: the test shorts only closes under the prior 20-day low, sized by depth and held 5 days, so its result judges exactly that claim.
Forecast: The forecast uses DistanceFromHighComponent with period 20, source "high", extreme "low", exclude_current 1 and form "percent". Its value is (close − lowest low of the prior 20 days) / that low × 100. The same measure, in the regime detector, sends a bar to `trending` only when this value is below 0, which means the close is under the prior 20-day low. Every other bar is flat. Inside the regime, the measure is standardised against its own last 60 values and clipped at a maximum of 0. The forecast is therefore 0 at the low itself and grows more negative, smoothly, the deeper the close sits under the low. It is never positive.
Config: 033-03_downside-break-continues-falling_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are short bets, read on the non-overlapping 5-bar grid of each window. For each case, take the coin's 5-bar return from the signal close, minus the coin's mean 5-bar return over all windows, in the short direction. The measure is the mean of this excess fall, with its t (cases on the same day pooled into one).
- Supporting check: The mean excess fall of cases with |forecast| above the cases' median is larger than that of cases below the median.
- Confirm: The mean excess fall is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean excess fall is below 0 with t ≤ -2, meaning breakdowns are followed by rises beyond the drift.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a confirming t with a failed check. The test also needs at least 30 cases on at least 30 distinct days; with fewer, the result is inconclusive.
