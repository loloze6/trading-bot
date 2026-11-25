---
idea: 038-02_rising-market-range-scaled-continuation
brief: 038_scaled-rallies-continue-in-rising-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f9d41455da54
---
Fidelity:
- Situation: a coin's 3-day return, in units of its average daily high-low range over the last 30 days, in a rising market -> kept (rising market is the brief's profile, added by code)
- Comparison: larger scaled rises versus smaller ones, and flat or down coins getting no lift -> kept: the position grows with the scaled rise and is 0 when the 3-day return is 0 or negative
- Outcome: the coin keeps rising over the next 3 days, more for larger scaled rises -> kept
- Verdict transfer: yes: the forecast is the idea's scaled 3-day rise, held for 3 days inside the rising profile, so a confirm or a reject of its link to the next 3-day return is a confirm or a reject of the idea.
Forecast: One component, `MeanAbsScaledReturnComponent` with period 3, window 30 and base "mean_relative_range". It reads the coin's 3-day return divided by its 30-day mean daily range (high minus low over the close). The value is standardised against its past 60 values, so a usual size reads about 10, capped at 20. It is then clipped at 0. The forecast is positive after a 3-day rise and grows linearly with the rise counted in usual daily ranges. It is 0 when the last 3 days were flat or down. It is never negative. The rising-market profile is added by code, so the book is flat outside rising markets.
Config: 038-02_rising-market-range-scaled-continuation_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The sample is the non-overlapping 3-bar grid of each window, using only bars where `scaled_rise` is recorded (in-profile bars). On those bars, take the slope of the coin's 3-bar forward return, minus that coin's mean 3-bar return over all windows (holding the coin), regressed on the forecast. The t uses standard errors clustered by day.
- Supporting check: On grid bars with forecast > 0, the mean excess 3-bar return (as above) is above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes, with at least 100 grid bars with forecast > 0.
- Reject: The slope is negative with t ≤ -2, with at least 100 grid bars with forecast > 0.
- Inconclusive: Any slope with t between -2 and 2. Also a positive slope with t ≥ 2 whose supporting check fails. Also fewer than 100 grid bars with forecast > 0, whatever the t.
