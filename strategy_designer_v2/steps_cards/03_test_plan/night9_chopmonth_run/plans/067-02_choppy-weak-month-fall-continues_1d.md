---
idea: 067-02_choppy-weak-month-fall-continues
brief: 067_choppy-market-monthly-move-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a choppy market, a coin's 30-day return below zero, larger the fall -> kept: the 30-day return, zero when not negative, graded by the depth of the fall; the choppy profile is added by code.
- Comparison: none -> kept
- Outcome: the coin falls over the next 7 days, more after bigger falls -> kept: a short graded by the fall, held 7 bars.
- Verdict transfer: yes: the forecast is exactly the depth of the 30-day fall, so the short side's 7-day result inside the choppy profile confirms or rejects the idea.
Forecast: The forecast is built from the 30-day percent return (`PriceEvolutionComponent`, period 30). It is standardised against its own past 60 values, then clipped at a maximum of 0. When the 30-day return is zero or positive, the forecast is 0 and the book is flat. When the return is negative, the forecast is negative (short), and its size grows in proportion to the depth of the fall, up to -20. Inside the choppy profile only, which code adds.
Config: 067-02_choppy-weak-month-fall-continues_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: The sample is the bars of a non-overlapping 7-bar grid in each window where the forecast is below 0. On each of these bars, take the coin's 7-bar forward return minus the coin's mean 7-bar return over all windows, on the short side. Average it weighted by abs(forecast). The t is computed with the cases of one day taken together.
- Supporting check: On the same cases, the mean short-side unusual 7-bar move of the larger half of abs(forecast) minus that of the smaller half must be above 0.
- Confirm: The weighted mean short-side unusual move is above 0 with t >= 2, and the supporting check passes.
- Reject: The weighted mean short-side unusual move is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with the supporting check failing is also inconclusive. Fewer than 100 independent days with cases is inconclusive.
