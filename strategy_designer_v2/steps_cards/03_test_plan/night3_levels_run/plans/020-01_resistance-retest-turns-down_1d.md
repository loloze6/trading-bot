---
idea: 020-01_resistance-retest-turns-down
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: price rises back to a price where it turned down several times in the past 90 days -> replaced: no component finds past turn-down prices or measures the close's nearness to them.
- Comparison: the more times it turned down there before, the larger the fall -> replaced: no component counts past turn-downs at one price level.
- Outcome: price falls over the next 5 days -> kept: a short position held 5 bars on daily bars.
- Verdict transfer: no: the nearest components measure other things, so neither a confirm nor a reject would carry over to the idea. Distance from the 90-day high sees only one level and no turns. The stall count counts bars that sit near the high, not reversals.
Reason: The idea needs two things from the coin's own highs and closes over 90 days: the prices where it turned down, and how many turns cluster near today's close. The config's logic could hold such a graded measure, but no catalogue component computes it. The combinations tried do not: `DistanceFromHighComponent`, `StallUnderHighCountComponent`, `DonchianBreakoutComponent`, and these with the proximity forms.
