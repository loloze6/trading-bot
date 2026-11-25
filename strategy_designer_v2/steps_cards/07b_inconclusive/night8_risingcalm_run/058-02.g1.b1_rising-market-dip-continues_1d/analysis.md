---
line: 7.b inconclusive
backtest: 058-02.g1.b1_rising-market-dip-continues_1d
idea tested: 058-02.g1.b1_rising-market-dip-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3318 USD
---
## Findings
- **F1:** The test's own result is on the side the idea predicts but well short of the bar: on all four folds the slope of excess 5-day return on |forecast| is -0.00048 with t -0.80 over 917 grid cases. Its size is an unusual move of -0.39 % per case (t -0.74, 678 days), a strength of -0.039, and a total move of -0.99 % per case, which is 5.1 times the 0.19 % cost of a trade.
- **F2:** In folds B and C the effect is stronger when depth is measured as the idea words it (the raw dip in 30-day usual moves) than with the 60-bar standardised forecast the test regressed on. The raw-depth slope t is -1.95 against -1.39 for |forecast|, over 528 five-day cases. Mean excess return also falls from +0.03 % in the shallowest raw-depth quintile to -2.81 % in the deepest.
- **F3:** The fall shows in calm markets, not in agitated ones. In calm markets the 5-day slope t is -1.78 (288 cases) against -0.07 in agitated ones (240 cases). At 10 days the calm slope t is -1.75 with mean excess -2.36 % (132 cases), against +0.87 and +0.66 % in agitated markets (135 cases).
- **F4:** The effect turns with the horizon. Over 1 and 3 days the slope is positive, a small bounce in the direction of the brief's recovery (t +1.20 and +1.79; in calm markets at 3 days t +2.26, 496 cases). It turns negative only from 5 days on (t -1.39 at 5 days, -0.99 at 10 days).
- **F5:** The effect is mixed across coins and windows, which drowns it in the pooled test. At 5 days the slope is negative for ETH, LTC, XMR and ZEC (t -1.13 to -1.51, 83 to 108 cases each) but positive for XRP (t +1.50) and BTC (t +0.74). One window, w16, carries a t of -4.44 (46 cases), while w12 has a t of +1.69.
- **F6:** More data is available than the test used. The six core coins in four folds are only part of it: ADA, DOGE, LINK, TRX, UNI and AAVE have daily bars in folds A and D and part of B and C, AVAX, SOL and INJ in folds A and D, and NEAR, SUI, TAO and ONDO in fold D. With that many more cases, a slope on the predicted side but this small (F1) could be told apart from zero.

## Ideas
- `058-02.g1.b1.b1_rising-dip-continues-more-coins` (from F1, F5, F6): In a rising market, the further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
