---
line: 7.g patterns
backtest: 058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5474 USD
---
## Findings
- **F1:** In the falling agitated profile, the next-day unusual move runs against the day's return scaled by its 30-day swing, on both sides. The OLS slope is -0.0121 per swing (t -4.38, about 1,300 bars). Outside the profile it is only -0.00136 (t -1.45, about 7,000 bars), so the one-day reversal belongs to this profile.
- **F2:** On up days in the profile, the next-day fade is limited to rises within about one swing. Rises of 0 to 0.5 swing are followed by -0.95 % (t -3.31, n 354) and rises of 0.5 to 1 swing by -1.17 % (t -2.13, n 163). Larger rises show no consistent fade: +0.48 % (t 0.74, n 64) at 1 to 1.5, -1.29 % (t -1.48, n 37) at 1.5 to 2, and +0.21 % (t 0.13, n 21) above 2. This is the tested cap, and no stronger short case is left above it.
- **F3:** Down days in the profile rebound the next day, graded by size. Falls larger than 2 swings gain +6.20 % (t 3.69, n 29), falls of 1 to 2 swings +2.17 % (t 3.22, n 112), and falls of 0.5 to 1 swing +1.11 % (t 3.35, n 209). This is the long side the map already holds 12 times in falling agitated.
- **F4:** In the profile, a close far below the day's high is followed by a large rebound. The top quintile (more than 1.06 swings below the high) gains +2.92 % the next day (t 6.08, n 260), while every other quintile is negative (-0.22 % to -0.74 %). This is already held through the "wide range, low close rebound" family (039-02, 044-01, 045-01).
- **F5:** Where the day closed in its range adds nothing to the scaled day return in the profile. In a regression of the next-day move on both, the close location's coefficient has t -0.47 against t -4.38 for the scaled day return. Up days closing high fall -0.81 % (t -2.88, n 392), in line with F2.
- **F6:** The brief's own situation, a 3-day rise, shows only a thin gradient in the profile over the next 3 days (non-overlapping). A rise of 0 to 1 swing is followed by -0.48 % (t -0.65, n 141), 1 to 2 swings by -1.62 % (t -1.38, n 33), and more than 2 swings by -8.54 % (t -2.28, n 6). Outside the profile, 3-day moves continue weakly: +1.18 % (t 1.97) after a 1 to 2 swing rise, +2.57 % (t 1.98) above 2, and -1.45 % (t -2.15) after a 1 to 2 swing fall. None of these stands out given the angles examined.
- **F7:** The short cases point the same way in every year and every coin of folds B and C:

## Ideas
- No ideas: The strong patterns are already tested or already held: the capped up-day fade in F1 and F2 is this backtest's idea, and the falling agitated rebounds in F3 and F4 repeat the 12 long strategies the map holds there. The remaining candidates are weak given the angles examined: the brief's multi-day give-back (F6: n 6 to 33, |t| ≤ 2.3) and the 3-day continuation outside the profile (|t| ≈ 2). The other angles also showed nothing that stands out: weekday, close location, distance from the day's low, and year.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
