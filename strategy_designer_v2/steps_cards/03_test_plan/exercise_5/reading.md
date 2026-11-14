# Exercise 5: reading

Opus, the same seven ideas, one call per idea. The prompt is exercise 4's, plus the warm-up line in the data block and one line on settings: "when the brief gives none, use the single most common convention for that indicator on that bar size". Cost: 1.80 USD (0.22 to 0.28 per idea). No config was run by the engine.

## Against the card's criteria

| Criterion | Result |
|---|---|
| Untestable where it should be | 2 of 2: 004-01 (another coin), 005-01 (no component can recall RSI at an earlier high) |
| A `Forecast:` line matching the config | 5 of 5 |
| `standardise` first; every strategy component graded | 5 of 5 |
| A regime only when the idea is a condition | 5 of 5 (003-01 only, a rule on the low-volume up bar) |
| No constant inside a regime; no "fading" | 5 of 5 |
| Same side as the idea | 5 of 5 |
| Settings from convention, stable | 5 of 5: RSI 14 twice; SMA 50/200 for both moving-average ideas (exercise 4: 10/30, then 20/50) |
| One horizon; one main measure plus one supporting check | 5 of 5 |
| The evidence as a number; overlapping returns counted once | 5 of 5 (t ≥ 2 or t ≤ -2 in all; samples taken 5, 20 or 1 bars apart) |
| Criteria sized to the data | 5 of 5: minimum counts of 30, 8, 60 and 50 events. 002-01 counts its own samples ("about 36 across the 6 windows"); 002-05 notes some windows may hold no up-cross stretch |
| Deviation stated | 5 of 5 |

No fault found.

## Small points, not faults

- **The two RSI ideas use different `signed_power` pivots** (10 and 20). Both are allowed and both are declared. The settings line covers indicators, not transforms.
- **002-01 and 002-05 are the same config again.** Their horizons (20 bars and 1 bar) and their measures differ, so they are two tests of one forecast. That is step 2's open point.
- **The criteria are demanding for the data.** 002-01 has about 36 independent samples in all, and needs 8 of them with a positive forecast. An "inconclusive" verdict is likely there, and the plan says so. This is honest, not a fault. If such ideas should be decidable, the data (fold or bar size) is the lever, and that is your call.

## Status

This is the first exercise with no fault. "Done when" asks for two in a row. The next exercise should run unchanged, to check stability.
