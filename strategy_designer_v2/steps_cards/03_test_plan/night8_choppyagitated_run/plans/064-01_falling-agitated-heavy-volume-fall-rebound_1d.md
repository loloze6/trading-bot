---
idea: 064-01_falling-agitated-heavy-volume-fall-rebound
brief: 064_falling-agitated-heavy-volume-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a down day, in a falling agitated market, on volume above the coin's own 20-day average -> kept: a regime rule requires a negative one-day return and a volume ratio to the prior 20 days above 1; the profile is added by code.
- Comparison: that day's volume against the coin's 20-day average volume -> kept: the forecast grows with volume / 20-day mean − 1.
- Outcome: a larger rise the next day, larger the heavier the volume -> kept: each bet is held 1 bar, and next-day excess return is read against forecast size.
- Verdict transfer: yes: the book is long only on heavy-volume down days in the profile, sized by relative volume, so the record can confirm or reject the next-day rise and its growth with volume.
Forecast: The forecast is active only on a down day (1-day return below 0) whose volume is above the mean of the prior 20 days' volumes. The profile vetoes keep it inside falling agitated. On those bars the forecast is the volume ratio minus 1, standardised (window 60, min_periods 20) and clipped at 0. It is long only. It starts at 0 when volume just equals its average and grows with how much heavier the day's volume is. On every other bar it is 0 (flat).
Config: 064-01_falling-agitated-heavy-volume-fall-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Over the case bars (forecast > 0, the regime `mean_reversion`), take each case's excess next-day return: close[t+1]/close[t] − 1 minus the coin's mean daily return over all its windows. Regress it on the forecast, within windows. Compute the slope's t with cases grouped by day: cases on several coins the same day count as one.
- Supporting check: On the same cases, the mean excess next-day return is above 0. Its t is also computed with cases grouped by day. This is before costs.
- Confirm: Both of these hold: - the slope's t is 2 or more; - the mean excess next-day return is above 0.
- Reject: Either of these holds: - the slope's t is −2 or less; - the mean excess next-day return has a t of −2 or less (heavy-volume falls keep falling).
- Inconclusive: Any other result is inconclusive. This includes a slope t between −2 and 2, and a positive slope with a mean excess at or below 0 whose t is above −2. It is also inconclusive with fewer than 100 distinct case days across all coins and windows.
