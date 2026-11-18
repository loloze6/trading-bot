---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: the close makes a new 30-day low -> kept: a regime rule on the close's distance below the lowest of the prior 30 closes (below 0).
- Comparison: 14-day RSI now is above the RSI at the previous low in the 30-day window -> adapted: graded as RSI now minus RSI at the earlier lowest close, positive part only.
- Outcome: the price rebounds over the next 10 days, more when the RSI gap is wider -> adapted: the position is held while on the new-low bar, and the 10-day hold is dropped and moved to the criterion's horizon.
- Verdict transfer: yes: the test measures the idea's exact situation and its graded comparison against the next 10 days' return, using only the allowed adaptations.
Forecast: The forecast is active only on bars where the close is below the lowest of the prior 30 closes. On those bars it equals RSI(14) now minus RSI(14) at the lowest close among bars t-30..t-4. It is standardised against its own past values (window 60, min_periods 20) and clipped at 0. It is positive and grows with how far the RSI sits above its earlier trough. It is 0 when there is no divergence and on every bar that is not a new 30-day low. It is never short.
Config: 005-02_bullish-rsi-divergence-rebound_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Cases are the bars with forecast > 0, counted once per coin-window: a case is skipped if it falls within 10 bars after an earlier counted case. For each case, x = (forecast/10) × (close[t+10]/close[t] − 1 − the coin's mean 10-bar return over all windows). The measure is the ordinary t of the mean of x, before costs.
- Supporting check: Among regime bars, the mean 10-bar forward return of the divergence cases (forecast > 0) minus that of the new-low cases with forecast 0 is above 0. Both sets are counted with the same non-overlap rule.
- Confirm: The mean of x is > 0 with t ≥ 2 over at least 30 independent cases, and the supporting difference is > 0.
- Reject: The mean of x is < 0 with t ≤ −2 over at least 30 independent cases.
- Inconclusive: Any t between −2 and 2 is inconclusive, as is a confirming t with a supporting difference ≤ 0. Fewer than 30 independent cases across all coins and windows is also inconclusive.
