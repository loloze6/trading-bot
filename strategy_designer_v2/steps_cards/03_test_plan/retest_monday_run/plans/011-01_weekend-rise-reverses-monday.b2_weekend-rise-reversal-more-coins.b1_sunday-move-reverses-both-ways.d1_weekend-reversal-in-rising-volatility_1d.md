---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's Saturday-to-Sunday close-to-close move, while its 20-day daily volatility is high against its last 60 days -> kept: the regime selects Sunday-close bars whose 20-day return std is at least the 60-day std, and the position grows with the Sunday bar's one-bar return.
- Comparison: 20-day daily volatility against the last 60 days' volatility -> kept: the std of the last 20 daily returns over the std of the last 60, with the condition met at a ratio of 1 or more (convention).
- Outcome: price moves the other way over Monday and Tuesday, more after a larger weekend move -> kept: a contrarian bet at Sunday's close, held 2 daily bars, sized by the weekend move.
- Verdict transfer: yes: the config bets against exactly the stated weekend move, only in the stated volatility condition, over the stated two days.
Forecast: The forecast is computed at each Sunday close, and only when the 20-day volatility of daily returns is at least the 60-day volatility (RecentToPriorVolatilityRatioComponent, vol_period 20, base_period 60, base_lag 0, ratio of 1 or more). It is the Sunday bar's one-bar return (PriceEvolutionComponent, period 1, close Sunday / close Saturday - 1), standardised over its last 60 daily values and then negated. After a weekend rise it is negative (short), after a fall it is positive (long), and its size grows with the size of the weekend move, capped at 20. On every other bar, and on Sundays in calm markets, the regime is null and the forecast is 0. The bet placed at Sunday's close is held for the 2 bars of Monday and Tuesday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are the Sunday bars with a nonzero forecast. For each case, take the coin's 2-bar return close[t+2]/close[t] - 1 and subtract the coin's normal 2-bar drift (its mean 2-bar return over all its windows, on non-overlapping stretches). Multiply the result by the sign of the forecast. The measure is the ordinary t of the mean of this signed excess move over all cases, all coins pooled. Cases are weekly, so they do not overlap.
- Supporting check: Split the cases at the median of |forecast|. The mean signed excess move of the larger half minus that of the smaller half must be above 0.
- Confirm: The mean signed excess move is positive with t >= 2 over at least 100 cases, and the supporting check passes.
- Reject: The mean signed excess move is negative with t <= -2 over at least 100 cases, meaning weekend moves continue rather than reverse.
- Inconclusive: Any t between -2 and 2, or t >= 2 with a failed supporting check, is inconclusive. Fewer than 100 cases is inconclusive whatever the t.
