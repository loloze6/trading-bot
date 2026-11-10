---
idea: 002-06_sma-down-regime-negative-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA under long SMA, from a down cross until the next up cross -> adapted: the on/off "below" state is made graded, sized by how far the 50-day SMA sits under the 200-day SMA, and zero while it is above.
- Comparison: random stretches of the same length -> kept: active bars are compared with all bars of the coin, which is the same as comparing with holding it.
- Outcome: price falls more often and further until the opposite cross -> kept: the bar-by-bar short return over the stretch, which ends at the up cross.
- Verdict transfer: yes: the short is held on exactly the bars between a down cross and the next up cross, so the stretch's fall is what the test measures.
Forecast: The 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA (convention on daily bars: 50/200). It is standardised against its own past 200 values, then clipped at a maximum of 0. It is negative (short) only while the 50-day average is below the 200-day average. The short grows with the gap, up to a forecast of -20. It is zero from the up cross until the next down cross.
Config: 002-06_sma-down-regime-negative-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars where the forecast is below 0, take the next bar's coin return minus the coin's mean bar return over all tested bars. Weight each by |forecast| and give the t-statistic of the weighted mean, pooled over the 6 windows. Each bar is counted once.
- Supporting check: Share of down bars on active bars against the share over all bars (binomial z), unweighted, testing the "more often" part.
- Confirm: The weighted excess return is negative, so the short gains beyond the coin's own drift, with t ≤ -2.
- Reject: The weighted excess return is positive, so prices rise more than usual during down-cross stretches, with t ≥ +2.
- Inconclusive: Any t strictly between -2 and +2. The result is also inconclusive with fewer than 100 active bars, or fewer than 2 separate down-cross stretches, across the 6 windows.
