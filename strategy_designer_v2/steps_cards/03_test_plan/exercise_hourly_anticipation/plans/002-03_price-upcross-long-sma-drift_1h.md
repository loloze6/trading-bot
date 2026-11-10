---
idea: 002-03_price-upcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: price has just closed above its long average after being below it -> adapted: "after the up-cross" becomes "while above", graded by the percent distance of the close above its 200-bar SMA.
- Comparison: random points -> kept: forward returns on active bars are compared with forward returns on all bars, which is what holding the coin earns.
- Outcome: price keeps rising, more often and further -> kept: the forward return of BTC over the next bars while the position is long.
- Verdict transfer: yes: an up-cross puts the close above the SMA, so an uptrend that persists after the cross shows as excess returns while the close is above the average, and a reversal after the cross shows as a deficit.
Forecast: The percent distance of the close from its 200-bar SMA, which includes the current close. It is standardised against its own past 200 values (target 10, cap 20) and clipped at 0. The forecast is 0 while the close is at or below the SMA and turns positive as soon as the close crosses above it. It grows smoothly as the close moves further above the average, relative to how far it usually sits, up to a cap of 20. It is never negative, because the idea is about up-crosses only.
Config: 002-03_price-upcross-long-sma-drift_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The 24-bar forward return of BTC on bars where the forecast is above 0, minus the 24-bar forward return over all bars of the same window (holding the coin). Bars are sampled every 24th bar so that overlapping returns count once. Results are pooled across the 6 windows.
- Supporting check: Take the bars where the forecast first turns from 0 to above 0 (the fresh up-crosses). Their 24-bar forward return minus the all-bar mean should be positive, and they should be up more often than all bars are.
- Confirm: The pooled excess mean is above 0 with t ≥ 2, it is positive in at least 4 of the 6 windows, and the supporting check is also positive.
- Reject: The pooled excess mean is ≤ 0. A pooled excess with t ≤ -2, which means moves reverse after crosses, rejects strongly.
- Inconclusive: A pooled excess that is positive but with t < 2, or positive in fewer than 4 windows, or a supporting check that disagrees with the main measure. The test needs at least 150 non-overlapping active samples pooled and at least 30 fresh up-crosses. With fewer, the test is inconclusive.
