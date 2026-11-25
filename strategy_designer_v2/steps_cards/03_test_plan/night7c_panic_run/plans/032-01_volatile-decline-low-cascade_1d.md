---
idea: 032-01_volatile-decline-low-cascade
brief: 032_monthly-low-in-volatile-decline
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 051b3422f169
---
Fidelity:
- Situation: a coin down over 30 days, with wide daily ranges over the month against its past year, closes below its prior 30-day low -> kept: a regime holds the three conditions together: the 30-day return below 0, the 30-day mean bar range above the 365-day mean, and the close below the prior 30-day low.
- Comparison: the close against the lowest low of the prior 30 days, and the further below it the larger -> kept: the forecast is graded by the close's percent depth under that low.
- Outcome: a further fall over the next 5 days, larger the deeper the break -> kept: a short position held 5 bars, sized by the depth.
- Verdict transfer: yes: the book is short only in the idea's situation, sized by the break depth, and is judged on the 5-day move against the coin's drift.
Forecast: Three conditions must all hold, or the book is flat: - the 30-day close-to-close return (`PriceEvolutionOnPeriodComponent`, 30) is below 0; - the mean daily high-low range of the last 30 bars is wider than that of the last 365 bars (`MeanBarRangeRatioComponent`, long 365, short 30, below 1); - the close is below the lowest low of the prior 30 bars, bar t excluded (`DistanceFromHighComponent`, period 30, source "high", extreme "low", exclude_current 1, percent below 0). Inside the situation, the forecast is that same percent distance standardised over 60 bars (min 20). It is negative (short) and grows in size the deeper the close sits under the prior low. It is clipped at 0 from above, so it is never long. The standardise base is mostly the positive distances of ordinary bars, so shallow breaks give small forecasts and deep breaks give large ones.
Config: 032-01_volatile-decline-low-cascade_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets: the forecast falls by at least 2 points, read once per non-overlapping 5-bar grid cell. For each case, take the coin's 5-day return minus its normal 5-day drift over all windows, signed short. Report its mean and t, with same-day cases taken together.
- Supporting check: Split the cases at the median absolute forecast. The deeper half's mean short-signed unusual move minus the shallower half's must be above 0.
- Confirm: The mean short-signed unusual move is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean short-signed unusual move has t <= -2, meaning the coin rises more than its drift after the break.
- Inconclusive: Any t between -2 and 2. Also t >= 2 with the depth check failing. Also fewer than 30 distinct case days across all coins and windows.
