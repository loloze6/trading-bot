---
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 42e48552438e
---
Fidelity:
- Situation: a 4h close above the high of the preceding two days while the 30-day return is negative -> kept: a regime rule fires when the close breaks the prior 12-bar high and the 180-bar return is below 0.
- Comparison: falls more than usual, against the coin's normal drift -> kept: the criterion measures returns net of the coin's mean 72-bar return.
- Outcome: the coin falls over the next 12 days, more so the deeper the 30-day fall -> kept: a short position sized by the depth of the 180-bar fall, held 72 bars.
- Verdict transfer: yes: the test bets short only on the stated breakouts, sizes each bet by the stated depth, and judges the stated 12-day fall against the usual move.
Forecast: The regime detector checks two things on each bar. The first is BreakoutInMeanRangesComponent (side "above", period 12, base 180), which must be above 0, meaning the close is above the highest high of the prior 12 bars (two days). The second is PriceEvolutionComponent (period 180, 30 days), which must be below 0, meaning the 30-day return is negative. When both hold, the bar is "trending". On every other bar the regime is null and the forecast is 0. On trending bars the forecast is the 180-bar return, standardised over its past 181 values. That return is negative there, so the forecast is short, and its size grows continuously with the depth of the 30-day fall (about -10 for a typical depth, capped at -20). It is never positive.
Config: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The unusual move per case, in the short direction. A case is a bet: a short rise of the forecast of at least 2 points, read once per 72-bar grid cell. The unusual move is minus (the 72-bar return from the signal bar's close minus the coin's normal 72-bar drift over all windows). The measure is its mean over the cases, with the t of that mean.
- Supporting check: Across cases, the correlation between the absolute forecast at the signal bar and the short-direction unusual move is above 0. This tests whether a deeper fall gives a larger decline.
- Confirm: The mean short-direction unusual move is above 0 with t >= 2, and the supporting correlation is above 0.
- Reject: The mean short-direction unusual move is below 0 with t <= -2, meaning the coin rises more than usual after these breakouts.
- Inconclusive: These results neither confirm nor reject: a t between -2 and 2, or t >= 2 with a correlation of 0 or less. Any result from fewer than 30 cases across all coins and windows is also inconclusive.
