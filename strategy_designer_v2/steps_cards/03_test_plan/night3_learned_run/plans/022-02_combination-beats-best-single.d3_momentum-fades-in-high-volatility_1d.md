---
idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day return, higher or lower -> kept: the 28-bar return.
- Comparison: 30-day volatility against its own past, lower is stronger -> kept: the 28-bar return is divided by current 30-bar volatility, which equals the return in past-usual units times past-usual volatility over current volatility.
- Outcome: the return over the next 20 days rises with the 28-day return -> kept: 20-bar forward return, signed like the momentum.
- Verdict transfer: yes: the forecast is momentum, sized up as current volatility falls below its past level, and it is held for the idea's 20 days.
Forecast: The forecast is the 28-bar return divided by the standard deviation of the last 30 daily returns, with no lag (VolatilityScaledReturnComponent, period 28, vol_period 30, vol_lookback 1). This equals the 28-day momentum, in the coin's usual moves, times how calm the coin is now against its past. It is standardised over its own past 60 values (target 10, cap 20). It is positive after a rise and negative after a fall. Its size grows with the size of the rise or fall and with how far current volatility sits below its usual level. It is near zero when the coin has gone nowhere over 28 days. It is ungated and signed.
Config: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The sample is the non-overlapping 20-bar grid of each window, every coin pooled. On each grid bar, take forecast/10 × (the coin's 20-bar forward return minus its normal 20-bar drift over all windows). The measure is the mean of this product and its t, which shows whether excess gains grow with the signed position size.
- Supporting check: The book's timing gain must be positive. This is the book's mean daily return before costs minus its gain from the market's own rise.
- Confirm: The main mean is positive with t ≥ 2.0, and the timing gain is above 0.
- Reject: The main mean is negative with t ≤ -2.0.
- Inconclusive: Any t between -2.0 and 2.0 is inconclusive. So is t ≥ 2.0 with a timing gain of 0 or less. Fewer than 300 grid cases pooled is also inconclusive.
