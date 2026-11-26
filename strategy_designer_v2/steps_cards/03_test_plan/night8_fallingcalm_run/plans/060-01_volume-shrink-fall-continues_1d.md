---
idea: 060-01_volume-shrink-fall-continues
brief: 060_volume-dry-up-extends-downtrends
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: in a falling market, how much 30-day volume has shrunk against the prior 30 days -> adapted: the falling market is the brief's profile; the shrinkage is graded, and the position is zero where volume grew.
- Comparison: the 30 days of volume before the past 30 -> kept: the mean volume of bars t-29..t against the mean of bars t-59..t-30, as a log ratio.
- Outcome: a larger fall over the next 5 days -> kept: the 5-bar forward return, held short for 5 bars.
- Verdict transfer: yes: the test measures this shrinkage against this base, in this profile, over this horizon and on this side.
Forecast: One component, `VolumeRatioComponent`, with `period` 30, `short_period` 30, `exclude_current` 30 and `form` "log". Its raw value is ln(mean volume of the last 30 days / mean volume of the 30 days before them). It is negative when volume has shrunk and more negative the more it has shrunk. It is standardised over its own past 60 values, which keeps the sign and puts it on the forecast scale. It is then clipped at a maximum of 0. The forecast is therefore negative (short) and grows in size with the shrinkage, reaching -20 at the cap. It is 0 whenever volume has not shrunk, and it is never long. The code's falling profile keeps the book flat outside a falling market.
Config: 060-01_volume-shrink-fall-continues_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is every in-profile bar on the non-overlapping 5-bar grid of each window, including the bars where the forecast is 0. On it, take the slope of the coin's excess 5-bar forward return on the forecast. The excess return is close[t+5]/close[t] - 1 minus that coin's mean 5-bar return over all its windows. The slope's t is computed with the cases of one day taken together.
- Supporting check: The cases are grid bars with a forecast of -2 or less, which are shrinking volume. Their mean excess 5-bar return minus that of in-profile grid bars with a forecast of 0, which are growing volume, must be below 0.
- Confirm: The slope is positive with t ≥ 2, so larger shorts are followed by lower excess returns, and the supporting check is below 0.
- Reject: The slope is negative with t ≤ -2, so larger shorts are followed by higher excess returns.
- Inconclusive: The idea is neither confirmed nor rejected when: - the slope's t is between -2 and 2, or - the slope confirms but the check is not below 0. The minimum is 60 in-profile grid bars, of which at least 30 have a forecast of -2 or less, spread over at least 20 distinct days. With fewer cases the test is inconclusive.
