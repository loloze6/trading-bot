---
line: 7.b inconclusive
backtest: 069-02.d1.d1_agitated-fall-up-day-fade_1d
idea tested: 069-02.d1.d1_agitated-fall-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3619 USD
---
## Findings
- **F1:** Inside the falling agitated profile the up days are followed by a clear next-day fall, but the fall does not grow with the depth. Over 622 cases on 263 days in folds B and C, the mean short gain over the coin's drift is +0.91 % (t 3.95). The slope of that gain on raw depth is −0.0006 (day-clustered t −0.25, 542 cases on 225 days). The depth quartiles give +1.06 %, +1.15 %, +0.92 % and +0.51 % (deepest, t 0.77), so the deepest closes fade least. Step 5's slope t is −0.41, a level effect with no grading.
- **F2:** The grading the idea predicts does show across all up days, with no profile. The short gain's slope on raw depth is +0.0017 (day-clustered t 2.08, 3,527 cases on 889 days) and +0.0020 outside the profile (t 2.49, 2,985 cases). By depth quintile, from highest close to deepest, the gain is −0.26 %, +0.10 %, +0.34 %, +0.08 % and +1.09 % (t 5.03). The grading is carried mainly by the deepest fifth.
- **F3:** The deepest-quintile fade lives in falling and choppy markets, not rising ones. Its mean is +1.21 % in a falling 60-day trend (t 4.07, 352 cases), +1.75 % when choppy (t 2.00, 58 cases) and +0.18 % when rising (t 0.42, 89 cases). The linear slope inside the falling trend alone is weak: +0.0013, t 0.90, 902 cases.
- **F4:** The profile's filter misses many of the deep closes. Only 19.7 % of the deepest-quintile up days fall inside the falling agitated profile (8–23 % across quintiles). The test therefore graded a narrow, already-deep slice where depth no longer separates the cases. Standardising depth over its own past 60 values (correlation −0.91 with raw depth) did not change this.
- **F5:** The effect holds at one day and is mixed across coins and years. Inside the profile the gain is +0.91 % at 1 day, +0.45 % at 2 days (t 1.34) and +0.41 % at 3 days (t 1.12). The deepest-quintile fade is positive on five coins with t 2.2–2.8, but XRP is +0.26 % (t 0.42). By year it runs from +1.76 % in 2018 (t 4.96) to +0.04 % in 2021 (t 0.06).
- **F6:** Inside the profile the biggest up days do not fade. The largest quartile of up-moves in units of swing gives −0.18 % (t −0.30), against +1.93 % for the third quartile (t 4.84). The up-day size slope is −0.0069 (t −1.63), which blurs the depth grading.

## Ideas
- `069-02.d1.d1.b1_deep-below-high-up-day-fade` (from F2, F4, F5): When a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next day.
- `069-02.d1.d1.b2_falling-trend-deep-up-day-fade` (from F3, F4, F1): In a falling market, when a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
