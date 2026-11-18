---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a coin's close makes a new 30-day low -> adapted: "after the new low" becomes "while the close is below the prior 30 closes", as a regime.
- Comparison: the smaller its 30-day decline into that low -> kept: graded by the closeness of the close to its 30-day high close, which is larger when the fall from that high is milder.
- Outcome: keeps falling over the next 10 days, short -> adapted: the 10-day holding period is dropped; the position exists only on new-low bars, and the outcome is judged at 10 bars.
- Verdict transfer: yes: the test compares the 10-bar fall after mild-decline new lows with the fall after deep-decline new lows, which is exactly the idea's claim.
Forecast: The regime gate is `DistanceFromHighComponent` (30 bars, extreme low, current bar excluded, percent form). It selects `trending` when the close is below every one of the prior 30 closes; every other bar is flat. On those bars the forecast comes from `DistanceFromHighComponent` (30 closes, bar included, proximity form, power 1), which is 1/(1+D), D being the percent fall from the 30-day high close. It is standardised over its past 60 values and negated. The forecast is therefore always short or zero. It is about -6 to -9 when the new low came after a mild fall from the high, and it shrinks smoothly toward 0 as that fall deepens.
Config: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are `trending` bars, kept in time order within each window. A bar is kept only if it lies at least 10 bars after the last kept case and its next 10 bars lie inside the window. Each case's outcome is its 10-bar return minus the coin's mean 10-bar return over all windows. The measure is the Welch t of the mild group (forecast at or below the cases' median, i.e. more negative) minus the deep group (forecast above the median).
- Supporting check: The mild group's mean excess 10-bar return is below 0.
- Confirm: The Welch t of mild minus deep is -2 or less, and the mild group's mean excess return is below 0.
- Reject: The Welch t of mild minus deep is +2 or more.
- Inconclusive: The idea is neither confirmed nor rejected when the t lies between -2 and +2, or when the t is -2 or less but the mild group's mean excess return is not below 0. At least 20 cases per group (40 in total) are required; with fewer, the result is inconclusive.
