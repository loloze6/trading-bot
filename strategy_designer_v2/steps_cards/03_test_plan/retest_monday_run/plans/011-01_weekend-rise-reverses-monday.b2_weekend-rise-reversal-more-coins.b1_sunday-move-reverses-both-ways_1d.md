---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's Saturday-to-Sunday close-to-close move, in either direction, of any size -> kept: the Sunday bar's 1-day return, read at Sunday's close when the coming bar is Monday.
- Comparison: none -> kept
- Outcome: the price moves the other way over Monday and Tuesday, more after a larger weekend move -> kept: a position against the move, sized by it, held 2 daily bars.
- Verdict transfer: yes: the test bets against each weekend move in proportion to its size for exactly Monday and Tuesday, which is what the idea states.
Forecast: The regime detector reads the weekday of the coming bar. The forecast is active only at the close of the Sunday bar, when the coming bar is Monday. It is flat on every other bar. On that bar it is minus the Sunday bar's 1-day close-to-close return. That return is standardised against the mean absolute size of the 60 previous daily returns, with target 10 and cap 20. The forecast is negative (short) after a weekend rise and positive (long) after a weekend fall. Its size grows linearly with the move: an ordinary move gives about 10, and twice that move hits the cap of 20. The bet is held 2 bars, through Monday and Tuesday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are the Sunday-close bars (regime mean_reversion) with a nonzero forecast. For each case, take the forecast times the coin's 2-bar return (Sunday close to Tuesday close, inside the window), minus that coin's mean 2-bar return over all its windows. The measure is the mean of this product over all cases and its t of the mean. The cases are one per week, so they do not overlap.
- Supporting check: Split the cases by |forecast| into thirds. The mean drift-adjusted 2-bar return in the forecast's direction must be higher in the largest third than in the smallest third (difference above 0).
- Confirm: The mean forecast-weighted drift-adjusted 2-bar return is positive with t >= 2, over at least 200 cases, and the supporting check passes.
- Reject: The mean forecast-weighted drift-adjusted 2-bar return is negative with t <= -2, over at least 200 cases. That means weekend moves continue rather than reverse.
- Inconclusive: Any of these is inconclusive: - t between -2 and 2; - t >= 2 while the size check fails; - fewer than 200 cases.
