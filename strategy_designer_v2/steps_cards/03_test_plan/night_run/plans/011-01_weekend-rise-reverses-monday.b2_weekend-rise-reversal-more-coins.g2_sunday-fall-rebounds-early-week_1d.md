---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin fell on Sunday (Saturday-close to Sunday-close return) -> adapted: the on/off "fell" is made graded, and the long size grows with the fall's size while the Sunday bar is the active bar.
- Comparison: the fall is measured against the coin's own recent daily volatility -> kept: the one-bar return is divided by the standard deviation of the last 20 daily returns.
- Outcome: the price rises over the next 2 days, more after larger falls -> adapted: the holding period is dropped, so the position is held for one bar and the 2-day rise is measured from the record.
- Verdict transfer: yes: the forecast is exactly the volatility-scaled size of the Sunday fall on Sunday bars, so a rise that grows with it confirms the idea and a fall that grows with it rejects it.
Forecast: The regime detector reads WeekdayComponent. When the coming bar is Monday (value 0), the current bar is the Sunday bar, and the regime is `mean_reversion`; every other bar is `unknown`, which is flat. On the Sunday bar, the forecast is VolatilityScaledReturnComponent (period 1, vol_period 20), the Sunday return in usual daily moves. It is standardised over 60 bars (min 20), negated, and clipped at a minimum of 0. The forecast is positive and grows linearly with the size of the Sunday fall. It is 0 after a Sunday rise and on every other day.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are Sunday bars (regime `mean_reversion`) with forecast > 0, pooled over coins and windows. Sundays are 7 bars apart, so their 2-bar returns do not overlap. Each case's excess return is close[t+2]/close[t] - 1 minus the coin's mean non-overlapping 2-bar return over all its windows. The measure is the OLS slope of that excess return on the forecast, with its t.
- Supporting check: The mean excess 2-bar return over these cases is above 0.
- Confirm: The slope is positive with t ≥ 2, and the mean excess 2-bar return is above 0.
- Reject: The slope is negative with t ≤ -2. Larger Sunday falls are then followed by larger further falls relative to holding the coin.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive. So is t ≥ 2 when the mean excess return is not above 0. At least 300 Sunday-fall cases are required; with fewer, the result is inconclusive.
