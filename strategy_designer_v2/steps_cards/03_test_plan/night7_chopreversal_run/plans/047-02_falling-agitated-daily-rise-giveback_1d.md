---
idea: 047-02_falling-agitated-daily-rise-giveback
brief: 047_falling-agitated-two-way-daily-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e8f4c1171351
---
Fidelity:
- Situation: a coin's one-day percent rise in a falling, agitated market -> kept: the profile is added by code, and the forecast is non-zero only on bars whose one-day return is positive.
- Comparison: the larger the rise, the larger the next-day fall -> kept: the short grows linearly with the day's rise.
- Outcome: the price falls over the next day -> kept: short over a 1-day horizon, which is 1 bar.
- Verdict transfer: yes: the forecast is the idea's short, sized by the rise, held one day, and only inside the profile.
Forecast: One component, the 1-bar percent return (`PriceEvolutionComponent`, `period` 1). It is standardised against the mean absolute size of its past 60 daily returns. A `clip` with `min` 0 keeps only up days, and `negate` turns the rise into a short. On a down or flat day the forecast is exactly 0. On an up day it is negative, and its size grows linearly with the rise, about -10 for a rise of usual size, down to the cap of -20. It is never positive.
Config: 047-02_falling-agitated-daily-rise-giveback_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Over bars with forecast < 0 (up days inside the profile), regress the coin's next-day excess return on the forecast (`post_pipeline_value`) by least squares. The excess return is close[t+1]/close[t]-1 minus the coin's mean daily return over all windows. Standard errors are clustered by day, and returns stay within each window. A positive slope means larger rises are followed by larger falls.
- Supporting check: The mean next-day excess return over the same bars, taken in the short direction (negated), is above 0.
- Confirm: The slope is > 0 with t >= 2, and the supporting check passes.
- Reject: The slope is < 0 with t <= -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive, and so is a positive slope with t >= 2 whose supporting check fails. The test also needs at least 100 cases (bars with forecast < 0) spread over at least 50 distinct days; with fewer, the result is inconclusive.
