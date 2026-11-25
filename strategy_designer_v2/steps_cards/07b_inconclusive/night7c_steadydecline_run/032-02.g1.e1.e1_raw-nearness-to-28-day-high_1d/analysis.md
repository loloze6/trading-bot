---
line: 7.b inconclusive
backtest: 032-02.g1.e1.e1_raw-nearness-to-28-day-high_1d
idea tested: 032-02.g1.e1.e1_raw-nearness-to-28-day-high
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.2074 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: the slope of the 5-day excess return on the forecast is +0.00078 with a day-clustered t of 1.57 over 3,419 grid cases on 617 days. The top third minus the bottom third is +1.20 %. The unusual move is +0.47 % per case, 0.039 of a usual move, with a t of 1.29 over 960 days.
- **F2:** On folds B and C alone the same slope is clearer: +0.00193 with t 2.37 over 1,710 cases at 5 days, and +0.00301 with t 1.92 over 846 cases at 10 days. So the pooled t of 1.57 means folds A and D are weaker, and the effect points the same way but is too small for the four folds to show clearly.
- **F3:** Over 5 days the effect rises steadily across the forecast's fifths, from −1.56 % in the lowest fifth (mean distance 52.7 % below the high) to +2.46 % in the highest (2.6 % below). Over 10 days it runs from −3.06 % to +4.14 %. This is the graded shape the idea predicts.
- **F4:** Closes within about 1 % of the 28-day high are followed by +2.99 % excess over 5 days (t 3.67, 256 cases) and +4.97 % over 10 days (t 2.72, 126 cases). This is the largest rise, as the idea says.
- **F5:** The effect is mixed across coins and windows, which inflates the noise. XRP alone has a t of 3.42, while the other five coins have slopes of the same sign with t between 0.41 and 1.43. Three of the 12 windows have negative slopes, and the year slopes run from t 0.20 in 2018 to t 1.74 in 2021.
- **F6:** The effect holds whatever the coin's 28-day return, as the idea claims. At 5 days the slope is +0.00228 (t 2.35, 623 cases) when the 28-day return is up and +0.00229 (t 1.41, 655 cases) when it is down. The weaker t in down markets comes from noise, not from a smaller slope.
- **F7:** The raw percent distance itself shows no linear slope (t −0.25 at 5 days, t −0.90 at 10 days). Its fifths are not monotone: the fourth fifth, 27.7 % below the high, gives −3.17 % (t −4.88), and the farthest fifth, 66.7 % below, gives +0.15 %. The graded effect shows in the forecast, which is standardised over its past 60 days, rather than in raw distance.

## Ideas
- `032-02.g1.e1.e1.b1_nearness-to-high-more-coins` (from F1, F2, F3, F5, F6): The closer a coin's close is to its highest close of the last 28 days, the larger its rise over the next 5 to 10 days, whether its 28-day return is up or down, with a close at the 28-day high itself followed by the largest rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
