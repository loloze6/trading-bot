---
idea: 032-01_calm-decline-depth-continues
brief: 032_calm-decline-keeps-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: the coin fell over the past 28 days while its daily ranges and volume stayed near their usual levels -> adapted: the calm condition is a regime (28-day mean bar range and mean volume each within 0.8 to 1.25 of their 360-day means), and the 28-day fall is graded, zero when there was no fall.
- Comparison: ranges and volume against their own usual levels; a larger fall against a smaller one -> kept: the 360-day means set the calm band, and the forecast's size follows the depth of the 28-day fall.
- Outcome: the coin keeps falling over the next 5 days, by more after a deeper fall -> kept: a short held for 5 bars, sized by the fall.
- Verdict transfer: yes: the test bets that calm 28-day falls continue in proportion to their depth, which is exactly what the idea claims.
Forecast: The detector reads two measures. One is the mean daily high-low range over the last 360 days divided by its mean over the last 28 days. The other is the mean daily volume over the last 28 days divided by its mean over the last 360 days. A bar is calm (regime `trending`) only when both ratios lie between 0.8 and 1.25. Every other bar is flat. On calm bars the forecast is the 28-day percent return, standardised against its own past 60 values and clipped at a maximum of 0. It is negative (short) only after a 28-day fall, and it grows with the depth of that fall, up to the cap of 20. It is 0 when the coin did not fall or the market is not calm.
Config: 032-01_calm-decline-depth-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's next 5-bar return, minus its mean 5-bar return over all windows, on the forecast. Measured on the non-overlapping 5-bar grid of each window, over the cells where the forecast is below 0. Cases on the same day are summed into one, so the t counts days.
- Supporting check: The mean of the same excess 5-bar return taken in the short direction (its negative) over those cells must be above 0.
- Confirm: The slope is positive with t ≥ 2, so a more negative forecast is followed by a lower excess return, and the supporting check's mean is above 0.
- Reject: The slope is negative with t ≤ -2, or the short-direction mean excess return has t ≤ -2.
- Inconclusive: Any slope t between -2 and 2, or a confirming slope whose short-direction mean is not above 0, is inconclusive. So is any result with fewer than 30 independent days of cases.
