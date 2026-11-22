---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline
line: 7.g patterns
backtest: 029-04_breakout-extension-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 20-day closing high, it rises more than its normal drift over the next 5 days, and the further its close and its highest high since the break stand above that old high, the larger the rise.
Consequence: A trader should refuse shorts into fresh 20-day highs, even after a brief slip back below them, and treat a strong push above the high as a reason to be long rather than short.
Why:
- F1: Measured on non-overlapping grids, bars that close above the prior 20-day closing high are followed by a rise above the coin's normal drift at every horizon tested: +1.06 % over 3 days (t 2.61, 528 cases), +1.62 % over 5 days (t 2.18, 306 cases) and +4.22 % over 10 days (t 2.42, 167 cases). The other bars give -0.08 %, -0.14 % and -0.44 % (t -0.63, -0.69, -1.10).
- F2: The step-5 rejection runs against the brief. Among failed breakouts, a larger peak excursion above the old high goes with a higher 5-day return, not a lower one: slope +0.042 of a usual move per point of excursion, t 2.80, 294 cases. By tercile of excursion the unusual 5-day move rises from -0.37 % to +0.13 % to +1.12 % (98 cases each). The slope fades at 10 days (t 1.08, 151 cases).
- F3: Failed-breakout bars as a whole show no downward follow-through. Their unusual 5-day move is +0.73 % (t 1.20, 398 cases) against -0.10 % on the other bars (t -0.48, 3021 cases).
- F4: The breakout rise is graded only weakly and is unstable.
