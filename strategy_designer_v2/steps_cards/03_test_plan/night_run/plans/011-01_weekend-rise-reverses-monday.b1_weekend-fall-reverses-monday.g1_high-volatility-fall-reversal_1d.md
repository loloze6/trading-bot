---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a down day in a coin whose 20-day daily volatility is high, the fall sized in 20-day daily standard deviations -> adapted: the high-volatility condition is a regime on the 20-day volatility percentile, and the fall is graded, not a down-day switch.
- Comparison: the effect is stronger as 20-day volatility rises, with no fading in calm markets -> kept: calm bars are flat, and a second component scales the fall by current volatility against its recent level.
- Outcome: price rises over the next 1 day -> kept: long for one daily bar, scored on the next close.
- Verdict transfer: yes: the forecast is long only after down days in volatile regimes, sized by fall depth and volatility, so its next-day gains confirm or reject the idea directly.
Forecast: The forecast is computed only on bars where the 20-day volatility percentile, ranked against the past 100 bars, is at or above 0.5. On every other bar it is flat. It is the equal-weight mean of two parts: - the day's return in 20-day standard deviations (`VolatilityScaledReturnComponent`, period 1, vol_period 20); - the day's percent return (`PriceEvolutionComponent`, period 1), standardised against its past 60 values. This is the fall in standard deviations times current volatility against its recent level. Each part is standardised over 60 bars, negated, and clipped at 0. Each part is therefore positive only on a down day and grows with the fall. The second part also grows with volatility. The forecast is zero on up days and in calm regimes, and never negative.
Config: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, the mean of (forecast / 10) x (the coin's next-day return minus the coin's mean daily return over all windows), pooled across coins and windows, with its t-statistic.
- Supporting check: On the same bars, the Spearman rank correlation between the forecast and the next-day excess return is above 0.
- Confirm: The main measure's t is 2 or more, and the rank correlation is above 0.
- Reject: The main measure's t is -2 or less.
- Inconclusive: Any t between -2 and 2, or t of 2 or more with a rank correlation of 0 or below, is inconclusive. Fewer than 100 bars with forecast > 0 is also inconclusive.
