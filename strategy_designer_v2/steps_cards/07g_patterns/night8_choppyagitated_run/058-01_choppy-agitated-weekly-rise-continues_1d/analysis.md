---
line: 7.g patterns
backtest: 058-01_choppy-agitated-weekly-rise-continues_1d
idea tested: 058-01_choppy-agitated-weekly-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5333 USD
---
## Findings
- **F1:** Inside the choppy agitated profile, the brief's weekly continuation is absent on folds B and C. On the 7-day grid the 64 in-profile cases (39 days) have a mean excess 7-day return of -1.43 % (t -0.51). The 12 cases after a rise (9 days) average -4.77 % (t -2.69), which is reversal and not continuation, though on very few cases. Step 5's own measure over all folds agrees: -0.12 % (t -0.12, 93 cases on 64 days).
- **F2:** The profile is too rare on daily bars to grade anything. Only 4.8 % of coin-days are in it, which leaves 30 in-profile grid cases with a non-zero scaled move. Their Spearman between the scaled 7-day move and the excess next-7-day return is 0.13 at 7 days and 0.22 at 3 days (77 cases). No coin or window carries a reliable sign: by coin the t runs from -2.65 (ETH) to 0.08 (XMR), and by window the means run from +7.0 % (w12) to -14.4 % (w16).
- **F3:** The mirror on falls points toward continuation but cannot be told from chance. The 18 in-profile cases after a 7-day fall (12 days) average -10.7 % excess over the next 7 days (t -1.87) and -3.5 % over the next 3 days (44 cases, t -1.29). The Spearman on falls is only 0.11 (18 cases), and 0.11 again in all choppy-trend markets (44 cases).
- **F4:** Outside the profile, weekly continuation is weak and not significant. The two top quintiles of the scaled 7-day move are followed by +2.28 % (t 1.29) and +2.55 % (t 1.19) excess over 7 days, the bottom quintile by -0.29 % (t -0.14), and the Spearman over 795 cases is 0.035. In any choppy-trend market, the top quartile of the scaled 7-day move gives +8.5 % over 7 days (t 2.47), but on only 22 cases and 12 days, out of more than 20 angles looked at.
- **F5:** The bars do hold rebounds after down days, but they are ideas the map already holds:
- **F6:** Friday and Saturday returns are the largest of the week: +0.50 % (t 3.42) and +0.57 % (t 4.07), against -0.32 % on Thursday (t -1.77). These t are not clustered by day, so six coins moving together inflate them. The effect repeats 045-01's late-week gain, already held.

## Ideas
- No ideas: The theme's effect is not in the data. In-profile weekly continuation after a rise is null or negative (F1), the profile is too rare on daily bars to grade (F2), and the fall-side mirror stays under t 2 (F3). The only patterns that stand out are the down-day rebounds and the late-week gain (F5, F6), which the profile map already holds. This rests on the angles looked at: the forecast by quintile, in and out of profile, by sign, coin, window and trend; 1-, 3- and 7-day horizons; the day's range and close location; and the weekday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
