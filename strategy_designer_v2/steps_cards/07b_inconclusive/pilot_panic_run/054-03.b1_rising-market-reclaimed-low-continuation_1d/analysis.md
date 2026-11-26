---
line: 7.b inconclusive
backtest: 054-03.b1_rising-market-reclaimed-low-continuation_1d
idea tested: 054-03.b1_rising-market-reclaimed-low-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3557 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar. Over all folds the signed short unusual 10-day move is +2.63 % per case (t 1.11, 52 cases on 43 days, depth slope +0.0031). On folds B and C alone the recorded cases give +5.26 % (t 1.71, 34 cases on 26 days, 62 % of cases positive, median +5.7 %), so the effect is positive but too sparse to show clearly.
- **F2:** The move per case is small against the coin's own swing. The 10-day usual move is 17.6 % against a mean unusual move of 2.6 to 5.3 % (strength 0.158 on all folds, 0.30 on B and C). With about 50 cases spread over 6 coins, the market's own moves drown it.
- **F3:** The effect is mixed across windows and coins. Window w16 gives +18.8 % (t 3.30, 6 cases) while w17 gives −7.4 % (t −2.99, 4 cases). ZEC gives +17.5 % (t 2.27, 4 cases), ETH +9.3 % and LTC +7.9 %, while XRP gives −6.4 % (t −2.25, 5 cases). No coin has more than 8 cases, so no sub-group can carry a verdict.
- **F4:** The sign holds across horizons. Rebuilt reclaimed-pierce days in a rising market show a short-side unusual move of +14.4 % over 5 days (t 2.12, 13 cases), +14.5 % over 10 days (t 3.42, 11 cases) and +18.2 % over 20 days (t 2.42, 9 cases). The test's horizon is not misplaced; the case count is what limits it.
- **F5:** The grading by depth is not clear. Among the recorded cases the correlation of the unusual move with |forecast| is +0.18 but with raw pierce depth −0.26. The rebuilt depth slope is −0.0030 at 10 days, and the shallow, mid and deep terciles give +12.6 %, +23.6 % and +9.5 % on 3 to 4 cases each. A narrower version would only cut the cases further.
- **F6:** The test used only the 6 default coins. Thirteen more coins have daily bars in folds A and D, and six of them also in part of B and C (ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO). That data could multiply the cases the result lacks (F1, F2).

## Ideas
- `054-03.b1.b1_reclaimed-low-uptrend-continuation` (from F1, F2, F4, F6): In a rising market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it falls over the next 10 days, and the fall is larger the deeper the day's low went below the 30-day low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
