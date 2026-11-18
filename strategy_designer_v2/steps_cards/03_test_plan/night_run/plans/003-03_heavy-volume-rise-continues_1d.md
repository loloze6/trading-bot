---
idea: 003-03_heavy-volume-rise-continues
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a sharp one-day rise on volume well above its own 30-day average -> adapted: the threshold is made graded, as the day's return in usual moves times volume over its 30-day mean, long side only.
- Comparison: volume against the coin's own 30-day average daily volume -> kept.
- Outcome: the price keeps rising over the next 5 days, more after larger, heavier rises -> adapted: "after" becomes "while", and the 5-day hold is dropped. The 5-bar forward return is still what is judged.
- Verdict transfer: yes: the forecast is the size of the rise and its relative volume, and it is judged on the 5-bar gain that follows it, net of holding the coin.
Forecast: The forecast starts from VolumeWeightedScaledReturnComponent (vol_period 20, volume_period 30). This is the day's close-to-close return divided by the standard deviation of the last 20 daily returns, times the day's volume over its 30-day mean volume. It is standardised against its own last 60 values (min_periods 20) and clipped at 0, so it is positive only on up days. A signed_power with exponent 3 and pivot 20 then acts as the strongest graded dead zone. The forecast is near 0 on ordinary up days and on down days. It grows steeply as the rise gets larger and the volume heavier, up to +20 at the extremes, and it is never short.
Config: 003-03_heavy-volume-rise-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take the bars of the non-overlapping 5-bar grid in each window, keeping those with forecast >= 5 (the large positions). On those bars, measure the 5-bar forward return close[t+5]/close[t]-1 minus that coin's mean 5-bar return over all windows. Report the t of the mean of this excess.
- Supporting check: On grid bars with forecast > 0, the Spearman correlation between the forecast and the 5-bar excess return is positive.
- Confirm: The mean excess is positive with t >= 2 over at least 30 independent cases, and the supporting correlation is above 0.
- Reject: The mean excess is negative with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t is also inconclusive when the correlation is not above 0. Fewer than 30 grid cases with forecast >= 5 is inconclusive.
