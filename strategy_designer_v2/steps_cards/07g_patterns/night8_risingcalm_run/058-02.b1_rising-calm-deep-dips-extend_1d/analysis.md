---
line: 7.g patterns
backtest: 058-02.b1_rising-calm-deep-dips-extend_1d
idea tested: 058-02.b1_rising-calm-deep-dips-extend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3826 USD
---
## Findings
- **F1:** In the rising calm bars of folds B and C, the raw scaled pullback (close against its 5-day closing high, divided by the 30-day daily swing, not standardised) predicts the 5-day excess return with a positive slope of 0.0347, t 3.29 with one day's cases taken together, over 258 cases on 98 days. So a deeper pullback is followed by a lower return and a close at the high by a higher one, which is the tested idea's direction. Step 5's slope on the standardised forecast over all folds was only t 0.61.
- **F2:** Inside rising calm, the effect runs across the whole range. The deepest fifth of pullbacks returns -5.04 % excess over 5 days (t -3.36, 31 cases). Bars at or near the 5-day high return +3.71 % (t 3.25, 121 cases). Closes exactly at the 5-day high return +3.36 % (t 2.06, 83 cases, 45 days).
- **F3:** The pullback slope is strongest in rising calm (0.0503, t 3.08, 171 cases). It is weaker in rising agitated (0.0271, t 1.48, 147 cases) and in falling agitated (0.0089, t 1.05, 227 cases). This is the brief's own contrast between calm and agitated, with the effect reversed: continuation, not recovery.
- **F4:** Five-day momentum (the 5-day return in usual moves, against the next 5-day excess return) is positive in the calm profiles: rising calm t 2.04, choppy calm t 3.03, falling calm t 1.99. It is flat in falling agitated (t -0.36) and rising agitated (t 0.41). This is close to the held calm "nearness to high" book (035-01.b1), so it is not a discovery.
- **F5:** After the lowest fifth of one-day moves in usual moves, the next day's excess return is +0.61 % (t 4.05, 1,253 bars). With a 2-day horizon by profile, no profile shows a slope beyond |t| 1.5. This is the agitated-fall next-day rebound the map already holds 12 times, so it is left out.
- **F6:** Weekday next-day excess returns are Wednesday -0.50 % (t -2.78), Thursday +0.41 % (t 2.80) and Friday +0.38 % (t 2.74). Among seven weekdays this does not stand out, and the late-week gain is already held (045-01), so it is left out.

## Ideas
- `058-02.b1.g1_rising-calm-high-distance-continuation` (from F1, F2, F3): In a rising, calm market, the nearer a coin's close sits to its highest close of the past 5 days, measured in its usual daily swing over the past 30 days, the larger its rise over the next 5 days. The further below that high it sits, the larger its fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
