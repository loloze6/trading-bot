---
idea: 025-02_falling-market-bounce-fades
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: in a falling market, a coin's 3-day rise measured in its usual daily moves (30-day std of daily returns) -> kept
- Comparison: the larger the rise, the larger the fall, so larger rises are compared with smaller ones -> adapted: graded, the short position grows with the rise in usual moves
- Outcome: the coin falls over the next 5 days -> kept
- Verdict transfer: yes: the forecast is the idea's own measure, held only in falling markets over its 5-day horizon.
Forecast: VolatilityScaledReturnComponent (period 3, vol_period 30) gives the 3-day return divided by the 30-day std of daily returns (and by a constant sqrt 3). `standardise` (60/20) scales it against its own past values. `clip` with min 0 keeps only rises, and `negate` makes those rises a short. The forecast is 0 after a flat or falling 3 days. It is negative after a rise, and the short grows linearly with the rise's size in usual moves. It is never positive. The falling profile, added by code, keeps the book flat outside falling markets.
Config: 025-02_falling-market-bounce-fades_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Cases are bars on each window's non-overlapping 5-bar grid where the forecast is below 0. On each case, take the coin's 5-bar forward return minus its mean 5-bar return over all windows (holding the coin). Regress that excess return on the case's |forecast|. Report the slope's t, with the cases of one day pooled.
- Supporting check: The mean excess 5-bar return over the cases, in the short's direction (negated), is above 0.
- Confirm: The slope's t is -2 or less (larger rises are followed by larger excess falls) and the supporting check passes.
- Reject: The slope's t is +2 or more (larger rises are followed by larger excess rises).
- Inconclusive: A slope t between -2 and +2, or a confirming slope with a short-side mean of 0 or below. Fewer than 50 cases on the grid is also inconclusive.
