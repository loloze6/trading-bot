---
idea: 077-01_agitated-high-close-week-rise
brief: 077_agitated-close-location-week-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a daily close near the top of that day's high-to-low range, in an agitated market -> adapted: "near the top" is made graded. The position is zero at or below mid-range and grows as the close nears the day's high. The agitated profile is added by code.
- Comparison: none -> kept
- Outcome: a rise over the next 7 days, larger the nearer the close is to the high -> kept: 7 bars on daily bars, long side only.
- Verdict transfer: yes: the forecast is long exactly on upper-range closes, sized by nearness to the high, and held for the idea's 7 days.
Forecast: The forecast is the close's place in that day's range. It uses a 1-bar Donchian position on high/low: -20 at the day's low, 0 at mid-range, +20 at the day's high. This is standardised over its past 60 values and clipped at 0. The forecast is therefore 0 on any day closing in the lower half of its range. Above mid-range it is positive and grows linearly as the close nears the day's high, typically reaching about +10 to +20 at the very top. It is never negative, and code keeps it at 0 outside the agitated profile.
Config: 077-01_agitated-high-close-week-rise_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: Take the bars with forecast > 0, on the non-overlapping 7-bar grid of each window. For each, the coin's 7-bar forward return minus the coin's mean 7-bar return over all its windows, averaged weighted by the forecast. Its t is computed with cases of the same day taken together.
- Supporting check: On the same grid cases, the mean excess 7-bar return of the top third of positive forecasts minus that of the bottom third must be above 0.
- Confirm: The weighted mean excess 7-bar return is above 0 with t >= 2, and the supporting check is positive.
- Reject: The weighted mean excess 7-bar return is below 0 with t <= -2.
- Inconclusive: Any result with t between -2 and 2 is inconclusive, and so is a positive main measure whose supporting check fails. Fewer than 100 independent grid cases with forecast > 0 is also inconclusive.
