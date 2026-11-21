---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 3 days, the more it rises over the next 3 days.
Consequence: Read the depth of the multi-day sell-off, not just whether one happened, as the strength of a rebound trade held for days.
Why:
- F6: The depth of the 3-day fall also sorts what follows: within the regime, the deepest 3-day-fall quartile (below -7.6 %) is followed by a 72-hour excess of +0.0041, and the shallowest (0 to -1.65 %) by -0.0098; the lowest 1-day-return quintile (below -2.8 %) earns +0.0035 in the regime and +0.0122 even outside it (n 217).
- F3: Holding the position set at each non-overlapping 72-hour grid bar for the full 72 hours would have earned a mean allocation × 72-hour return of +0.0034 per case (t 3.48, n 1891 independent cases), so the rebound is real at the 3-day scale but is lost to hourly re-sizing.
