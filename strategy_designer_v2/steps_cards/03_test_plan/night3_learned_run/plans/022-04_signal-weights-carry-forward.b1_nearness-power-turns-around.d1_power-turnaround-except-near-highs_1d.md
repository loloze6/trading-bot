---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d1_power-turnaround-except-near-highs
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the nearness-to-90-day-high signal's power over the past 365 days is high, unless the close is near the high after a large 20-day return -> kept: the "single"/"high" term w x z and HighProximityMomentumComponent (period 90, return_period 20) compute both.
- Comparison: power over the following 90 days against power over the past 365 days -> replaced: a forecast can only bet on the coin's direction, not compare two correlation windows.
- Outcome: the signal's 5-day predictive power falls over the next 90 days, while pressed-high strong coins keep rising -> replaced: a bet against the signal gains only when its power turns negative, not when it merely falls.
- Verdict transfer: no: a power that falls but stays positive would refute a counter-bet without refuting the idea, and a mixed book's gain cannot be split between the main claim and its exception.
Reason: The idea's outcome is that a correlation (the signal's power over the coming 90 days) is lower than its past value, not a directional move of the price. The config can express a position on the price only, and a bet against the signal gains only if its power changes sign. Measuring "lower power" also needs a comparison of two correlation windows, which the guide says the config cannot express (only a forecast per bar).
