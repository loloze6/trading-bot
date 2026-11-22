---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the larger that rise in units of the usual daily move, the larger the fall.
Consequence: Sharp bounces in a long-falling coin are given back over the following days as underwater holders and returning short sellers sell into them.
Why:
- F1: The test's result is on the side the idea predicts but short of the bar: the 1324 short cases show a mean short-direction unusual 5-day move of +0.48 % (t 1.81), 0.048 of the coin's usual 5-day move (10.60 %), which is the size real ideas usually have; my own recount (1361 cases) gives +0.54 % with t 2.01, so the result sits right at the threshold.
- F2: The effect is mixed across periods and coins. The 5-day unusual move is strongly positive in 2018 (+2.37 %, t 2.83, 255 cases), 2019 (+1.48 %, t 2.47) and 2025 (+1.58 %, t 2.53). It is negative in 2020 (-2.18 %, t -2.33) and 2021 (-2.08 %, t -1.80). Five of six coins are positive (ETH +1.20 %, ZEC +1.10 %, LTC +0.92 %, BTC +0.89 %, XMR +0.29 %). XRP is negative (-1.20 %, t -1.43). With six coins, this spread is what keeps the t below 2.
