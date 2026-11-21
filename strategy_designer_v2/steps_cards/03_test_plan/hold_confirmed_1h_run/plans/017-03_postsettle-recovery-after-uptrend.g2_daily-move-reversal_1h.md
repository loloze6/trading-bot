---
idea: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: the coin's own past 1-day return -> kept: the 24-bar return of the coin's own closes.
- Comparison: that move relative to the coin's recent volatility -> kept: the return divided by the recent usual 1-bar move times sqrt(24).
- Outcome: the next 1-day return runs against the past move, growing with its size -> kept: the position is opposite and proportional, held over 24 bars.
- Verdict transfer: yes: the forecast is exactly the volatility-scaled past-day return with its sign reversed, so its gains over the next day show the claim directly.
Forecast: The forecast is the coin's 24-bar (1-day) return divided by its usual move. The usual move is the standard deviation of the last 168 one-bar returns times sqrt(24). This value is standardised against its own past 168 values and negated. The forecast is short after a rise and long after a fall. Its size grows in proportion to how large the past day's move was in units of recent volatility, and it is near zero when the past day was flat. It is active on every bar, with no regime and no dead zone, because the idea is a steady proportional relation.
Config: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use non-overlapping bars at positions 0, 24, 48, ... of each window. On each, take forecast/10 x (the coin's next-24-bar return minus that coin's mean 24-bar return over all windows), pooled over coins and windows. Report the ordinary t of its mean and the number of cases.
- Supporting check: The same product, averaged over the third of cases with the largest |forecast|, exceeds its mean over the third with the smallest |forecast|.
- Confirm: The mean is positive with t >= 2, and the supporting check passes.
- Reject: The mean is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 when the supporting check fails. At least 500 non-overlapping cases are required; with fewer, the result is inconclusive.
