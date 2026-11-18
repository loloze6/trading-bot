---
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a coin's fall over the last 1 day, larger or smaller -> kept: the 1-bar percent return, kept only when negative, sized by the size of the fall.
- Comparison: larger falls against smaller falls -> kept: the position grows with the fall, so the outcome is compared across fall sizes.
- Outcome: the next 1-day return is higher, upward -> kept: the 1-bar forward return, judged against the coin's average day.
- Verdict transfer: yes: the forecast is the idea's own graded relation at its own 1-day horizon, so a confirm or reject of the slope is a confirm or reject of the idea.
Forecast: The forecast uses one indicator, the 1-day percent close-to-close return (PriceEvolutionComponent, period 1). It is standardised over the past 60 days, so a typical daily move reads about 10. Its sign is then flipped so that a fall reads positive. Finally it is clipped at 0, so up days give 0 (flat). After a fall the forecast is long and grows in proportion to the size of the drop, up to the cap of 20 for a drop about twice the usual daily move. It is never negative.
Config: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of each bar's next-day excess return on its forecast, pooled over all coins and windows, with its t-statistic. - The excess return is close[t+1]/close[t] - 1 minus that coin's mean daily return over all windows. - Only bars with forecast > 0 are used, one case per bar, never across windows. - Before costs.
- Supporting check: The book's timing gain must be above 0. This is its mean daily return minus the gain from the market's own rise.
- Confirm: The slope is positive with t >= 2, and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is t >= 2 with a failed supporting check. At least 300 bars with forecast > 0 are required; fewer is inconclusive.
