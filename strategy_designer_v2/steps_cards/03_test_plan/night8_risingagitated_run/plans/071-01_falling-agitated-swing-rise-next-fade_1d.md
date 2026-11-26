---
idea: 071-01_falling-agitated-swing-rise-next-fade
brief: 071_falling-agitated-scaled-rise-next-day-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 503ce793b4fe
---
Fidelity:
- Situation: a coin's one-day rise, in units of its own 20-day daily swing, inside a falling, agitated market -> kept: the 1-bar return over the 20-bar standard deviation of daily returns, up days only; the profile is added by code.
- Comparison: the rise against the coin's own 20-day daily swing -> kept
- Outcome: a larger fall over the next day, larger for larger scaled rises -> kept: a short held for 1 bar, its size growing with the scaled rise.
- Verdict transfer: yes: the forecast is the idea's graded scaled rise, shorted for one day only in the stated profile, so confirming or rejecting it confirms or rejects the idea.
Forecast: One component, VolatilityScaledReturnComponent (period 1, vol_period 20). It gives the day's return divided by the standard deviation of the last 20 daily returns. It is standardised over its past 60 values (min_periods 20) and clipped at 0, so only up days count. It is then negated, so the forecast is never positive. The forecast is 0 on down and flat days. On up days it is negative, and its size grows in proportion to the rise in usual moves, up to a cap of -20. Code adds the falling-agitated profile, and the book is flat outside it.
Config: 071-01_falling-agitated-swing-rise-next-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The cases are the bars with forecast below 0, pooled over all coins and windows. On those bars, fit the slope of the next-day excess return on the forecast's size (abs(forecast)). The next-day excess return is close[t+1]/close[t] - 1, minus the coin's mean daily return over all windows. Report the slope's t, with the cases of one day taken together.
- Supporting check: On the same bars, the mean next-day excess return is below 0.
- Confirm: The slope has t ≤ -2 (larger scaled rises are followed by larger falls than the coin's drift), and the supporting check passes.
- Reject: The slope has t ≥ +2 (larger scaled rises are followed by larger next-day gains).
- Inconclusive: A slope t between -2 and +2 is inconclusive. A slope t ≤ -2 with a mean excess return not below 0 is also inconclusive. So is any result with fewer than 100 cases or fewer than 60 distinct days.
