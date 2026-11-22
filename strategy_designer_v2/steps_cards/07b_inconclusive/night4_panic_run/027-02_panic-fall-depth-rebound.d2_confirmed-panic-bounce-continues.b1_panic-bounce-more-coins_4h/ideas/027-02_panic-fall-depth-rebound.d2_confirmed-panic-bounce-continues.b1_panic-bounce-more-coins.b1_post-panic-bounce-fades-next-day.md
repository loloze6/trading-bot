---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
line: 7.b inconclusive
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the lower its return over the following 24 hours.
Consequence: A trader should not chase the first sharp rebound after a panic, because the larger that rebound, the more of it is given back the next day.
Why:
- F5: Bounce size predicts the next 24 hours, in the opposite direction to the idea. The slope of the raw 24-hour return after the case bar on the bounce is -0.000634 with t -4.17 on 507 cases, about -3.1 % across the spread from the bottom bounce quintile (-17.8) to the top one (+31.1). The relation is gone by 3 days (t -0.06) and 7 days (t -0.10).
- F1: The tested slope's positive t comes from a few extreme cases. On the same 463 cases the rank correlation of bounce with 84-bar excess return is 0.001 (p 0.98), the slope after winsorising the excess return at 2 %/98 % has t 0.32, and removing the 10 highest-leverage cases (4 of them ZEC) turns it negative (slope -0.000666, t -1.81, 453 cases).
