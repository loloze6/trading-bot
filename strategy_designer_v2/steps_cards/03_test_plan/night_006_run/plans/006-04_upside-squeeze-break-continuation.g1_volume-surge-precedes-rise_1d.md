---
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the 5-day average volume against the 30-day average volume, the higher the stronger -> kept
- Comparison: the price rise against the coin's usual 3-day return -> kept
- Outcome: the price rises more over the next 3 days as the ratio rises; quiet, fading volume means staying out -> kept
- Verdict transfer: yes: the forecast grows with the same volume ratio and is flat when volume fades, and the test measures the excess 3-day return the idea claims.
Forecast: The forecast is the log of the ratio between the mean volume of the last 5 bars and the mean volume of the last 30 bars (bar t included), standardised against its own past 60 values. It is positive when recent volume is above the 30-day average, and it grows with the size of the surge, up to the cap of 20. It is clipped at 0, so the strategy is flat when recent volume is at or below the average, as the idea's consequence says. It is long-only and graded, with no regime condition.
Config: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: On a non-overlapping 3-bar grid in each window, take the coin's 3-bar forward return minus that coin's mean 3-bar return over all its windows. Regress this pooled excess return on the recorded forecast and report the t of the slope.
- Supporting check: The forecast-weighted mean of the excess 3-bar return on the same grid is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes (forecast-weighted mean excess return > 0), with at least 300 grid cases where forecast > 0.
- Reject: The slope's t is -2 or less, with at least 300 grid cases where forecast > 0.
- Inconclusive: Any other result is inconclusive: a slope t between -2 and 2, or t of 2 or more with the forecast-weighted mean excess at or below 0. Fewer than 300 grid cases with forecast > 0 is also inconclusive, whatever the t.
