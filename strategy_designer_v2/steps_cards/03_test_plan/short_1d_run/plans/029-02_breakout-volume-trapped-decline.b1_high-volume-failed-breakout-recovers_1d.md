---
idea: 029-02_breakout-volume-trapped-decline.b1_high-volume-failed-breakout-recovers
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a daily close above the prior 20-day high, then a close back below it within 3 days, while the 60-day return is positive -> adapted: the failure is read "while" it holds (FailedBreakoutVolumeRatioComponent, fail_window 4), and the 60-day rise is a regime rule.
- Comparison: the breakout day's volume against its 20-day average volume -> kept: the volume ratio of the breakout bar sizes the forecast.
- Outcome: the coin rises over the next 10 days -> replaced: the brief's header allows short positions only, so the long this idea calls for cannot be held.
- Verdict transfer: no: a short-only book cannot take the idea's long, so neither a gain nor a loss on it would confirm or reject a rise.
Reason: The brief's header limits the test to short positions, but the idea predicts a rise and calls for a long sized by breakout volume. Under that side limit the forecast can never be positive, so the idea's outcome cannot be traded or measured as stated.
