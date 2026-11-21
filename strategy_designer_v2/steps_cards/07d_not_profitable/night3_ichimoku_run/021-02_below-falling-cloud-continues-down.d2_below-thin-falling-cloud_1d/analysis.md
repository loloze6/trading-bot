---
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
idea tested: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3795 USD
---
## Findings
- **F1:** The book loses before any cost because the total move per case runs against the short: the coin's normal drift is +4.15 % over 26 days, the unusual move only +2.79 %, so the total is -1.36 % per case (241 cases), against a cost of 0.19 %. On the bars where the book is short the coin still rose +0.069 % a day (+0.119 % on all bars), and the short bars earned -0.040 % a day, giving a book Sharpe of -0.31 and a mean daily return of -0.0002.
- **F2:** Thinness grades the move as the idea says, and the losses sit in the thick-cloud cases. In the thickest third of the forecast (mean |forecast| 2.4, 52 cases) the total move is -8.7 % (unusual -4.3 %). In the middle third it is -0.5 % (unusual +3.8 %). In the thinnest third (|forecast| 14.6) it is +1.0 % (unusual +5.0 %), with a Spearman between |forecast| and the excess return of p 0.008 over 156 cases.
- **F3:** The worst cases are a thick cloud after a 7-day fall: the coin then rose about 20 % over 26 days (total -19.9 %, unusual -15.9 %, 28 cases). Under a thick cloud after a 7-day rise the short earned +6.1 % total (31 cases). Under a thin cloud the short earned +5.7 % after a 7-day fall (31 cases) and +0.8 % after a 7-day rise (28 cases).
- **F4:** The fall from the 26-day high also grades the result: in the third deepest below that high (mean -36 %) the short's total is -5.7 % per case, in the shallowest third (mean -10 %) it is +1.9 %.
- **F5:** The book's deepest falls come from staying short through the coins' rallies: in w21 the book lost 23 % (deepest fall 25 %) while the coins rose 87 %. In w8, w16, w17 and w6 it lost 13 to 21 % while the coins rose 29 to 48 %.
- **F6:** Long-lasting regimes lose. In the third of cases where the coin had been below the falling cloud for the longest (mean 34 days) the short's total is -7.3 %, against +2.0 % in the middle third (mean 10 days).
- **F7:** The loss is uneven across coins: per case XRP's total is -10.7 % (23 cases) and XMR's -6.0 % (20 cases), while LTC's is +4.2 % (25 cases).

## Ideas
- `021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud.d1_thin-cloud-shallow-fall-short` (from F1, F2, F4, F5): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the thinner the cloud is relative to the price, only while the coin's close is near its 26-day high rather than far below it.
- `021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud.d2_thick-cloud-washout-rebound` (from F1, F2, F3): When a coin closes below a thick falling Ichimoku cloud after falling over the past 7 days, its return over the next 26 days is positive, and larger the thicker the cloud is relative to the price and the deeper its 7-day fall.
- `021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud.d3_fresh-break-below-thin-cloud` (from F1, F2, F5, F6): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the thinner the cloud is relative to the price, only while the coin first closed below the cloud within the past few weeks rather than over a month ago.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
