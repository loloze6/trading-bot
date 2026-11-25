---
idea: 041-01_agitated-scaled-rise-next-day-continues
brief: 041_agitated-falls-revert-rises-do-not
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a one-day rise, measured against the 30-day standard deviation of daily returns, in an agitated market -> adapted: graded by the scaled rise (zero on down days); the agitated profile is added by code.
- Comparison: the rise's size against the 30-day daily-return std -> kept.
- Outcome: the larger the scaled rise, the larger the rise over the next day -> kept.
- Verdict transfer: yes: the forecast is the scaled rise itself, held one day, so its next-day gains test the idea directly.
Forecast: The forecast is the day's return divided by the standard deviation of the last 30 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 30). It is standardised against its own past 60 values and clipped at 0, so it is long only. It is zero on down or flat days. On up days it is positive and grows linearly with the scaled rise, up to the cap of 20. Outside the agitated profile it is zero (the profile is added by code).
Config: 041-01_agitated-scaled-rise-next-day-continues_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, the forecast-weighted mean of the next-day return minus the coin's mean daily return over all windows. Its t treats the cases of one day as one piece of evidence.
- Supporting check: Among cases with forecast > 0, the mean next-day excess return of the top third by forecast minus that of the bottom third is above 0.
- Confirm: The main measure is positive with t >= 2, and the supporting check passes.
- Reject: The main measure is negative with t <= -2 (scaled rises given back beyond drift).
- Inconclusive: Any result with t between -2 and 2 is inconclusive. A main t >= 2 with the supporting check failing is also inconclusive. So is a test with fewer than 100 distinct days with forecast > 0.
