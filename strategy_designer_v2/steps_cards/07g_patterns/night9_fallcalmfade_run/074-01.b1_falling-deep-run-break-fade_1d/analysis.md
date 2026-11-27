---
line: 7.g patterns
backtest: 074-01.b1_falling-deep-run-break-fade_1d
idea tested: 074-01.b1_falling-deep-run-break-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3876 USD
---
## Findings
- **F1:** In a falling market, among the first up days after a run of down closes, the deepest third of run depths (the run's loss over the 30-day daily swing) is followed by a drift-adjusted next-day return of -2.58 % (t -4.43, 185 cases on 80 days), while the shallow and middle thirds are followed by only -0.57 % (t -1.07) and -0.28 % (t -0.44), so the fade sits almost entirely in the deepest runs and grows faster than in proportion to depth.
- **F2:** The fade is specific to up days that end a down run: in falling markets, up days after a down day are followed by -1.14 % (t -2.86, 556 cases, 191 days), up days after an up day by +0.16 % (t 0.36, 417 cases), and run-ending up days in rising markets by +0.36 % (t 0.98, 447 cases).
- **F3:** The size of the up day does not grade the fade: in falling markets, the three terciles of the bounce's size in 30-day swings are followed by -1.19 %, -1.00 % and -1.23 % (t -2.06, -1.82, -2.20), and the slope of the next day on the bounce's size is -0.50 % per swing with t -0.94.
- **F4:** The fade holds in calm and agitated falling markets alike, -1.20 % (t -2.72, 204 cases, 109 days) when calm and -1.11 % (t -2.06, 352 cases, 126 days) when agitated, and calm falling is a profile where the map holds only 2 short strategies.
- **F5:** Run length grades the fade only roughly in falling markets: runs of 1, 2, 3 and 4 or more down days give -0.93 % (t -1.72), -1.52 % (t -2.24), -0.32 % (t -0.38) and -2.44 % (t -2.95), which is weaker than the depth grading in F1.
- **F6:** The book's gain is concentrated: its 10 best days carry 93 % of its summed daily return and its 10 worst days give back 48 %, with w14 (+0.21 % a day) and w7 (+0.16 %) holding most of it, which fits a book that earns from a few deep-run cases (F1) and explains its Calmar of 0.46.
- **F7:** Other angles show nothing new that stands out after this many looks: the rebound after large down days in agitated markets (slope -2.12 % per swing, t -2.60, falling agitated) repeats long rebound ideas the map already holds, and the falling-market Saturday effect (+0.84 %, t 2.14) and the choppy-market fade after small up days (-0.73 %, t -2.08) are within chance.

## Ideas
- `074-01.b1.g1_convex-deep-run-fade` (from F1, F2, F3, F6): In a falling market, the first up day after a run of down days is followed by a fall in the coin's close over the next day, and the fall grows faster than the run's depth (the run's return over its down days against the coin's usual daily swing over the last 30 days): slides that are deep for the coin are faded far more than in proportion to slides that are moderately deep.
- `074-01.b1.g2_calm-downtrend-relief-fade` (from F4, F1, F2): In a falling, calm market, the first up day after a run of down days is followed by a fall in the coin's close over the next day, and the deeper the run's fall against the coin's usual daily swing over the last 30 days, the larger that next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
