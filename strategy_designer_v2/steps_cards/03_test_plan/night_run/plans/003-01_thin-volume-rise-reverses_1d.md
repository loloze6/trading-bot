---
idea: 003-01_thin-volume-rise-reverses
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a sharp one-day rise on a coin -> adapted: "sharply" made graded, as the day's rise in usual moves (20-day return volatility), on up days only.
- Comparison: volume well below its own 30-day average daily volume -> adapted: "well below" made graded, as the log of the day's volume over its prior 30-day mean, on below-average days only.
- Outcome: part of the rise is given back over the next 5 days, more for a larger rise on thinner volume -> adapted: the 5-day hold is dropped, so the short is held only while the situation lasts and is judged on the 5-day return.
- Verdict transfer: yes: the forecast is short in proportion to both the rise and the thinness, exactly on the idea's bars, and it is judged on the idea's 5-day return.
Forecast: The forecast is active only when two conditions both hold. The day's close-to-close return must be up (VolatilityScaledReturnComponent, period 1, vol_period 20, above 0). The day's volume must be below the mean of the prior 30 days (VolumeRatioComponent, period 30, exclude_current 1, ratio below 1). On all other bars the forecast is 0. When active, it is the equal-weight mean of two parts: - the rise in usual moves, standardised and negated; - the log volume ratio, standardised, which is negative when volume is thin. Each part goes through signed_power with exponent 3, so small rises or near-average volume give a short close to 0. The short grows steeply as the rise gets larger and the volume thinner. The forecast is never positive.
Config: 003-01_thin-volume-rise-reverses_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping 5-bar grid of each window, using only grid bars with a forecast below 0, pooled over coins and windows. On each such bar, take -forecast/10 x (the coin's 5-bar return minus that coin's mean 5-bar return over all its windows). Report the ordinary t of the mean of this quantity. A positive mean says the short gains more than holding the coin, and gains more when the short is larger.
- Supporting check: Take the 20% of active grid bars with the most negative forecast. Their mean excess 5-bar return (the coin's return minus its mean 5-bar return) must be below 0.
- Confirm: The main measure's t is 2 or more and the supporting check passes.
- Reject: The main measure's t is -2 or less.
- Inconclusive: Any t strictly between -2 and 2. Also a t of 2 or more where the supporting check fails. Also any result from fewer than 100 active grid cases in total.
