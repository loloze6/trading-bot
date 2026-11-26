---
idea: 058-02_choppy-agitated-weekly-fall-continues
brief: 058_choppy-agitated-weekly-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a choppy agitated market, the coin's 7-day return is a fall -> kept: the profile is added by code, and the 7-day return clipped at zero gives no position unless it is a fall
- Comparison: the size of the fall against the coin's usual daily swing over the past 30 days -> kept: the 7-day return is divided by the standard deviation of the past 30 daily returns
- Outcome: the coin falls further over the next 7 days, more after a larger scaled fall -> kept: a short position graded by the scaled fall, held for 7 bars
- Verdict transfer: yes: the forecast is short only after a 7-day fall in the named profile and grows with the vol-scaled fall, so its gains test both the continuation and the grading.
Forecast: The forecast is the coin's 7-day return divided by its usual move. The usual move is the standard deviation of its last 30 daily returns times sqrt(7), from `VolatilityScaledReturnComponent` with period 7 and vol_period 30. This value is standardised against its own past 60 values (target 10, cap 20), then clipped at a maximum of 0. It is negative (short) only when the past 7 days fell, and zero after a flat or rising week. Its size grows linearly with the depth of the fall in usual moves, up to -20. Code adds the choppy-agitated profile, so the book is flat outside it.
Config: 058-02_choppy-agitated-weekly-fall-continues_1d_config.json
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: The unusual move per case, in the short direction. A case is a short bet (the forecast falls by at least 2 points), read once per 7-bar grid cell. The unusual move is the coin's return over the next 7 bars minus its normal 7-bar drift (from holding the coin), with the sign flipped for a short. Its t takes the cases of one day together.
- Supporting check: Split the cases at the median of |forecast|. The cases with the larger |forecast| must have a mean short-direction unusual move above that of the smaller half (difference larger minus smaller > 0).
- Confirm: The mean short-direction unusual move is > 0 with t >= 2, and the supporting check passes.
- Reject: The mean short-direction unusual move is < 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming main measure whose check fails, and any result from fewer than 30 cases.
