---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that rise that came from its few biggest hourly gains, the smaller the coin's further rise over the next 3 days.
Consequence: A trader would scale down long exposure after rises carried by a few violent hours, rather than short them, because those rises still drift up only less.
Why:
- F1: The tested difference is on the side the idea predicts but small next to the noise of 72-hour returns: the grind group's mean 72-hour forward return minus the jump group's is +0.0047 (Welch t 0.83, 487 vs 490 grid cases), while each quintile's 72-hour returns have a standard deviation of 0.076 to 0.104, so detecting a gap of this size at t 2 would need about six times as many cases.
- F2: The effect is mixed across coins, so no subset shows it clearly. The difference is positive on four coins (BTC +0.0045, t 0.43; LTC +0.0159, t 1.24; XRP +0.0315, t 1.44; ZEC +0.0173, t 1.04) and negative on two (ETH −0.0159, t −1.41; XMR −0.0178, t −1.63). By year, five years are positive and three negative, and no year reaches |t| 2; 2025 comes closest (+0.0280, t 1.77, 68 vs 60 cases).
- F4: Part of the measure is the move's size, but controlling for size does not change the result. grind_residual has a Spearman correlation of 0.44 with the past 72-hour rise, and quintile mean past rises go from 0.077 to 0.168. With the past rise in the regression, grind_residual's coefficient is 0.0149 (t 0.82, n 967) and the past rise adds nothing (t 0.12). Within past-size terciles the difference is −0.0015 (t −0.19), +0.0112 (t 1.16) and −0.0016 (t −0.13).
- F5: Another horizon does not reveal a clearer effect, because it is largest at short horizons and gone by 6 to 10 days. The difference is +0.0037 over 24 hours (t 1.08) and +0.0047 over 72 hours (t 0.83), then +0.0007 over 144 hours (t 0.09) and −0.0018 over 240 hours (t −0.14).
