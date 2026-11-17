---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's Saturday-to-Sunday close-to-close return, in either direction -> adapted: the Sunday bar's one-bar return, read at Sunday's close, used as a graded size rather than an on/off event.
- Comparison: none (the idea only says larger weekend moves bring larger moves back) -> kept
- Outcome: price moves against the weekend move over Monday and Tuesday, more for larger moves -> adapted: the position is held only from Sunday's close to Monday's close (holding period dropped); the 2-day move after Sunday's close is still measured from the record.
- Verdict transfer: yes: the forecast leans against Sunday's move, sized by that move, and is judged on the following Monday-plus-Tuesday return.
Forecast: - When it is active. A weekday regime selects Sunday's bar: that is the bar whose next bar is Monday, so WeekdayComponent equals 0. On every other bar the forecast is 0 (flat). - What it reads on Sunday. The 1-bar return of the Sunday bar, from PriceEvolutionComponent with period 1. - How it is scaled. That return is standardised against the mean absolute size of its own 60 previous daily values (min_periods 20), then negated. - Sign and size. The forecast is negative after a weekend rise and positive after a weekend fall. Its size grows linearly with the size of the weekend move (about ±10 for a typical daily move, capped at ±20).
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: - Cases. Each Sunday bar with regime mean_reversion and a non-zero forecast, where bar t+2 lies in the same window. Sundays are 7 bars apart, so these cases do not overlap. - Score per case. (forecast/10) × (close[t+2]/close[t] − 1 − the coin's mean 2-bar return over all windows). - Test. The t of the mean score over all cases, against zero. - Benchmark. Subtracting the coin's mean 2-bar return judges the idea against simply holding the coin, before costs.
- Supporting check: - Sort the same cases by |forecast| into terciles. - Compute sign(forecast) × excess 2-bar return in each tercile. - The check passes when the mean of the top tercile minus the mean of the bottom tercile is greater than 0, meaning larger weekend moves reverse more.
- Confirm: the main-measure t is ≥ 2 and the supporting check passes.
- Reject: the main-measure t is ≤ −2, meaning weekend moves continue into Monday and Tuesday.
- Inconclusive: - A main-measure t between −2 and 2. - A t of 2 or more with the tercile difference ≤ 0. - Fewer than 300 cases in total.
