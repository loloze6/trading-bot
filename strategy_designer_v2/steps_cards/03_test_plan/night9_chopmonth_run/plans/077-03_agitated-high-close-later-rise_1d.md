---
idea: 077-03_agitated-high-close-later-rise
brief: 077_agitated-close-location-week-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 2e4516e62833
---
Fidelity:
- Situation: in an agitated market, a daily close near the top of that day's high-to-low range -> adapted: the profile is added by code; "near the top" is a regime condition at the common internal-bar-strength level, close location of 0.8 or more, and the position inside it is graded by how near the close is to the high.
- Comparison: larger the nearer the close sits to the day's high -> kept: the forecast grows with the close's place in the range inside the regime.
- Outcome: a rise from the end of the next day to the end of the seventh day -> kept: the situation is read with a one-bar lag, so the position opens at the next day's close and is held 6 bars.
- Verdict transfer: yes: the book holds long only after an agitated high close, from day 1's close to day 7's close, sized by the close's nearness to the high.
Forecast: Every bar is read through the close location of the previous day: (close − low) / (high − low) of bar t−1, from `CloseLocationInRangeComponent` with `reference` "low" and `lag` 1. When that value is below 0.8, the detector sends the bar to a flat regime and the forecast is 0. When it is 0.8 or more, the forecast is the same lagged close location, standardised against its own last 60 daily values (window 60, min_periods 20). This gives about 16 at 0.8 and 20 at a close on the high. It then passes through `signed_power` with exponent 2 and pivot 20, which spreads that band to about 13 to 20, so the long grows as the close nears the high. The forecast is never negative. Code adds the agitated profile, so the book is flat in calm markets. Each bet is held 6 bars, from the end of the next day to the end of the seventh day.
Config: 077-03_agitated-high-close-later-rise_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 6 bars
- Main measure: The mean unusual move over 6 bars per case, measured from the close of the signal's bar (the end of the day after the high close). The unusual move is the coin's 6-bar return minus its normal 6-bar drift (holding the coin), in the long direction. Its t is computed with the cases of each day taken together.
- Supporting check: The mean unusual move of cases whose lagged close location is 0.9 or more, minus that of cases between 0.8 and 0.9, is above 0.
- Confirm: The main measure is above 0 with t ≥ 2, and the supporting check is above 0.
- Reject: The main measure is below 0 with t ≤ −2.
- Inconclusive: Any other result, including a t between −2 and 2, or a positive main measure whose supporting check fails. The minimum is 100 cases falling on at least 50 distinct days; fewer is inconclusive.
