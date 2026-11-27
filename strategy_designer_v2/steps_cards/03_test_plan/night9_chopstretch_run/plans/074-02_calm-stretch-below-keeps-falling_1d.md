---
idea: 074-02_calm-stretch-below-keeps-falling
brief: 074_agitated-stretch-below-average-rebounds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: the coin's close sits below its 20-day average, in a calm market -> kept: the calm market is the brief's profile, which code adds; the close's distance below the 20-day SMA is measured as stated.
- Comparison: the distance measured in units of the 20-day std of daily returns -> kept: `MovingAverageDistanceComponent` with `base` "usual_moves" and `vol_period` 20.
- Outcome: the further below the average, the more it keeps falling over the next 10 days -> kept: the short is graded by depth and held 10 bars.
- Verdict transfer: yes: the forecast is the idea's own graded measure inside the idea's own profile, so a confirm or a reject applies to the idea itself.
Forecast: One component, `MovingAverageDistanceComponent` (`period` 20, `average` "sma", `base` "usual_moves", `vol_period` 20). It gives (close − SMA20) / SMA20 divided by the 20-day std of daily returns: the distance from the average in usual daily moves. It is standardised over 60 bars (min_periods 20), so a typical size is about 10. It is then clipped at a maximum of 0, so only the below-average side remains. The forecast is 0 at or above the average and negative below it, which is a short. The short grows linearly with the depth below the average, up to the cap of −20. Code keeps the book flat outside calm markets.
Config: 074-02_calm-stretch-below-keeps-falling_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 10 bars
- Main measure: The data is a non-overlapping 10-bar grid in each window, using the grid cells where the forecast is below 0. On those cells, regress the coin's next-10-bar return, minus its normal 10-bar drift over all windows, on the forecast. The result is the t of the slope (positive means a deeper stretch is followed by a larger fall).
- Supporting check: On those same cells, the mean drift-removed 10-bar return in the signal's direction (the idea's strength) is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is −2 or less: a deeper stretch is followed by a larger rise.
- Inconclusive: The slope's t lies between −2 and 2, or the slope confirms but the check fails. A test with fewer than 100 grid cells with a negative forecast is inconclusive whatever the result.
