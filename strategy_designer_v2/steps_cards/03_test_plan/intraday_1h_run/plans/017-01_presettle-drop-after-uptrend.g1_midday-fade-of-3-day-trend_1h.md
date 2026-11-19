---
idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's 3-day return, read when the hour starting 12:00 UTC begins -> kept: 72-bar return, active only on the bar whose coming bar starts at 12:00 UTC.
- Comparison: none (the idea is a graded relation, a larger 3-day return gives a lower next-hour return) -> kept
- Outcome: the return over the 1 hour after 12:00 UTC runs against the 3-day return, larger for a larger trend -> kept: the position is held for 1 bar, from the 12:00 close to the 13:00 close.
- Verdict transfer: yes: the test bets against the 3-day return, sized to it, over exactly that hour, so its gain or loss is the idea's prediction.
Forecast: A clock regime is active only on the bar whose coming bar starts at 12:00 UTC (HourOfDayComponent = 12). On that bar, the forecast is the negated 72-bar percent return (PriceEvolutionComponent, period 72). It is standardised against its past 72 values (window 72, min_periods 20). It is short after a 3-day rise and long after a 3-day fall, and its size grows linearly with the size of the 3-day move. It is zero when the 3-day return is zero, and zero on every other hour, so the position lasts only the hour from 12:00 to 13:00 UTC.
Config: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The sample is every bar with regime "trending" (one bar per coin per day). On each, take postRebalance_current_allocation × (close[t+1]/close[t] − 1 − the coin's mean 1-bar return over all its windows). Pool these across coins and windows and compute the ordinary t of their mean. This is the timing gain against simply holding the coin, before costs.
- Supporting check: The same mean excess gain is positive in at least 4 of the 6 coins.
- Confirm: Pooled mean excess gain > 0 with t ≥ 2, and the supporting check passes.
- Reject: Pooled mean excess gain < 0 with t ≤ −2.
- Inconclusive: Any t between −2 and 2, or t ≥ 2 with the coin check failing. At least 500 hour-12 cases with a nonzero position are needed; about 17,000 are expected (6 coins × 24 windows × ~122 days).
