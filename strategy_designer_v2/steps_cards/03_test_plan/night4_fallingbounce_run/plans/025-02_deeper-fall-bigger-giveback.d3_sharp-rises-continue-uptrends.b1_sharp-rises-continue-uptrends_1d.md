---
idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a coin with a positive 90-day return has a day's rise measured against the standard deviation of its last 20 daily returns -> kept: a regime on the 90-bar return above 0, and the rise in 20-bar volatility units, clipped at 0.
- Comparison: up days that are only ordinary against that volatility versus rises of several usual daily moves -> adapted: on/off made graded, with a smooth dead zone that damps ordinary rises and lets several-move rises grow.
- Outcome: the coin rises over the next 10 days, more after larger rises -> kept: long only, held 10 bars.
- Verdict transfer: yes: the test measures the idea's own condition, its own size ratio and its own 10-day horizon, so its result is the idea's result.
Forecast: The regime is "trending" only while the coin's 90-bar return is above 0; every other bar is flat. In that regime the forecast is built in three steps: - The day's return divided by the standard deviation of the last 20 one-bar returns (VolatilityScaledReturnComponent, period 1, vol_period 20). - That value standardised against its 60 prior values, then clipped at 0, so down days give 0. - Then signed_power with exponent 2 and pivot 20, which is a smooth dead zone. An ordinary one-usual-move up day standardises to about 12 and gives about 7. A rise of several usual moves reaches the cap of 20 and stays 20. The forecast is never negative, and it grows with the size of the rise against volatility. Each bet is held 10 bars.
Config: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Each case is a rise of the forecast of at least 2 points, read once per non-overlapping 10-bar grid cell of each window. For each case, take the coin's 10-bar return from the signal bar's close minus the coin's mean 10-bar return over all windows (its unusual move). Compute the mean over the cases, with its t-statistic. This is before costs.
- Supporting check: Split the cases at the median forecast. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The mean unusual move has t ≥ 2 over at least 30 cases, and the supporting check is above 0.
- Reject: The mean unusual move has t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 with the upper-half minus lower-half difference at 0 or below, and any result from fewer than 30 cases.
