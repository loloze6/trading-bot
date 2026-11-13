---
idea: N4-01_breakout-drift-lasts
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
(Orchestrator's sizing diagnostic, not written by step 3: the config of N4-01 with vol_target after standardise.)
Fidelity:
- Situation: a close at the highest of the prior 20 daily closes, on an up day -> adapted: "after X" made "while X", graded by recency; the bars since the last new 20-day closing high count down from 20 to 0 (such a close is always an up day).
- Comparison: the rise continues even when the following days close below the new high -> kept: the countdown ignores later closes below the high.
- Outcome: price keeps rising over the next ten or more days -> kept: long while the countdown runs, judged on the 10-bar forward return.
- Verdict transfer: yes: the forecast is long only in the 20 days after a new closing high, so a drift there confirms the idea and a reversal there rejects it.
Forecast: One indicator, BarsSinceHighComponent (lookback 20, max_bars 20). It is 20 on the bar of a new 20-day closing high, falls by 1 each bar after it, and is 0 once the high is more than 20 bars old. It does not care whether later closes fall back below the high. The value is standardised against its own past 60 values. The forecast is long and largest right after a new high, shrinks smoothly as the high ages, and is zero when there has been no new high for 20 bars. It is never negative.
Config: N4-01_breakout-drift-lasts_1d_volt_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The coin's 10-bar forward close-to-close return after each new-high bar, minus the coin's mean 10-bar return over all its bars in all windows together. A new-high bar is one where the recorded indicator equals 20. Events are pooled across coins and are non-overlapping: a new high within 10 bars of a counted event is skipped.
- Supporting check: The same excess 10-bar return, restricted to events whose next bar closes below the new high. It must also be positive for the second claim to hold.
- Confirm: The mean excess 10-bar return is above 0 with t >= 2, using non-overlapping events only.
- Reject: The mean excess 10-bar return is below 0 with t <= -2. That means new highs are followed by reversal relative to holding.
- Inconclusive: Any t between -2 and 2, or fewer than 100 non-overlapping events pooled across all coins and windows.
