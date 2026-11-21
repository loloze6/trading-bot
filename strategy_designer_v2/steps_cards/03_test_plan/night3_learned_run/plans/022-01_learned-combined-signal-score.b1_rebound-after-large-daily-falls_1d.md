---
idea: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: a coin's 1-day fall, the larger the stronger -> kept: the 1-bar return in usual moves, negated, long side only.
- Comparison: the fall against its 30-day volatility -> kept: divided by the std of the last 30 daily returns.
- Outcome: higher return over the next 1 day -> kept: each bet is held 1 bar.
- Verdict transfer: yes: the forecast grows with the vol-scaled daily fall and is judged on the next day's return, as the idea states.
Forecast: The forecast starts from one value: today's close-to-close return divided by the standard deviation of the last 30 daily returns. It is negated and standardised over its past 60 values, so a fall reads positive. It is clipped at 0, so it is zero on up days and the strategy is long only after falls. A signed power with exponent 2 and pivot 10 then damps small falls towards zero, which matches "refuse small falls", and amplifies large ones. The forecast grows smoothly with the size of the fall in usual moves, and it is never negative.
Config: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The OLS slope of the next-day excess return on the bar's forecast, pooled over all coins and windows. The excess return is close[t+1]/close[t]-1 minus the coin's mean daily return over all windows. Every bar is one case, since the horizon is 1 bar. The slope comes with its t-statistic.
- Supporting check: On bars with forecast > 0, the mean next-day excess return must be above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is a t of 2 or more with a failed supporting check. The test needs at least 300 bars with forecast > 0 across coins and windows; with fewer it is inconclusive.
