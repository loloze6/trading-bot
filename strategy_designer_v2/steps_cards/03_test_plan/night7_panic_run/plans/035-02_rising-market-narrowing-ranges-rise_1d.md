---
idea: 035-02_rising-market-narrowing-ranges-rise
brief: 035_calming-swings-lift-rising-coins
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a coin in a rising market, its last 14 days' mean daily high-to-low range low against the 90 days before -> kept: the rising market is the profile; the range ratio is read on every bar inside it and sizes the long.
- Comparison: mean daily range of the last 14 days vs the 90 days before them -> kept: MeanBarRangeRatioComponent(104, 14) gives L/Q = 14/104 + (90/104) x (prior-90 mean / last-14 mean), an exact increasing function of the idea's ratio.
- Outcome: the coin rises over the next 3 days, more so the calmer -> kept: a long sized by calmness, held 3 bars.
- Verdict transfer: yes: the forecast ranks and sizes bars by the idea's own ratio, inside the idea's own profile, over the idea's horizon.
Forecast: One component, MeanBarRangeRatioComponent with long_period 104 and short_period 14. It is the mean daily high-low range over the last 104 days divided by the same mean over the last 14 days, so it rises as the last 14 days quiet against the 90 before them. It is standardised over its past 104 values (min_periods 26), which gives about +10 at its usual level. The value is higher, up to 20, when the recent ranges are narrower than usual, and lower, toward 0, when they are wider. The forecast is always positive (long only) and grows smoothly with calmness. The profile code keeps the book flat outside rising markets.
Config: 035-02_rising-market-narrowing-ranges-rise_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the in-profile bars with forecast > 0, on each window's non-overlapping 3-bar grid. Each case is the coin's 3-day return minus that coin's mean 3-day return over all windows. Compare the cases in the top third of forecast (calmest) with those in the bottom third (widest), using Welch's t of top minus bottom.
- Supporting check: The mean excess 3-day return of the top-third cases is above 0.
- Confirm: The main measure needs Welch t >= 2 (top minus bottom), and the supporting check must also pass.
- Reject: Welch t <= -2 (bottom-third cases rise more than top-third cases).
- Inconclusive: Any t between -2 and +2, or a passing t with a failing supporting check. At least 100 grid cases per third are needed, otherwise the result is inconclusive.
