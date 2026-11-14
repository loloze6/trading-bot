---
idea: N3-01_strong-volatile-momentum
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: coin up over both 20 and 60 days, with 20-day volatility in its upper range -> kept: regime rules, 20- and 60-day returns above 0 and the 20-day volatility percentile at or above 0.5.
- Comparison: next days rise more than the coin's average -> kept: forward returns judged against the coin's mean return over all windows.
- Outcome: price rises over the next days -> kept: forward return over 5 bars, long side only.
- Verdict transfer: yes: the conditions are kept as rules and the size of the run-up only grades the long, so both a confirm and a reject read directly on the idea.
Forecast: The forecast is active only on bars where the 20-day return and the 60-day return are both above 0 and the smoothed 20-day volatility percentile, ranked over 100 bars, is at or above 0.5. On all other bars it is 0. When active, the forecast is the 20-day return divided by the mean absolute 20-day return of the 60 bars before it, times 10, capped at 20. It is then cubed around a pivot of 10, so an ordinary run-up gives a near-zero long and an unusually large one a large long. It is then clipped at 0, so it is never short. It grows continuously with how far the 20-day return exceeds its usual size.
Config: N3-01_strong-volatile-momentum_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The 5-bar forward return after bars with forecast at or above 10, minus the coin's mean 5-bar return over all 24 windows pooled. Cases are pooled across coins and taken at most one per 5 bars per coin, so overlapping returns are counted once.
- Supporting check: Across active bars, the excess 5-bar return grows with forecast size, measured as a positive slope of excess return on forecast with non-overlapping samples.
- Confirm: The mean excess 5-bar return after forecast at or above 10 is positive with t >= 2, before costs.
- Reject: The mean excess 5-bar return after forecast at or above 10 is negative with t <= -2, meaning these run-ups reverse.
- Inconclusive: Any t between -2 and 2, including results near zero. Also any result with fewer than 30 non-overlapping cases at forecast at or above 10.
