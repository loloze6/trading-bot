---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its last 24 hours, the more it rises over the next 3 days.
Consequence: A trader buying after a deep one-day fall and holding for days captures a move several times a round trip, which the evening 2-hour trade cannot.
Why:
- F1: The test's slope is on the side the idea predicts but falls short of the bar (slope +0.00031, t 1.92, 5,683 grid cases). Half of those cases (2,873) have a forecast of 0 after a 24-hour rise. On the 2,810 cases with a positive forecast alone, the slope is +0.00069 with t 2.90.
- F6: The effect is mixed across years and drowned in some of them:
