---
line: 7.b inconclusive
backtest: 058-01.g2.b1.d3.b2_large-one-day-rises-fade_1d
idea tested: 058-01.g2.b1.d3.b2_large-one-day-rises-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.6832 USD
---
## Findings
- **F1:** In folds B and C (114 cases on a 5-day grid, 62 days), the give-back after a standout up day does not grow with the rise; it shrinks. The smallest rises (1.0 to 1.19 of the 30-day swing) give back 4.50 % of unusual move (t 2.27, 26 cases). The three larger quartiles give −1.49 %, −0.33 % and +0.36 % (t −0.87, −0.14, +0.15). The Spearman correlation of the scaled rise with the 5-day unusual move is −0.105. The brief's own grading is therefore contradicted, not just too weak to show.
- **F2:** The forecast's size tells the same story. Cases with |forecast| from 10.7 to 16.0 give 3.76 % (t 2.40, 38 cases). The capped cases from 16.0 to 20 give 0.33 % (t 0.22, 76 cases), so the strongest bets carry nothing.
- **F3:** The tested idea is about one up day, but where it does show, the up day breaks a fall rather than extending a multi-day rally. Cases whose two prior days fell give 1.69 % (t 1.46, 77 cases) against 1.01 % (t 0.43, 37) when they rose. The top tercile of the 3-day scaled rise (0.91 to 3.51) gives −1.45 % (t −0.63), against +1.64 % and +2.39 % for the lower terciles. The brief's situation, a several-day rise, is where the effect is absent.
- **F4:** The effect appears only at the plan's 5-day horizon. The mean unusual move is +0.23 % at 1 day, −0.47 % at 2 days, +0.28 % at 3 days, +1.47 % at 5 days and +0.69 % at 10 days (t 0.32, −0.63, 0.23, 1.23, 0.43). A gradual give-back over days would build steadily, and this one does not.
- **F5:** The result is drowned by the market's own swings and by a few extreme cases.

## Ideas
- No ideas: The idea is on the predicted side only weakly. Where the give-back shows (the smallest standout rises, rises that break a fall, the 5-day horizon only), it runs against the brief's grading and its multi-day-rise situation (F1–F4). No amended idea on the theme is clear enough to test, so the theme's effect is not in the data.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
