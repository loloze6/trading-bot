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
- Situation: the stretch from an upward cross of the short SMA over the long SMA until the next downward cross -> adapted: "after the up-cross, until the down-cross" becomes "while the short SMA is above the long SMA", and that on/off state is graded by the size of the spread.
- Comparison: random stretches of the same length -> kept: compared with simply holding the coin, using its mean return over all windows pooled.
- Outcome: price rises more often and further over the stretch -> kept: the coin's return on each bar of the stretch, measured both as how often it rises and by how much.
- Verdict transfer: yes: the forecast is positive on exactly the bars between an up-cross and the next down-cross, so a real excess return there confirms the idea and a real shortfall rejects it.
Forecast: The forecast is the 50/200-day SMA spread, (SMA50 − SMA200) / SMA200 in percent. This is the most common daily-bar convention for a golden cross. The spread is standardised against its own past 200 values, so a spread of average size gives a forecast of about +10. It is then clipped at 0, because the idea concerns only the stretches after an up-cross. The forecast is positive and grows with the spread while SMA50 is above SMA200. It falls smoothly to 0 at the cross and stays 0 while SMA50 is below SMA200. It never goes short.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: For each bar, the next-bar coin return times the allocation (forecast / 10), minus the same allocation times the coin's mean daily return. That mean is taken over all 24 windows pooled, per coin. The excess is then pooled across coins and windows, and judged by its t-statistic, before costs. One-bar returns do not overlap.
- Supporting check: Compare the share of next-bar returns that are positive on bars with forecast > 0 against the share over all bars of the same coin, pooled across windows. This checks the "more often" part of the idea.
- Confirm: The pooled mean excess return is positive with t ≥ 2, and the up-bar share on forecast > 0 bars is higher than the coin's overall up-bar share.
- Reject: The pooled mean excess return is negative with t ≤ −2, meaning returns during up-cross stretches fall short of holding, as when the cross marks exhaustion.
- Inconclusive: Any t between −2 and 2, including results near zero. A result is also inconclusive if there are fewer than 500 pooled bars with forecast > 0, or fewer than 15 distinct up-cross stretches across all coins.
