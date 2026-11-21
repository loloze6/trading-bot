---
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: a score combining the coin's 28-day return, minus its 1-day return, its closeness to its 90-day high and minus its 30-day volatility -> kept
- Comparison: each signal weighted equally in its known direction, not by weights learned from the past 365 days -> kept
- Outcome: the coin's return over the next 5 days is higher the higher the score -> kept
- Verdict transfer: yes: the forecast is the fixed, equal-weight, known-direction score, and the test asks whether 5-day returns grow with it.
Forecast: Four graded signals, each standardised against its own past values: - the 28-bar percent return, long when it is up; - the 1-bar return, negated, so a fall reads long; - the percent distance of the close below its 90-bar closing high, which is always 0 or below; - the 31-bar standard deviation of returns (30 one-bar returns), negated, so it is always below 0. The last two are about -10 on average after standardising. A constant +10 at weight 2 centres them. Distance then reads positive when the close is nearer the high than usual, and volatility reads positive when it is lower than usual. The forecast is (momentum + reversal + distance + volatility + 20) / 6. Each signal has an equal weight of 1 in its known direction. The forecast is positive when the combined score is above its usual level and negative when it is below. Its size grows with the score, it is clipped at ±20, and it is signed (long and short).
Config: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bars on a non-overlapping 5-bar grid of each window. For each case, take the forecast times the coin's 5-day return minus the coin's mean 5-day return over all its windows. The measure is the t of the mean of these products, pooled over all coins and windows, before costs.
- Supporting check: none
- Confirm: The mean product is positive with t ≥ 2 over at least 500 cases: 5-day returns above the coin's drift grow with the forecast.
- Reject: The mean product is negative with t ≤ -2 over at least 500 cases: returns fall as the score rises.
- Inconclusive: A t between -2 and 2 is inconclusive, as is any result on fewer than 500 grid cases.
