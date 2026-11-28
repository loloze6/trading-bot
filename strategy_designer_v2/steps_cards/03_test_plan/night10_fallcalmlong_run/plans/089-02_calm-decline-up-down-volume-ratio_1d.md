---
idea: 089-02_calm-decline-up-down-volume-ratio
brief: 089_falling-calm-up-volume-lean
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 5a7846f8b001
---
Fidelity:
- Situation: a falling, calm market, with a coin's 20-day mean up-day volume set against its mean down-day volume -> kept: the falling calm profile is added by code, and inside it the lean is the log ratio over 20 bars.
- Comparison: up-day mean volume against down-day mean volume over the same 20 days -> kept.
- Outcome: the higher the ratio, the more the coin rises over the next 5 days -> kept: the long position grows with the ratio and is held 5 bars (long only, per the brief).
- Verdict transfer: yes: the test measures this ratio, in this profile, at this horizon, so a confirm or a reject applies to the idea itself.
Forecast: The forecast is UpDownMeanVolumeRatioComponent(period 20, form "log"), the natural log of the mean volume of the last 20 days' up days over that of their down days. It is standardised over its past 60 values (min_periods 20), so a lean of usual size reads about 10. It is then clipped at 0 because the brief is long only. The forecast is positive and grows with the ratio when up days trade heavier per day than down days. It is 0 when they trade the same or lighter. Code adds the falling calm profile, so the forecast is 0 on every bar outside it.
Config: 089-02_calm-decline-up-down-volume-ratio_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The forecast-weighted mean 5-bar excess return. It is taken on the non-overlapping 5-bar grid of each window, over the bars with forecast > 0. The excess return is the coin's return over the 5 bars minus the coin's mean 5-bar return over all its windows. Its t clusters the cases of the same day.
- Supporting check: The Spearman correlation between the forecast and the 5-bar excess return over the same cases is above 0.
- Confirm: The weighted mean excess return is above 0 with t ≥ 2, and the Spearman correlation is above 0.
- Reject: The weighted mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t whose Spearman correlation is 0 or below. Fewer than 30 cases with forecast > 0, or cases falling on fewer than 20 distinct days, is also inconclusive.
