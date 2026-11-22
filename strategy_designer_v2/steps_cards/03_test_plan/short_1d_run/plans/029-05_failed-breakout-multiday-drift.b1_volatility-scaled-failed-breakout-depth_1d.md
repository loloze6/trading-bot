---
idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a close back below the old 20-day high within 3 days of a close above it -> kept: `FailedBreakoutDepthComponent` (period 20, fail_window 3, source close) finds exactly this event.
- Comparison: how deep the re-entry close sits below the old high, in units of the coin's 20-day daily volatility -> replaced: no component divides that depth by the 20-day volatility of daily returns.
- Outcome: the decline continues, a larger fall from day 2 to day 10 after the failure -> kept: a lag of 2 bars and an 8-bar hold short.
- Verdict transfer: no: without the volatility scaling, the test would rank failures by percent depth, not by depth against the usual daily move the idea names.
Reason: The idea's grading needs the failed-breakout depth below the old 20-day high divided by the coin's 20-day standard deviation of daily returns. Every input is in the coin's own closes, but no component computes this ratio, and the weighted mean cannot divide one component by another. The closest substitutes measure something else: `vol_normalize` uses the 24-bar price standard deviation times the close, and `VolatilityScaledDistanceFromHighComponent` measures the distance from the breakout bar's own high, not from the old high.
