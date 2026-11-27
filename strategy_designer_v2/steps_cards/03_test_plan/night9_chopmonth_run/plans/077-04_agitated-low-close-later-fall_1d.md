---
idea: 077-04_agitated-low-close-later-fall
brief: 077_agitated-close-location-week-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 2e4516e62833
---
Fidelity:
- Situation: a daily close near the bottom of that day's high-to-low range, in an agitated market -> adapted: the day's close location (0 at the high, 1 at the low) is a regime condition at 0.75 or more, the usual bottom-quarter convention; inside it the forecast is graded; the agitated profile is added by code.
- Comparison: none -> kept
- Outcome: a fall from the end of the next day to the end of the seventh day, larger the nearer the close is to the low -> kept: the reading is lagged one bar, so the short opens at the next day's close and is held for 6 bars.
- Verdict transfer: yes: the test shorts exactly these closes over exactly that stretch, so a confirm or a reject of the test is one of the idea.
Forecast: The forecast uses the close location of the previous day: (high − close) / (high − low), read at lag 1. That value is 0 at the day's high and 1 at its low. A position exists only while that previous-day location is 0.75 or more, meaning the close sat in the bottom quarter of the range, and only inside the agitated profile. On those bars the location is standardised against its own past 60 values, with 20 at minimum, and negated. The forecast is therefore short, about −15 at the 0.75 edge and growing to about −20 at a close on the low. On every other bar the forecast is 0. It is never positive. Each short opens at the next day's close and is held for the 6 bars to the seventh day's close.
Config: 077-04_agitated-low-close-later-fall_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 6 bars
- Main measure: The unusual move of each case. A case is a short bet, meaning a fall of the forecast below 0 by at least 2 points, read once per cell of the 6-bar grid. Its move is the 6-bar return from that bar's close, minus the coin's mean 6-bar return over all windows, taken in the short direction. Its t takes the cases of one day together.
- Supporting check: The cases are split at the median of |forecast| at entry. The upper half's mean unusual move minus the lower half's must be above 0.
- Confirm: The mean unusual move must have t ≥ 2 and the supporting difference must be above 0.
- Reject: The mean unusual move has t ≤ −2, meaning the coin rises more than its drift after low closes.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is a t ≥ 2 whose supporting difference is not above 0. The test needs at least 30 distinct case days; fewer is inconclusive.
