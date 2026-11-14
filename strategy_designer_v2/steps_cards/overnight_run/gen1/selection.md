# Generation 1: selection

**Pool.** 124 ideas from step 7 on the full-data backtests of brief 002: lines 7.b, 7.d and 7.g, exercises 1 and 2 (002-01, 002-03) and the generation 1 analyses (002-02, 002-04), both modes.

**Themes, by how often they recur:**

| Theme | Recurs | Chosen as |
|---|---|---|
| T1 above the long average **and** up over the last 20 days, it keeps rising | about 12 | N1-01 |
| T4 a fresh cross falls back; once above for weeks, the drift appears | 8 | N1-03 |
| T5 after an unusually large daily drop, the next day rises | 8 | N1-04 |
| T6 Friday's close to Saturday's close rises more than an average day | 6 | N1-05 (expected missing-components: no component reads the weekday; kept to test that path) |
| T7 far below the long average, it rebounds over the next days | 6 | N1-06 |
| T3 above a **rising** long average, it keeps rising | 5 | N1-02 |
| T10 a strong last 20 days leads to a strong next 20 | 5 | N1-08 |
| T8 just after a death cross, it rebounds | 4 | N1-07 |
| T11 below a **falling** long average, it keeps falling | 4 | N1-09 |
| high volatility within a trend helps / hurts | contradictory | not chosen |

One representative per theme, a one-call idea where one exists. Hand-off: `handoff/` (lineage: `handoff/LINEAGE.md`). All are tested on the default data (6 coins, folds A to D, daily), where they were found: a pass is checked again on unseen coins.
