---
idea: 029-03_close-below-breakout-bar-low
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a failed breakout above the prior 20-day high, with a daily close below the breakout day's low -> kept: `FailedBreakoutDepthComponent` (`period` 20, `source` "high", `reference` "breakout_low", `fail_window` 3) is above 0 only on such a close.
- Comparison: how far that close sits below the breakout day's low -> kept: the component's value is that depth, in percent of the breakout day's low.
- Outcome: the coin falls over the next 5 days, more after a deeper close -> kept: the book holds a short sized by the depth for 5 bars.
- Verdict transfer: yes: the forecast is short exactly on the idea's closes and sized by their depth, so the 5-day returns that follow are the idea's own outcome.
Forecast: The component looks for the most recent close above the highest high of the prior 20 days within the last 3 days. "Within a few days" in the brief is taken as 3, the component's default. If the current close is below that breakout day's low, the component gives the depth of the close under that low, in percent of the low. It is 0 on every other bar. The depth is standardised against its own past 60 values, then negated. The forecast is 0 when there is no such close. It is negative (short) when there is one, and larger in size the deeper the close sits below the breakout day's low, capped at -20. It is never positive, because the brief is short only.
Config: 029-03_close-below-breakout-bar-low_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are bars on a non-overlapping 5-bar grid in each window (positions 0, 5, 10, ...) where the forecast is below 0. For each case, take the coin's 5-bar return from that close, minus the coin's mean 5-bar return over all its windows on the same grid. Report the mean of this excess return over the cases, with its t.
- Supporting check: Among the cases, the Spearman rank correlation between |forecast| and the excess 5-bar return must be below 0. A deeper close should be followed by a larger fall.
- Confirm: The mean excess 5-bar return is negative with t <= -2 over at least 30 cases, and the rank correlation is below 0.
- Reject: The mean excess 5-bar return is positive with t >= +2 over at least 30 cases.
- Inconclusive: Any t between -2 and +2 is inconclusive. So is t <= -2 with a rank correlation at or above 0, and so is any result on fewer than 30 cases, all coins and windows pooled.
