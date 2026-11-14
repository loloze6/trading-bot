---
idea: 002-06_down-cross-to-reverse-cross-loss
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short moving average below the long one, from the down-cross until the up-cross -> adapted: "after the cross" made "while below", and the on/off state made graded by how far the short SMA sits below the long one.
- Comparison: random spans of the same length -> kept: the coin's mean return over all bars of all windows.
- Outcome: price falls over the span, more often and further -> kept: the coin's return on bars where the short SMA is below the long one, short side.
- Verdict transfer: yes: the test measures the return of exactly the below-cross spans against all bars, so it judges the same claim.
Forecast: The forecast uses the percent spread of the 50-day SMA over the 200-day SMA, which is the conventional daily "death cross" pair. It is standardised against its own past 200 values, then clipped at a maximum of 0. It is negative (short) only while the 50-day SMA is below the 200-day SMA, and it gets larger the further below it sits. It is 0 whenever the 50-day SMA is at or above the 200-day SMA. It never goes long, because the idea concerns only the down-cross spans.
Config: 002-06_down-cross-to-reverse-cross-loss_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars where the forecast is below 0, take the next 1-bar return of the coin minus the coin's mean 1-bar return over all 24 windows together. Flip its sign, weight it by |forecast|, and pool across coins. Report the mean and its t-statistic, with each bar counted once.
- Supporting check: Among bars where the forecast is below 0, the share whose next-bar return is below the coin's all-window mean return, compared with 50% using a binomial z.
- Confirm: The weighted mean excess short return is above 0 with t ≥ 2, so prices fall further than over random spans.
- Reject: The weighted mean excess short return is below 0 with t ≤ -2, so prices rise relative to holding during the below-cross spans, which reads as reversal.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a pooled count below 300 bars with forecast below 0.
