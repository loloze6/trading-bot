---
line: 7.b inconclusive
backtest: 067-02.b1.b1.d2_agitated-choppy-month-fall-continues_1d
idea tested: 067-02.b1.b1.d2_agitated-choppy-month-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3498 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts, but too small for this data to show it: the |forecast|-weighted short-side 7-day excess return is +1.02 % with t 0.74, over 108 independent days (215 cases). The size check agrees, at +1.22 % per case (0.076 of a usual 12.84 % move) with t 1.66 over 265 days. The test already used all 19 coins and all four folds on daily bars, so there is no more data to add.
- **F2:** In the folds shown here (B and C), only 27 grid cases on 20 days fall inside the choppy agitated profile after a monthly fall. Their mean short-side excess is +6.3 % (t 1.71). Without window w16 it drops to +5.2 % (t 1.35, 25 cases on 18 days). w16 alone gives +32.9 % on 5 cases, so much of the visible effect is one episode.
- **F3:** No subset carries the effect clearly, because every split leaves too few cases. By depth of the fall, the deepest quarter gives +17.4 % (7 cases), and the other quarters give +4.6 % to +8.2 % (7 to 8 cases each). By where the close sits in its 30-day range, closes near the low give only +2.9 % (t 0.67, 18 cases), against +12.1 % in mid-range (t 1.82, 7 cases). A last week still falling gives +4.7 % (t 1.58), against +8.0 % after a bounce (t 1.29). By year, the effect ranges from -0.5 % (2018, 3 cases) to +8.3 % (2021, 11 cases).
- **F4:** Changing the horizon does not sharpen it. The short-side excess is +6.4 % (t 2.46) over 3 days, +9.4 % (t 4.17) over 7, +8.1 % (t 3.22) over 14 and +11.6 % (t 3.98) over 21. These come from the same 25 to 30 overlapping-profile cases, without the per-day t. No horizon stands out against the plan's 7 days.
- **F5:** The book fights the coin's own rise. The normal drift in the short direction is -0.94 % per 7 days, so the total move per case is only +0.28 %, about 1.2 times the 0.22 % cost of a trade. The book's Sharpe is 0.03 against holding's 0.55, and it was in a position on 9 % of coin-days.

## Ideas
- No ideas: The effect points the predicted way but is small (t 0.74 on the main measure, t 1.66 on the size). The test already used every coin and fold available on daily bars. No coin, period, depth, position in range or horizon shows it clearly apart from one window's episode (F1–F4), so no further test on this data would give a clearer answer.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
