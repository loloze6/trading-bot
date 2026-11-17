---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell on Sunday (its Saturday-close to Sunday-close return, measured against its own recent daily volatility) rises over the next 2 days, and the larger the Sunday fall, the larger the rise.
Consequence: The Sunday-close fade should also buy Sunday falls, not only short Sunday rises, which roughly doubles the cases the tested strategy acts on.
Why:
- F3: A Sunday bar's own one-day move is undone over Monday and Tuesday on both sides. By Sunday z-quintile, the Monday-Tuesday excess return is +1.00% (t 3.96) and +0.90% (t 3.67) in the two falling quintiles. It is -0.43%, -0.90% (t -3.42) and -0.57% (t -2.21) in the three rising quintiles, about 956 cases each. The tested plan only shorted the rising half.
- F4: The two-day Saturday-plus-Sunday return does not predict Monday-Tuesday (pooled slope -0.0002, t -0.18, n=4717). The reversal is a one-day-back, one-day-ahead effect, not a whole-weekend effect.
- F6: The book barely earns from the effect it holds. It is in the market only on Monday, where its mean daily return is +0.00022 (t 0.80, n=5270). Sunday's rebalancing costs -0.00021 a day (t -19.4), so fees take almost all of the Monday gain.
