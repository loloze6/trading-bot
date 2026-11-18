---
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: close makes a new 30-day low while the 14-day RSI is above its reading at the previous low in that window -> kept, as a regime rule: close below its prior 30-close low and RSI(14) now minus RSI at the earlier lowest close above 0.
- Comparison: rebound size grows with how far the RSI stays above its earlier trough and with how deep the 30-day decline into the low was -> adapted: the on/off condition is graded as the equal-weight mean of the standardised RSI gap and the standardised 30-day fall.
- Outcome: price rebounds (rises) over the next 20 days, not just the next day -> adapted: "after X" becomes "while X" and the holding period is dropped; the criterion reads the 20-bar return from the recorded closes.
- Verdict transfer: yes: the bars where the divergence regime holds and the forecast's size are the idea's situation, and their 20-bar forward returns against holding are the idea's outcome.
Forecast: The forecast is computed only on bars where the close is below the lowest of the prior 30 closes and the 14-day RSI is above its value at the earlier 30-day lowest close (the lowest close among bars t-30..t-4). On those bars it is the equal-weight mean of two values: - the RSI gap (RSI now minus RSI at the earlier low), standardised over its past 60 values; - the 30-day fall (the negated 30-bar percent change), standardised over its past 60 values. Both values are positive on these bars, so the forecast is long and grows with both the RSI gap and the depth of the fall. A clip at 0 keeps it long-only. On every other bar the forecast is 0.
Config: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The 20-bar forward return close[t+20]/close[t]-1 is taken from bars with forecast > 0, minus the coin's mean 20-bar return over all its windows. - Only bars with t+20 inside the same window count. - Events are taken without overlap: the first positive-forecast bar starts an event, and later positive bars within the next 20 bars are skipped. - The measure is the ordinary t of the mean excess, before costs.
- Supporting check: The Spearman correlation between the event's forecast and its 20-bar excess return is above 0.
- Confirm: The mean excess 20-bar return is above 0 with t ≥ 2 over at least 30 events, and the Spearman correlation is above 0.
- Reject: The mean excess 20-bar return has t ≤ -2 over at least 30 events.
- Inconclusive: Any of these is inconclusive: - t between -2 and 2; - t ≥ 2 but the Spearman correlation is 0 or below; - fewer than 30 non-overlapping events across all coins and windows.
