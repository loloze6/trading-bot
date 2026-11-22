---
idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a four-hour volume far above its 30-day average -> adapted: "far above" becomes graded, as the volume ratio's excess over 1 with a strong graded dead zone.
- Comparison: against the coin's own 30-day (180-bar) average volume -> kept
- Outcome: the coin rises over the next three days, more for a larger surge -> kept
- Verdict transfer: yes: the forecast is long only on volume above the 30-day average, grows with the ratio, and is judged on the 18-bar rise that follows.
Forecast: The forecast starts from the current 4h bar's volume divided by its 180-bar (30-day) mean, minus 1. This is standardised over its past 180 values. It is clipped at 0, so it is long only and is 0 whenever volume is at or below average. It is then passed through signed_power with exponent 3 and pivot 20, the strongest graded dead zone. Ordinary above-average volume gives almost no position. The forecast grows steeply as the surge becomes extreme, up to +20 at the standardise cap. It is never negative.
Config: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Take the cases: forecast bets of at least 2 points, read once per non-overlapping 18-bar grid cell of each window. For each case, compute the coin's 18-bar return from the signal bar minus its normal 18-bar drift (mean over all windows). The measure is the mean of these excess returns across all coins, with the ordinary t of the mean.
- Supporting check: Across the cases, the Spearman correlation between the forecast at the signal bar and the excess 18-bar return is above 0.
- Confirm: The mean excess return is above 0 with t >= 2, over at least 30 cases, and the supporting correlation is above 0.
- Reject: The mean excess return is below 0 with t <= -2, over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with a correlation at or below 0 is also inconclusive. Fewer than 30 independent cases is inconclusive.
