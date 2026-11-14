---
idea: 002-05_up-cross-to-reverse-cross-gain
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the span from the short MA's upward cross to its downward cross -> adapted: "after the cross until the opposite cross" becomes "while the 50-day SMA is above the 200-day SMA", graded by the size of the gap.
- Comparison: random spans of the same length -> kept: measured against simply holding the coin over all bars.
- Outcome: price rises over the span, more often and further -> kept: the coin's return on the bars that follow, while the position is long.
- Verdict transfer: yes: the up-cross span is exactly the state of the short SMA being above the long one, and holding stands in for random spans.
Forecast: The 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA, standardised against its own past 200 values. Values below zero are clipped to zero, because the idea is about up-cross spans only. The forecast is zero while the short SMA is below the long one, and turns positive from the up-cross onwards. It grows with the gap between the averages, up to the cap of 20, and returns to zero at the down-cross. No regime is used.
Config: 002-05_up-cross-to-reverse-cross-gain_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The mean next-bar return of the coin on bars where the forecast is above 0, minus the coin's mean next-bar return over all bars of all windows together. Coins are pooled. The t-statistic uses Newey-West errors with 10 lags, so that bars within the same span are not counted as independent.
- Supporting check: The share of up bars while the forecast is above 0, compared with the share of up bars over all bars. A binomial z-test is run, with each coin's baseline taken from its own pooled data.
- Confirm: The excess mean return is above 0 with t >= 2. The up-bar share should also be higher, with z >= 2.
- Reject: The excess mean return is below 0 with t <= -2. In that case returns during the cross spans are lower than when holding, which is the brief's "crosses mark exhaustion".
- Inconclusive: Any t between -2 and 2 is inconclusive, including a result near zero. A verdict also needs at least 30 distinct up-cross spans pooled across coins and at least 1000 bars with a positive forecast; fewer is inconclusive.
