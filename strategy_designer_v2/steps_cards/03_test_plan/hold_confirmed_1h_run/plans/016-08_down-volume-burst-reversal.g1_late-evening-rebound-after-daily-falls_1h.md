---
idea: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's fall over its past 24 hours, as of the 20:00 UTC close -> kept: a regime selects the decision bar whose coming bar starts at 20:00, and PriceEvolution(24) is negated and clipped to falls only.
- Comparison: none (a graded "the more ... the more" relation) -> kept
- Outcome: the coin rises more over the next 2 hours, long only -> adapted: holding period dropped, the position is held one bar and the 2-bar rise is read from the record.
- Verdict transfer: yes: the test grades a long position by the 24h fall on exactly the 20:00 decision bars and judges the 2-hour return that follows.
Forecast: The forecast is active only on the bar that closes at 20:00 UTC, where the coming bar's hour is 20. On every other bar it is 0. On that bar it is the 24-bar percent change of the close, standardised against its own last 60 hourly values (mean absolute value about 10, capped at 20), with its sign flipped and clipped at 0. It is positive and grows with the size of the 24-hour fall. It is 0 when the coin rose over the 24 hours. It never goes short.
Config: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are the decision bars (regime mean_reversion) with forecast > 0, one per day per coin. For each case, take the 2-bar return close[t+2]/close[t]-1 inside the window and subtract the coin's mean 2-bar return over all windows. Regress this excess return on the forecast, pooled over coins and windows, and read the t of the slope.
- Supporting check: The mean excess 2-bar return of the cases in the top third of forecasts, minus that of the bottom third, is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any t between -2 and 2, or a t of 2 or more with the check failing. At least 500 cases are needed; with fewer the result is inconclusive.
