---
idea: 061-01_falling-calm-scaled-rise-fade
brief: 061_falling-calm-rally-next-day-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: a one-day rise, large against its 30-day daily-return standard deviation, in a falling calm market -> adapted: "large" is graded (a damped scaled rise, zero on down days); the falling calm profile is added by code.
- Comparison: the rise against the standard deviation of daily returns over the last 30 days -> kept: the one-day return divided by the 30-day standard deviation.
- Outcome: a fall over the next day, larger the larger the scaled rise -> kept: a 1-bar short whose size grows with the scaled rise.
- Verdict transfer: yes: the forecast is the idea's scaled rise held short for its one-day horizon, so a result on it is a result on the idea.
Forecast: The forecast uses one indicator, `VolatilityScaledReturnComponent` (`period` 1, `vol_period` 30). This is the day's return in 30-day standard deviations of daily returns. Its steps: - It is standardised against its own past 60 values, so an average-sized day reads about 10. - It is clipped at 0, so only up days count. - It is damped by `signed_power` (exponent 2, pivot 10), so small rises give almost nothing and large rises give much more. - It is negated, so the position is short. The forecast is 0 on down and flat days and negative on up days. A rise of about half a usual move gives about -4; a rise of about one standard deviation gives about -15. Larger rises reach the -20 cap. It is never positive. Step 3's code keeps the book flat outside the falling calm profile.
Config: 061-01_falling-calm-scaled-rise-fade_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On every bar with a nonzero position, the gain before costs is the position held after the bar's trade times (the next-day return minus the coin's mean daily return over all windows). Its mean is tested with a t-statistic, cases of the same day summed together. This is the timing gain against simply holding the coin.
- Supporting check: On bars with forecast below 0, regress the next-day excess return (minus the coin's mean daily return) on the forecast, cases of one day summed together. The slope must be positive with a t of 2 or more: a more negative forecast is followed by a larger fall.
- Confirm: The main measure's mean is above 0 with a t of 2 or more, and the supporting check passes.
- Reject: The main measure's mean is below 0 with a t of -2 or less: the positions lose against the coin's drift after scaled rises.
- Inconclusive: Any other result is inconclusive. That covers: - a main t between -2 and 2; - a main t of 2 or more with the slope's t under 2; - fewer than 100 distinct days with a nonzero position across coins and windows.
