---
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h bar closes above the highest high of the preceding two-day stretch -> adapted: the close-above condition is made graded, as the size of the breakout above the prior 12-bar high (0 when there is none).
- Comparison: how narrow that stretch was against the coin's 30-day average 4h range -> kept: the 180-bar mean bar range divided by the 12-bar stretch range multiplies the breakout.
- Outcome: the coin rises over the next three days, more for a narrower stretch -> kept: each bet is held 18 bars and its size grows with the narrowness.
- Verdict transfer: yes: the component measures the idea's breakout, stretch and 30-day base exactly, and the book holds for the idea's horizon.
Forecast: NarrowRangeBreakoutComponent with period 12 (two days) and base_period 180 (30 days). It reads max(0, close − prior 12-bar high) / close × 100 × (180-bar mean bar range / prior 12-bar range). It is standardised over 180 past values (min_periods 45) and clipped at 0, so the forecast stays long only. The forecast is 0 on every bar without an upward close beyond the stretch's high. It is positive on a breakout bar, and larger the further the close clears the high and the narrower the stretch is against the 30-day average range. It never goes negative. Each breakout bet is held 18 bars.
Config: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Cases are bets: a rise of the forecast of at least 2 points, read once per 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the close of the signal bar, minus the coin's mean 18-bar return over all its windows (unusual move). The measure is the mean of these unusual moves over all cases, with its t of the mean.
- Supporting check: Split the cases at the median forecast on the signal bar. The mean unusual move of the upper half minus that of the lower half must be above 0 (narrower or stronger breakouts rise more).
- Confirm: The mean unusual move has t ≥ 2 over at least 30 cases, and the upper-half minus lower-half difference is above 0.
- Reject: The mean unusual move has t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 with a supporting difference at or below 0. So is any result with fewer than 30 cases.
