---
line: 7.d confirmed, not profitable
backtest: 067-02.b1.b1.d1_choppy-deepest-month-falls-continue_1d
idea tested: 067-02.b1.b1.d1_choppy-deepest-month-falls-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5668 USD
---
## Findings
- **F1:** The book's gain is diluted by the shallow falls and by the coins' own rise, so it never covers what it risks. It is in a position on 16 % of coin-days and earns 0.016 % per position day, against the 0.05 % required. Its 458 trades are all short and average -2.21 % before fees (-2.31 % after). Short bars with a forecast between -2 and 0 lose 0.143 in summed gain, while bars from -10 to -2 make +0.448 and bars at -10 or below make +0.231. The normal drift works against the short by -1.15 % per case, which cuts the total move to +0.50 % although the unusual move is +1.65 %.
- **F2:** The effect sits in the deepest plain 30-day falls and is graded by raw depth (choppy grid, 7 days, drift-adjusted short return):
- **F3:** Over a longer horizon the deep falls carry more and the shallow ones lose more:
- **F4:** The effect is not one window's. Leaving out any one window, the largest third's 7-day unusual move stays between +3.4 % and +6.5 %, and its 21-day move between +5.9 % and +11.8 %. The book still fails with one window left out because it loses in w8, w10, w11 and w13 (Sharpe -2.5, -2.0, -4.3, -2.0), windows where holding rose (Sharpe +1.6, +3.2, +6.1, -0.4) and only 1 to 3 large cases fell.
- **F5:** In a choppy agitated market (30-day swing above its past-year median), the deep-fall cases are much stronger: 7-day unusual move +13.8 % (total +11.8 %), against +3.3 % in a calm one. Over 21 days they reach +15.0 % (t 2.16), against +8.6 %. The sample is small: 11 cases on 5 days, 7-day t 1.59. Agitation alone without the signal earns nothing: +0.09 % over 7 days and a total of -1.1 % over 21 days, on 14 cases. So agitation is not an effect of its own. It fits the brief's theory that a sharp month's move in a flat two-month window marks a fresh turn whose repositioning crowd has not finished selling.

## Ideas
- `067-02.b1.b1.d1.d1_deepest-choppy-falls-three-weeks` (from F1, F2, F3, F4): In a choppy market, the further a coin's close sits below its close of 30 days earlier, measured as a plain percent of that earlier close, the more it falls over the next 21 days, with the decline growing faster than the depth so that the deepest month's falls carry nearly all of it and shallow falls carry almost none.
- `067-02.b1.b1.d1.d2_agitated-choppy-deep-falls` (from F5, F2, F3): In a choppy, agitated market, the further a coin's close sits below its close of 30 days earlier, measured as a plain percent of that earlier close, the more it falls over the next 21 days, with the decline growing faster than the depth so that the deepest month's falls carry nearly all of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
