---
idea: 060-01_falling-agitated-rally-fades-three-days
brief: 060_falling-agitated-scaled-rise-giveback
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a one-day rise in a falling, agitated market -> kept: the profile code keeps the book flat outside falling agitated, and the forecast is zero on days that did not rise.
- Comparison: the rise against the standard deviation of daily returns over the past 30 days -> kept: the return over 1 bar divided by the std of 30 one-bar returns, today's included.
- Outcome: a larger fall over the next 3 days, the larger the scaled rise -> kept: a short graded by the scaled rise, held 3 bars.
- Verdict transfer: yes: the short's gain over 3 days after scaled up days, growing with their size, is the idea's claim.
Forecast: The indicator is VolatilityScaledReturnComponent (period 1, vol_period 30). It gives the day's return in units of the 30-day daily-return std. It is standardised over its past 60 values (min 20), clipped at 0 so that down days give 0, then negated. The forecast is therefore 0 on down and flat days. On up days it is negative, a short. The short grows linearly with the rise in usual moves, up to the cap of -20. It is never positive. The profile code limits it to falling agitated bars.
Config: 060-01_falling-agitated-rally-fades-three-days_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move of the cases, measured in the short direction. A case is a short bet of at least 2 forecast points, read once per cell of the 3-bar grid. The unusual move is the coin's 3-bar return from the signal's close minus its normal 3-bar drift over all windows, signed for the short. Its t is computed with cases clustered by day.
- Supporting check: Across the cases, the slope of the short-signed unusual move on the case's absolute forecast must be positive, with t >= 2 (larger rises, larger giveback).
- Confirm: The main measure's t is >= 2 and the supporting check passes (slope t >= 2), before costs.
- Reject: The main measure's t is <= -2 (scaled up days are followed by returns above the normal drift), or the slope's t is <= -2.
- Inconclusive: Any result between those two cases, including a main t between -2 and 2, or a main t >= 2 with a slope t below 2. The test also needs at least 30 distinct case days; with fewer, the result is inconclusive whatever the t.
