---
idea: 089-04_calm-decline-up-volume-lasting
brief: 089_falling-calm-up-volume-lean
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: b5764dedf919
---
Fidelity:
- Situation: in a falling, calm market, the share of the last 20 days' volume traded on up days -> kept: the 20-bar up-day volume share; the falling calm profile is added by code.
- Comparison: the larger the share, the larger the rise -> adapted: graded long from an even split (share 0.5) upward, since the brief is long only.
- Outcome: the coin rises over the next 10 days, the rise building rather than fading -> kept: the 10-bar forward return, plus its second half.
- Verdict transfer: yes: the test measures this share and this 10-day rise inside this profile, and a rise that grows with the share confirms the idea while one that falls with it rejects it.
Forecast: One component, the share of the last 20 daily bars' volume traded on up-close days, minus 0.5 (`UpDayVolumeShareComponent`, period 20, form "centred"). It is standardised against its own past 60 values, so a typical lean reads about 10. It is then clipped at 0, so the book stays long only. The forecast is 0 when volume is split evenly or leans to down days. It is positive and grows in proportion as more of the volume falls on up days, capped at 20. The code holds it only on bars in the falling calm profile and keeps it flat elsewhere.
Config: 089-04_calm-decline-up-volume-lasting_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 10 bars
- Main measure: On the non-overlapping 10-bar grid of each window, take the cases with forecast > 0. For each case, take the coin's 10-bar return from that close minus the coin's mean 10-bar return over all windows. Measure the slope of that excess return on the forecast, with cases of the same day taken together.
- Supporting check: The mean excess return of those cases over bars t+5 to t+10, weighted by the forecast, is above 0 (the rise builds rather than fades).
- Confirm: The slope is positive with t >= 2 and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with |t| < 2, or a positive slope with t >= 2 whose second-half check fails. A verdict needs at least 30 cases on at least 30 distinct days.
