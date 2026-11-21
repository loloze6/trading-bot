---
idea: 021-02_below-falling-cloud-continues-down
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a31b77de3651
---
Fidelity:
- Situation: the coin closes below its Ichimoku cloud and the cloud is falling -> kept: a regime rule requires both a close below the cloud bottom and a negative cloud slope.
- Comparison: the return is more negative the faster the cloud has fallen over the past 26 days -> kept: the short size grows with the cloud's 26-bar fall.
- Outcome: the return over the next 26 days is negative -> kept: the horizon is 26 bars, on the short side.
- Verdict transfer: yes: the test measures the same condition, the same grading and the same 26-day return the idea states.
Forecast: The regime detector reads two values. The first is the Ichimoku cloud position (9/26/52/26, edge "nearest", base "close"), which is negative only when the close is below the cloud. The second is the Ichimoku cloud slope (9/26/52/26, lookback 26), which is the percent change of the cloud's mid level over 26 bars. When both are below 0, the bar is labelled "trending". On those bars the forecast is the cloud slope over 26 bars, standardised against its own past 104 values. Inside this regime the slope is always negative, so the forecast is a short that grows with the speed of the cloud's fall. A cloud's usual 26-bar fall gives about -10, and the cap is -20. On every other bar the forecast is 0: when the close is at or above the cloud bottom, or when the cloud is flat or rising.
Config: 021-02_below-falling-cloud-continues-down_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: The cases are the bars on a non-overlapping 26-bar grid of each window where the forecast is below 0. For each case, take the coin's 26-bar return minus its mean 26-bar return over all windows, signed for a short. The measure is the mean of these values over the cases, with its t-statistic.
- Supporting check: Across the cases, the slope of that short-signed excess return on |forecast| is above 0.
- Confirm: The main measure's mean is above 0 with t >= 2 over at least 30 cases, and the supporting slope is above 0.
- Reject: The main measure's mean is below 0 with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 with a supporting slope at or below 0, and so is any result with fewer than 30 cases.
