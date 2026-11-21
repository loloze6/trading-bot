---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
line: 7.b inconclusive
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the more slowly the cloud has fallen over the past 26 days.
Consequence: A coin drifting below a gently falling cloud is a reason to short it, while a coin below a cloud that has collapsed fast is a reason to refuse the short.
Why:
- F1: Across all 156 grid cases the short earns +1.51 % per case over 26 days beyond the coin's drift, with t 0.69, and 59 % of cases are positive. The result is on the side the idea predicts but far short of t 2. The total move is -2.72 %, because the coins' normal drift over 26 days (+1.4 % to +7.4 %) works against a short.
- F2: The idea's graded part is clear, and it points where the idea says. The slow-fall half earns +7.32 % beyond drift (t 3.06, 78 cases, strength 0.29), the fast-fall half -4.30 % (t -1.20, 78 cases). Their difference is +11.6 % with Welch t 2.70, and regressing the excess on log slowness gives slope 0.075 (t 2.91, 156 cases). By slowness quartile, from fastest to slowest fall, the excess runs -7.5 %, -1.1 %, +6.8 % (t 1.95) and +7.8 % (t 2.36).
- F3: The forecast's own size orders the outcome the same way. The most-short quartile earns +8.3 % (t 1.71) and the least-short quartile -7.2 % (t -1.36), 39 cases each. The main measure averages strong slow-fall cases with fast-fall cases that go against the short, and that mix is what keeps its t low.
- F5: Inside the slow-fall half the sign holds on all 6 coins: BTC +5.8 %, ETH +9.4 %, LTC +13.2 % (t 3.17), XMR +3.4 %, XRP +1.4 %, ZEC +11.5 %. Each coin has only 9 to 23 cases, so it is too few cases, not a few coins, that leaves the result unclear.
