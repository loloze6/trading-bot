---
idea: 081-01_deep-up-day-next-day-fade
brief: 081_deep-up-day-fades-any-market
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a day that closes up, sitting below the 20-day high -> adapted: "closes up" is a regime of up days; inside it the depth is graded, not thresholded.
- Comparison: deeper below the high, in 20-day daily swings, against shallower -> kept: the depth is (close − 20-day high) / high / std of 20 daily returns, and the short grows with it.
- Outcome: a larger fall over the next day -> kept: short for one daily bar, sized by depth.
- Verdict transfer: yes: deeper up days fading more the next day, beyond the coin's drift, is the idea itself, and no such fade rejects it.
Forecast: The forecast exists only on bars whose close is above the prior close (the regime). It is zero on every other bar. - On an up day it is the close's distance below its highest close of the last 20 days (today included), divided by that high and by the standard deviation of the last 20 daily returns. - That distance is standardised against its own past 60 values. It is always zero or negative. - So the forecast is a short that is zero at a new 20-day high and grows in size as the close sits more usual swings below that high, capped at −20.
Config: 081-01_deep-up-day-next-day-fade_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: - The sample is the up-day bars with a non-zero forecast. - On each, the timing gain is the position held × (the next day's return − the coin's mean daily return over all windows). - Gains are summed per day across coins. The measure is the t of their mean.
- Supporting check: On those up days, the next-day excess return of the deepest third by depth minus that of the shallowest third must be negative (Welch t ≤ −1).
- Confirm: Both must hold: - The mean daily timing gain is positive with t ≥ 2. - The supporting check passes.
- Reject: The mean daily timing gain is negative with t ≤ −2 (the deep up days rise more than the drift).
- Inconclusive: - Any t between −2 and 2, or a confirming main measure with a failed check. - Fewer than 300 up-day cases on fewer than 100 distinct days.
