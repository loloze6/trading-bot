---
idea: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a close above the prior 20-day high, a push above it, then within 3 days a close back below the old high -> kept: the breakout bar is found within the last 4 bars (failure up to 3 days after it), and its push above the high is part of every such breakout.
- Comparison: the breakout day's volume against its 20-day average, and only a low ratio counts -> adapted: "only when low" becomes graded thinness, max(0, 1 − ratio), so a lower ratio gives a larger short.
- Outcome: the coin falls over the next 5 days -> kept: each short is held 5 daily bars.
- Verdict transfer: yes: the forecast is short exactly on thin-volume failed breakouts and sized by their thinness, so the test's 5-day result is the idea's result.
Forecast: The forecast uses one indicator, `FailedBreakoutVolumeRatioComponent`, with these settings: - prior high: the highest high of the 20 days before the breakout day; - breakout day: the most recent close above that high, within the last 4 bars; - failure: today's close is back below that high; - volume: the breakout day's volume against its 20-day mean, in the "thin" form, max(0, 1 − ratio). The reading is standardised over its last 500 values (at least 120 needed) and negated. The forecast is therefore: - negative (short) only on a failed breakout whose breakout day traded below its average volume, and larger the thinner that volume; - zero on every other bar: no breakout, no failure, or a breakout day at or above average volume; - never positive (short only).
Config: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short signals: a fall of the forecast of at least 2 points, read once per non-overlapping 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal's close, minus the coin's mean 5-bar return over all windows, signed for a short. The measure is the mean of these unusual moves, with the t of that mean. This is before costs.
- Supporting check: Across the cases, the Spearman correlation between the thinness (`thin_fail.last_history_value`) and the short-signed unusual move is above 0.
- Confirm: The mean short-signed unusual move has t >= 2 over at least 20 cases, and the supporting correlation is above 0.
- Reject: The mean short-signed unusual move has t <= -2 over at least 20 cases, meaning these failures rise more than usual.
- Inconclusive: Any t between -2 and 2, or fewer than 20 cases. A confirming t with a correlation at or below 0 is also inconclusive.
