---
idea: 041-01_agitated-fall-rise-vs-swing-giveback
brief: 041_falling-agitated-daily-moves-reverse
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: in a falling, agitated market, a one-day rise measured against the coin's 30-day standard deviation of daily returns -> kept: the profile is added by code, and the rise is the day's return over its 30-day std, zero on down days.
- Comparison: the larger the scaled rise, the larger the fall -> kept: the short position grows with the scaled rise.
- Outcome: the price falls over the next day -> kept: 1 bar on daily bars, short side.
- Verdict transfer: yes: the forecast is the idea's scaled rise, inside its profile, judged on the next day's return.
Forecast: The forecast uses one component, VolatilityScaledReturnComponent with period 1 and vol_period 30. It measures the day's return in units of the 30-day standard deviation of daily returns. It is standardised over its own past 60 values. It is clipped at 0, so down days give 0. It is then negated. The forecast is 0 on down days and flat days. On an up day it is negative, and it grows smoothly in size with the rise in usual moves, up to -20. It is never long. The profile (falling agitated) is added by code, so the book is flat outside that profile.
Config: 041-01_agitated-fall-rise-vs-swing-giveback_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast < 0, take the next-bar return close[t+1]/close[t]-1 minus the coin's mean daily return over all windows. Regress it on abs(forecast). The measure is the slope's t, with the cases of one day taken together.
- Supporting check: On those same bars, the mean next-bar return minus the coin's drift is below 0, measured before costs.
- Confirm: The slope is ≤ 0 with t ≤ -2, so larger scaled rises are followed by larger falls than drift. The supporting check must also pass. At least 100 cases are required.
- Reject: The slope has t ≥ +2, so larger scaled rises are followed by relatively higher next-day returns.
- Inconclusive: Any slope t between -2 and +2 is inconclusive. A slope t ≤ -2 whose mean next-day excess return is not below 0 is also inconclusive. Fewer than 100 cases (bars with forecast < 0) is inconclusive, whatever the t.
