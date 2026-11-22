---
idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a four-hour volume far above its 30-day average -> adapted: "far above" made graded, as the bar's volume over its prior 180-bar mean, minus 1, kept only above 1 and damped near it.
- Comparison: the coin's 30-day average volume -> kept: the mean volume of the 180 bars (30 days) before the bar.
- Outcome: price rises over the next three days, more with higher volume -> kept: a long position held 18 bars, sized by the volume ratio.
- Verdict transfer: yes: the test measures this ratio against this average, long only, over this horizon, so a confirm or a reject carries over to the idea.
Forecast: The forecast starts from VolumeRatioComponent with period 180, short_period 1, exclude_current 1 and form "centred". It is the 4h bar's volume divided by the mean volume of the prior 180 bars (30 days), minus 1. This value is standardised against its own past 180 values, so a typical size is about 10. It is then clipped at 0, so a bar with below-average volume gives a flat position. Finally, signed_power with exponent 3 and pivot 10 damps ordinary surges toward 0 and amplifies the strong ones. The forecast is therefore never negative. It is 0 at or below average volume, and grows steeply and continuously as the volume rises further above its 30-day average, up to the cap of 20.
Config: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are bets: a rise of the forecast of at least 2 points, read once per cell of each window's non-overlapping 18-bar grid. For each case, take the coin's 18-bar return from the signal bar's close, minus that coin's mean 18-bar return over all windows. The measure is the mean of this excess return weighted by the forecast, with its t computed over cases pooled across coins.
- Supporting check: Split the cases at the median forecast. The mean excess 18-bar return of the upper half minus that of the lower half must be above 0.
- Confirm: The forecast-weighted mean excess return is above 0 with t ≥ 2, and the upper-half minus lower-half difference is above 0.
- Reject: The forecast-weighted mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is t ≥ 2 when the upper half does not beat the lower half. At least 100 cases across all coins and windows are needed; with fewer, the result is inconclusive.
