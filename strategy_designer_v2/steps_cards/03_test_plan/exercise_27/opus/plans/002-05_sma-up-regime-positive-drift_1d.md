---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the stretch from the short SMA crossing above the long SMA until the next down-cross -> adapted: "after the up-cross until the down-cross" becomes "while the short SMA is above the long SMA", and the on/off state becomes graded by the size of the spread.
- Comparison: random stretches of the same length -> kept: measured against holding the coin, using its mean return over all windows together.
- Outcome: price rises more often and further over the stretch -> kept: the long position's next-bar returns are compared with holding the coin.
- Verdict transfer: yes: the forecast is long exactly over the idea's up-cross stretches and flat elsewhere, so a confirm or reject of excess return there transfers to the idea.
Forecast: The forecast is the percent spread of the 50-day SMA over the 200-day SMA (the conventional daily cross pair). It is standardised against its own last 200 values, then clipped at 0. It is positive and grows with the spread while the 50-day SMA is above the 200-day SMA, which is the stretch between an up-cross and the next down-cross. It is exactly 0 from a down-cross until the next up-cross. It is never short, because the idea speaks only of up-cross stretches.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On each bar where the forecast is above 0, take the coin's next-bar return minus that coin's mean daily return over all 24 windows together, weighted by the allocation. Pool across coins and compute the mean and its t-statistic. Each bar counts once.
- Supporting check: Compare the share of up next-bars on bars with a forecast above 0 against the coin's up-bar share over all windows. This is a two-proportion z-test, pooled across coins.
- Confirm: The weighted mean excess return is above 0 with t ≥ 2.
- Reject: The weighted mean excess return is below 0 with t ≤ -2. This means up-cross stretches underperform holding, which fits the brief's "marks exhaustion" failure case.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a result based on fewer than 300 pooled bars with a forecast above 0, or one where fewer than 4 coins contribute any such bars.
