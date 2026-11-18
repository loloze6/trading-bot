---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.b inconclusive
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply on a volume burst, the longer the lower wick below the close, as a share of the bar's high-to-low range, the larger the price rise over the next 3 days.
Consequence: The lower wick shows buyers already absorbing the forced flow, which marks the cascade's exhaustion and the start of recovery.
Why:
- F1: The test's own measure sits on the predicted side but is close to nothing: on 223 independent flush bars the 3-day slope of excess return on the close's location in the range is +0.024 with t 0.74. The flush bars' mean 3-day excess return is +0.0003 (t 0.05), and the wick terciles run low −0.011, mid +0.008, high +0.004, which is not graded.
- F6: Coin by coin, no group carries the tested effect. Every coin's 3-day slope t lies between −0.15 and 1.45 (n 28 to 48), and the slope is not stronger among the deepest falls (t −0.25), the middle ones (t 0.78) or the shallowest (t −0.70).
