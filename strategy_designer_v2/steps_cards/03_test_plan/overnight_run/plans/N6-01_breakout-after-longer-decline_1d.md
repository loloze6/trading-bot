---
idea: N6-01_breakout-after-longer-decline
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close at its highest close of the prior 20 days, while the close is below its close 60 bars earlier -> adapted: the 20-day high threshold becomes a graded range position (top of the 21-close range, current bar included); the 60-bar-decline condition is kept as a regime rule.
- Comparison: the coin's average ten-bar rise -> kept: the criterion measures against the coin's mean 10-bar return pooled over all windows.
- Outcome: a rise over the next ten bars larger than average -> kept: the forward 10-bar return after the largest long positions.
- Verdict transfer: yes: the forecast is largest exactly at 20-day closing highs made inside a 60-bar decline, and its forward 10-bar excess return answers the idea both ways.
Forecast: A regime rule on PriceEvolutionComponent(period 60) selects "trending" when the close is below its close 60 bars earlier (raw value < 0). Otherwise the forecast is flat. In that regime, DonchianBreakoutComponent(period 21) gives the close's position in the range of the current and prior 20 closes: +20 when the close is the highest of them, -20 when it is the lowest. This value is standardised over 60 bars and clipped at 0, so the forecast is long only and the low side of the range gives nothing. It then passes through signed_power with exponent 3 and pivot 20, the strongest graded dead zone the guide allows. Mid-range closes give a forecast near 0. A close at the 20-day high gives up to +20. The size grows smoothly as the close nears the top of its range. The forecast is zero whenever the 60-bar change is 0 or above.
Config: N6-01_breakout-after-longer-decline_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The forward 10-bar close-to-close return after bars with forecast >= 10, minus the coin's mean 10-bar return over all of its test windows pooled. Measured before costs, with qualifying bars within 10 bars of each other counted as one case, pooled across coins.
- Supporting check: Across all bars in the "trending" regime, the correlation between the forecast and the forward 10-bar excess return, using non-overlapping 10-bar samples. It should be positive.
- Confirm: The mean excess return is greater than 0 with t >= 2 over the independent cases.
- Reject: The mean excess return is below 0 with t <= -2 over the independent cases.
- Inconclusive: Any t between -2 and 2, or fewer than 30 independent cases, neither confirms nor rejects.
