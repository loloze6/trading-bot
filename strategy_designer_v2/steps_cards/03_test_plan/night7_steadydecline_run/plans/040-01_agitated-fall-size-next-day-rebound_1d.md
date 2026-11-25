---
idea: 040-01_agitated-fall-size-next-day-rebound
brief: 040_agitated-big-fall-rebounds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: a coin's one-day fall in an agitated market -> kept: the profile line keeps the agitation, and the fall is the day's percent return, zero on up days.
- Comparison: none -> kept
- Outcome: a larger rise over the next day, growing with the fall -> adapted: the long position is graded by the fall's size and held for 1 bar.
- Verdict transfer: yes: the position grows with the day's fall only inside the agitated profile, so next-day gains that grow with it confirm the idea, and losses that grow with it reject it.
Forecast: The forecast uses one indicator, the day's own percent return (`PriceEvolutionComponent`, period 1 bar). It is standardised against its last 60 values, negated, then clipped at 0. It is positive only after a down day and grows in proportion to the size of that day's fall, about +10 for a fall of usual size and capped at +20. It is zero on up days and flat days. It is never negative, so the book is long only. The code adds the agitated profile, which keeps the book flat outside it.
Config: 040-01_agitated-fall-size-next-day-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-day excess return on the forecast, with its t. The excess return is close[t+1]/close[t] - 1 minus the coin's mean daily return over all windows. The sample is every bar with forecast > 0, within windows only.
- Supporting check: The book's timing gain must be above 0 before costs. The timing gain is its mean daily return minus its gain from the market's own rise.
- Confirm: The slope is positive with t ≥ 2 and the timing gain is above 0.
- Reject: The slope is negative with t ≤ -2, meaning bigger falls are followed by weaker next days or further decline.
- Inconclusive: Any slope t between -2 and 2 is inconclusive, as is a positive slope whose timing gain is not above 0. The test needs at least 100 bars with forecast > 0 across all coins and windows.
