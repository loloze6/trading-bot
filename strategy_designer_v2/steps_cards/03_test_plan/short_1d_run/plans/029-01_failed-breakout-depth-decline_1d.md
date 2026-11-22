---
idea: 029-01_failed-breakout-depth-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 1063cd22d7e7
---
Fidelity:
- Situation: a daily close above the prior 20-day high, then within 3 days a close back below that old high -> replaced: the catalogue has no measure of the close against the high from before the breakout, only against highs that include the breakout bar.
- Comparison: the deeper the close sits below the old high, the larger the fall -> replaced: no component grades that depth (the old high ends 1 to 3 bars before t).
- Outcome: the coin falls over the next 5 days (5 bars on 1d), short only -> kept: the book holds the short for 5 bars, measured against holding the coin.
- Verdict transfer: no: depth below the breakout close is not depth below the old high, so neither a confirm nor a reject would carry over to the idea.
Reason: The data is in each coin's own daily bars, and the config's logic could hold the idea. A regime would gate on a recent breakout: `BarsSinceHighComponent` with lookback 20 and max_bars 4, set between 1 and 3. A graded short would then size by the depth below the old high. But no component measures the close against the 20-day high that stood before the breakout bar. `DistanceFromHighComponent`, `BreakoutInMeanRangesComponent` "below" and `VolatilityScaledDistanceFromHighComponent` all include the breakout bar in their high and have no lag. Per-day regimes or weighted mixes do not shift their window either.
