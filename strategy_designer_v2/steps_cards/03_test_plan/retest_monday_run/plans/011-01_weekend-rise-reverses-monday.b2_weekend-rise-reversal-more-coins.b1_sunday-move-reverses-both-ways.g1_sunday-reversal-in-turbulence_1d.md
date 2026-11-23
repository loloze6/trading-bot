---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 6d77ef5ed57a
---
Fidelity:
- Situation: a coin's Sunday close-to-close move -> kept: the one-bar return of the bar stamped Sunday, read at Sunday's close and selected by a weekday regime.
- Comparison: past 20-day volatility against the usual 60-day volatility -> kept: 20-bar return std over 60-bar return std, multiplying the move, so larger moves at higher ratios weigh more.
- Outcome: the move is undone over Monday and Tuesday -> kept: a position against Sunday's move, held 2 daily bars.
- Verdict transfer: yes: the forecast bets against Sunday's move, sized by move times volatility ratio, over exactly the 2 days the idea names.
Forecast: The forecast is active only at Sunday's daily close. That is the bar whose next bar, per WeekdayComponent, is Monday (0); on every other day it is zero. On a Sunday it is the negated product of two things: Sunday's one-bar percent return, and the ratio of the 20-bar to the 60-bar standard deviation of one-bar returns. The product comes from RecentToPriorVolatilityWeightedReturnComponent with period 1, vol_period 20, base_period 60 and base_lag 0. It is standardised against its own past 61 values (min_periods 20). The forecast is negative after an up Sunday and positive after a down Sunday. Its size grows linearly with the size of the move and with how turbulent the last 20 days were against the last 60. It is zero for a flat Sunday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are Sunday bars with a non-zero forecast; Sundays are 7 bars apart, so the cases do not overlap. Each case's unusual move is the coin's return from Sunday's close to Tuesday's close, minus the coin's normal 2-bar drift over all windows. The measure is the pooled least-squares slope of that unusual move on the forecast, with its t.
- Supporting check: The forecast-weighted mean of the unusual move in the forecast's direction is above 0. That is sum(|forecast| × sign(forecast) × unusual move) / sum(|forecast|).
- Confirm: The slope is positive with t ≥ 2 and the supporting check passes.
- Reject: The slope is negative with t ≤ -2, meaning larger, more turbulent Sunday moves continue rather than reverse.
- Inconclusive: Any slope with -2 < t < 2, or a positive t ≥ 2 with the check failing. A minimum of 300 Sunday cases across all coins and windows is required; with fewer, the result is inconclusive.
