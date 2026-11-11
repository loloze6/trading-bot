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
- Situation: short moving average above the long one, from the up-cross to the down-cross -> adapted: "from cross to cross" becomes "while SMA50 is above SMA200", and the on/off state is graded by the spread's size.
- Comparison: random spans of the same length -> adapted: the coin's unconditional return over the same windows, which is what random spans average to.
- Outcome: price rises over the span, more often and further -> kept: forward coin return and its hit rate while the state holds.
- Verdict transfer: yes: the long position exists exactly while the short average is above the long one, so excess return there tests the idea both ways.
Forecast: The forecast uses the SMA50-minus-SMA200 spread as a percent of SMA200 (EMASpreadComponent, average "sma", 50/200, the usual daily cross). It is standardised against its own past 200 values and clipped at 0. It is positive and grows with the spread while SMA50 is above SMA200, which is the span from an up-cross to the next down-cross. It is zero (flat) while SMA50 is below SMA200. It never goes short, because the idea concerns only up-cross spans.
Config: 002-05_up-cross-to-reverse-cross-gain_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Mean 20-bar forward coin return after bars with forecast > 0, minus the mean 20-bar forward return of all bars in the same coin-windows. Use non-overlapping 20-bar blocks, pooled over coins and windows, before costs.
- Supporting check: Share of positive 20-bar forward returns when forecast > 0, against the unconditional share in the same windows.
- Confirm: The excess return is above 0 with t ≥ 2, counting non-overlapping blocks only.
- Reject: The excess return is below 0 with t ≤ -2, meaning moves during up-cross spans underperform or reverse.
- Inconclusive: Any t between -2 and 2, or fewer than 30 non-overlapping 20-bar blocks with forecast > 0.
