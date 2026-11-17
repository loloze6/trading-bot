---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's 1-day move, up or down, judged by its size against its own 60-day volatility -> adapted: measured as the squared 1-day return over the mean squared 1-day return of the prior 60 days, a graded and rising form of the same size.
- Comparison: the move's size relative to the coin's own 60-day volatility -> kept: the 60-day scale comes from standardise over the 60 prior days.
- Outcome: the coin rises over the next 2 days, more so the larger the move -> adapted: the position follows each day's latest move ("while X"), and the 2-day rise is measured in the criterion.
- Verdict transfer: yes: the forecast grows with the move's size against 60-day volatility in either direction and is always long, so the forecast's relation to the next 2-day return tests the idea directly.
Forecast: The forecast is built from the 1-day return in percent, squared, so it is the same for up and down moves (MomentumDivergenceComponent with both spans set to 1 bar). That value is divided by the mean of the same squared returns over the 60 days before the current bar, then multiplied by 10 and capped at 20 (standardise, window 60, min_periods 20). The result is about (move / 60-day RMS move)² × 10. It is never negative, so the position is always long or flat. It is near 0 after a quiet day, about 10 after a typical day, and grows smoothly to the cap of 20 after a day about 1.4 or more usual moves in size. It is 0 only on a day with no move.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Pooled OLS slope of the next-2-bar return minus the coin's mean 2-bar return (over all its windows) on the recorded forecast. Samples are non-overlapping, at positions 0, 2, 4, … of each window, across all coins and windows. The slope's t is reported with the number of cases.
- Supporting check: The mean excess 2-bar return (as above) on grid bars in the top fifth of the forecast is greater than 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the supporting check failing. At least 500 non-overlapping cases are required, and at least 100 of them in the top fifth; with fewer, the result is inconclusive.
