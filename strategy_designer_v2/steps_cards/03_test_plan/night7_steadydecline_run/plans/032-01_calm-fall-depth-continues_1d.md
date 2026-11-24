---
idea: 032-01_calm-fall-depth-continues
brief: 032_calm-decline-keeps-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin in a falling, calm market -> kept: the falling calm profile, which code adds as the regime
- Comparison: larger past 30-day falls against smaller ones -> adapted: the 30-day fall's size grades the short position
- Outcome: the coin falls more over the next day -> kept: next-day return, 1 bar, short side
- Verdict transfer: yes: a graded short sized by the 30-day fall, held one day inside the profile, earns only if larger falls lead to larger next-day declines.
Forecast: The forecast uses the 30-bar price change (PriceEvolutionComponent, period 30). It is standardised against its own past 60 values (min 20) and clipped at a maximum of 0. It is therefore negative (short) only when the coin is below its close of 30 days ago. Its size grows linearly with the depth of that fall, up to -20. It is 0 when the coin is not down over 30 days. The code keeps the book flat outside the falling calm profile.
Config: 032-01_calm-fall-depth-continues_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bars
- Main measure: On bars where the forecast is not 0, take (-forecast/10) x -(next-day return minus the coin's mean daily return over all windows). This is the gain from the graded short above holding the coin's drift, before costs. Report its mean and t, with same-day cases across coins summed into one.
- Supporting check: On the same bars, the mean next-day excess return of the deepest third of 30-day falls (most negative forecast) minus that of the shallowest third must be below 0.
- Confirm: The main measure's mean is positive with t ≥ 2, and the supporting check passes.
- Reject: The main measure's mean is negative with t ≤ -2, meaning larger falls are followed by rebounds against drift.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is a confirming main measure whose check fails. At least 100 distinct days with a non-zero forecast are needed across coins and windows; with fewer, the result is inconclusive.
