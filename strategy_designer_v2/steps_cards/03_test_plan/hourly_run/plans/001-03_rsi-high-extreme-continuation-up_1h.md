---
idea: 001-03_rsi-high-extreme-continuation-up
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: hourly RSI at a high extreme after a one-sided run up -> adapted: graded by how far RSI(14) sits above 50, squared so extremes dominate; "after X" becomes "while X".
- Comparison: returns after neutral RSI readings -> kept: returns after the largest positions are compared with returns after RSI 45–55 bars.
- Outcome: price keeps rising over the following hours -> kept: forward 6-bar return of the coin, upward.
- Verdict transfer: yes: a long sized by RSI strength above 50 profits only if high readings precede gains larger than after neutral readings.
Forecast: Use RSIPullbackComponent (period 14, signed), which outputs 50 − RSI. Standardise it over its past 60 values, then negate it so the forecast is positive when RSI is above 50. Clip it at a minimum of 0, so there is never a short. Then apply signed_power with exponent 2 and pivot 10. Readings near 50 are damped smoothly towards zero, and high readings grow quadratically, up to the cap of 20. The forecast is zero whenever RSI is at or below 50, and it is largest at the highest RSI extremes.
Config: 001-03_rsi-high-extreme-continuation-up_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: The 6-bar forward close-to-close return after bars where the forecast is in its top decile, minus the same return after neutral bars. Neutral bars are those where the raw RSI component lies between −2 and +2, that is RSI between 45 and 55. Returns are measured before costs and use non-overlapping 6-bar blocks. The result is pooled over coins and windows, with a t-statistic.
- Supporting check: In each coin, the mean 6-bar forward return after top-decile bars minus the coin's unconditional mean 6-bar return, so that the market's own drift is removed.
- Confirm: The pooled difference is greater than 0 with t ≥ 2, and the supporting excess is positive in at least 2 of the 3 coins.
- Reject: The pooled difference is below 0 with t ≤ −2, meaning high RSI readings are followed by weaker returns than neutral readings.
- Inconclusive: A t-statistic strictly between −2 and 2, or a confirming t without the 2-of-3-coin agreement. The test needs at least 200 non-overlapping top-decile cases and 200 neutral cases pooled; with fewer it is inconclusive.
