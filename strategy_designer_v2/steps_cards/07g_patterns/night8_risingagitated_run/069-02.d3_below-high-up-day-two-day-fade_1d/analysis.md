---
line: 7.g patterns
backtest: 069-02.d3_below-high-up-day-two-day-fade_1d
idea tested: 069-02.d3_below-high-up-day-two-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6348 USD
---
## Findings
- **F1:** On up days, the next-day excess move falls steadily as the close sits lower in the 20-day high-low range: from -0.91 % (t -2.25, 738 cases on 303 days) in the lowest fifth, to -0.54 % (t -2.05) in the second, -0.17 % and -0.12 % in the middle fifths, and +0.25 % (t 0.75) in the top fifth; the deepest fifth's move is about 4.8 times the 0.19 % cost of a trade.
- **F2:** That grading of up days by range position is positive in every subset checked, though no single subset is sure on its own: all 6 coins (slopes 0.14 to 0.43 of a usual daily move, BTC t 2.44, the others t 1.0 to 1.7), all 4 years (0.06 to 0.24), and both halves of the folds shown (w7-w12 lowest fifth -0.58 % against top +0.15 %; w13-w18 -1.23 % against +0.33 %); on a 10-day range the slope is 0.26 with t 2.32 over 3690 up days.
- **F3:** The effect fades over the tested 2-day horizon: on the 2-day grid the lowest fifth of up days moves -1.08 % with t only -1.26 (368 cases, 165 days), against -0.91 % with t -2.25 over one day, so the second day adds noise rather than move, which fits the tested idea's t of 1.49.
- **F4:** Only the strongest forecasts carry the tested idea: up days with a forecast from -20 to -15 are followed by -1.27 % over 2 days (t -2.52, 339 cases) and those from -15 to -10 by -0.69 % (t -2.09, 464), while the weaker ones from -10 to 0 are followed by +0.17 % and +0.15 % (t 0.65 and 0.51, 1338 cases); the book still sits in a position on 80 % of the coins' days.
- **F5:** The book's loss is the coin's own rise: its daily returns correlate -0.62 with the coins', and it loses in the rising windows (w11: coins +1.26 % a day, book -0.24 %; w10: +0.40 %, book -0.14 %) while it gains in the falling ones (w14: coins -0.43 %, book +0.24 %; w7: -0.47 %, book +0.14 %).
- **F6:** Deep up-day closes fall over 2 days in falling markets (-1.02 %, t -2.11, 280 cases) and in choppy ones (-1.88 %, t -1.81, 48), but not in rising ones (-0.08 %, t -0.09, 61); inside falling markets, though, the 1-day slope on range position is not sure (agitated 0.29, t 0.66; calm -0.09, t -0.41), so the trend does not clearly hold the grading.
- **F7:** In choppy agitated markets, the empty short cell of the profile map, the next-day excess move falls the higher the coin closes within its own day's range: slope -0.82 of a usual daily move (t -2.68, 167 days), and the top third of closes is followed by -1.78 % (t -2.29, 56 cases on 44 days); the slope is negative in both halves of the folds (w13-w18 -1.12, t -2.56; w7-w12 -0.26, t -1.08), but the sample is small.
- **F8:** Patterns that are already held or did not stand out: the largest scaled one-day falls rebound the next day (+0.78 %, t 4.32), which the falling-agitated rebound family already holds; Thursday and Friday next-day gains (+0.47 %, t 3.19; +0.39 %, t 2.87) are already held as the late-week gain; down days high in the 20-day range rise the next day (top fifth +0.69 %, t 2.36), as the held nearness-to-high books do, and that grading is not sure by coin or by year; high closes fade in falling agitated markets (slope -0.52, t -2.46), which is the held 060-01.g1.d2.d1.

## Ideas
- `069-02.d3.g1_low-in-range-up-day-next-day-fade` (from F1, F2, F3, F4, F5): When a coin closes up on the day, the lower that close sits within its 20-day high-low range, the larger its fall over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `069-02.d3.g2_choppy-agitated-high-close-fade` (from F7, F8): In a choppy, agitated market, the higher a coin closes within its own day's high-low range, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
