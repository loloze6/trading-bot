---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin whose 3-day return is a deep fall against its usual 3-day moves, the return over the next 24 hours is positive, and the deeper that fall, the larger the rebound.
Consequence: After a deep 3-day fall, a trader should expect a one-day bounce at any hour and should refuse to open new shorts there.
Why:
- F1: The book loses because fees are about five times what the positions earn: its mean gross gain is 0.000016 per bar against a fee of 0.000077 per bar (net about -0.00006 per bar in every coin, from -0.000054 in XRP to -0.000072 in LTC), so its mean daily return is about -0.0015 (-0.00132 to -0.00174 by coin) while holding the coins gains +0.0007 to +0.0016 a day.
- F4: Over the next 24 hours the rebound after a 3-day fall is several times larger and graded by depth. Across all hours the excess 24-hour return by fall quintile goes from -0.0029 (t -2.37, n 1702) for the shallowest falls to +0.0037 (t 3.11) and +0.0027 (t 1.96) for the deepest two, and for falls deeper than 1.5 standard deviations it is +0.0033 (t 3.06, n 2634) against t 1.31 at 2 hours.
- F5: Starting from off-settlement closes, the 24-hour excess return after falls of 1.5 to 2 standard deviations is +0.0072 (n 405) and after deeper falls +0.0031 (n 352), while shallow falls give -0.0012 to -0.0033. The rebound at 48 hours is gone (top-quintile t 0.65, weighted t 0.16), so it plays out within about a day.
