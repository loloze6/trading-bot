---
idea: 058-01_calm-downtrend-depth-continues
brief: 058_quiet-volume-calm-decline-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: a coin in a falling, calm market that has fallen over its last 30 days -> kept: the 30-day fall measured directly; the code adds the falling calm profile.
- Comparison: the more it has fallen, the more it keeps falling -> kept: the short position grows with the depth of the 30-day fall.
- Outcome: it keeps falling over the next 5 days -> kept: a short held for 5 daily bars.
- Verdict transfer: yes
Forecast: The forecast is the coin's 30-day return in percent (PriceEvolutionComponent, period 30), standardised over its last 60 values (min_periods 20). It is then clipped at a maximum of 0, so only falls count. The forecast is negative (short) when the coin is below its close of 30 days ago, and grows in size with the depth of that fall, up to the cap of -20. It is zero when the coin is at or above that close. There is no long side. The code adds the falling calm profile, so the forecast is zero outside it.
Config: 058-01_calm-downtrend-depth-continues_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping 5-bar grid of each window, on cells whose bar has forecast < 0. For each cell, take the coin's 5-bar return minus its normal drift (its mean 5-bar return over all windows), times -1 for the short side. Average these values weighted by |forecast|. Its t pools the cases of one day together.
- Supporting check: On the same cases, the signed excess return of the half with the larger |forecast| minus that of the half with the smaller |forecast| is above 0.
- Confirm: The weighted mean signed excess return is above 0 with t >= 2, and the supporting check is above 0.
- Reject: The weighted mean signed excess return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2, or a confirming t with a failed supporting check. Fewer than 30 grid cases in a position (with forecast < 0) on the six coins together is also inconclusive.
