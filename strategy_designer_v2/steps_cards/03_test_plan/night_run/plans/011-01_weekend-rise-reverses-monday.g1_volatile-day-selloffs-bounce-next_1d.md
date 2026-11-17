---
idea: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a one-day fall that is large in units of the coin's usual daily move over the past 60 days -> adapted: "large" made graded, a cubic dead zone on the vol-scaled one-day fall.
- Comparison: the fall against the usual daily move (std of 60 daily returns) -> kept.
- Outcome: the coin rises over the next 1 day, more for larger falls and more when 60-day volatility is higher; nothing after rises -> kept: long-only after falls, with the volatility part tested in the supporting check.
- Verdict transfer: yes: the forecast is the vol-scaled fall itself, and the volatility strengthening is part of the confirm rule.
Forecast: The forecast starts from VolatilityScaledReturnComponent (period 1, vol_period 60), which gives today's return divided by the std of the last 60 daily returns. It is standardised over its own past 60 values (min_periods 20), negated so that falls are positive, and clipped at 0 so that rises give no position. A cubic graded dead zone (signed_power, exponent 3, pivot 20) then keeps ordinary falls near 0 and lets the long position grow steeply with the size of the fall. The forecast is never negative and is 0 on up days. The regime detector is ungated.
Config: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take the bars with forecast >= 5 (falls of roughly 1.3 or more usual moves). On each, measure the next-bar return close[t+1]/close[t]-1 minus that coin's mean daily return over all windows. Report the mean of this excess, pooled over coins and windows, and its ordinary t over the independent bars.
- Supporting check: Split the main measure's cases at the pooled median of the 60-day std of daily returns, recomputed from closes. The mean excess in the high-volatility half minus the low-volatility half must be > 0.
- Confirm: The main mean excess is > 0 with t >= 2, and the supporting check's difference is > 0.
- Reject: The main mean excess is < 0 with t <= -2.
- Inconclusive: Either of these is inconclusive: - t between -2 and 2; - t >= 2 but the high-volatility minus low-volatility difference is <= 0. At least 100 cases with forecast >= 5 are needed (and at least 30 per volatility half); with fewer, the result is inconclusive.
