---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a 1-day fall, large against its 20-day daily volatility, closing near the day's low; or a large vol-scaled 1-day rise -> kept: fall in usual moves times the close's location toward the low (`FallCloseLocationComponent`, vol_period 20); rise in usual moves (`VolatilityScaledReturnComponent`, period 1, vol_period 20).
- Comparison: the close above its 50-day average for the fall side, below it for the rise side -> kept: regime rule on the close's distance from the 50-day SMA.
- Outcome: rises over the next 1 day after the fall; gives back over the next 1 day after the rise -> kept: long on the fall reading, short on the rise reading, held 1 bar.
- Verdict transfer: yes: every part is measured as stated, so a confirm or a reject of this forecast's next-day gains is a confirm or reject of the idea.
Forecast: A 50-day SMA distance in the regime detector decides which side is active. - Close above its 50-day SMA ("mean_reversion" regime): the forecast is long. It equals the standardised fall-close-location reading: the day's fall in 20-day usual moves times (high − close)/(high − low). It is 0 on up days and grows with a deeper fall and a close nearer the low. - Close below its 50-day SMA ("chop" regime): the forecast is short. It equals minus the standardised 1-day return in 20-day usual moves, clipped so that only rises count. It is 0 on down days and grows more negative with a larger rise. - Exactly on the average ("unknown"): flat. - Standardise uses window 60 and min_periods 20, so a typical signal is about 10 and the cap is 20.
Config: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d_config.json
Criterion:
- Horizon: 1 bars
- Main measure: The case set is every bar with forecast ≠ 0, pooled over coins and windows. On each case, compute position held × (close[t+1]/close[t] − 1 − the coin's mean daily return over all its windows). Test the t of the mean of that value, before costs.
- Supporting check: Split the cases into thirds by |forecast|. The mean drift-adjusted directional next-day return of the top third, minus that of the bottom third, must be above 0.
- Confirm: The main measure's t is 2 or more, and the top-minus-bottom third difference is above 0.
- Reject: The main measure's t is −2 or less.
- Inconclusive: Any t between −2 and 2 is inconclusive. A t of 2 or more with the supporting check failing is also inconclusive. So is a pool of fewer than 100 cases.
