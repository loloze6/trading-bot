---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: While a coin's 14-day return is positive, the more its volatility over the last 7 days exceeds its volatility over the last 90 days, the higher its return over the next 14 days.
Consequence: A trader buys a rising coin whose volatility is expanding and refuses a rising coin whose volatility is contracting, where the next two weeks tend to lag.
Why:
- F2: The volatility-ratio effect sits in coins whose prior 14-day return is positive. There, the top quintile averages +0.232 of a usual move (t 3.11, n 168) and the bottom quintile −0.172 (t −2.15, n 155), a clean progression of −0.17, −0.06, −0.08, +0.18, +0.23. After a negative 14-day return the quintiles are flat and mixed (+0.086, −0.126, −0.042, +0.093, +0.081, no |t| above 1.9).
- F1: Across every 84-bar grid point of every coin (about 1,500 cases), the ratio of the coin's 7-day (42-bar) volatility to its 90-day (540-bar) volatility predicts its excess return over the next 14 days. The Spearman rho with strength is 0.139 (p = 7e-8). The top volatility-ratio quintile averages +0.166 of a usual 14-day move (t 3.19, n 300) and the fourth quintile +0.131 (t 2.18), against −0.048, −0.092 and −0.058 for the three lowest. The rho is positive in 18 of the 19 coins (share 0.947).
- F4: The panic premium the backtest captures comes from up-moving wide-range stretches, not falls. When a coin's 24-hour range is at least 7.5 mean bar ranges and it rose over those 24 hours, the next 84 bars beat the drift by +7.58 % (strength 0.263, t 3.37, 369 cases). The same stretches with a fall gain only +1.40 % (strength 0.063, t 1.33, 284 cases).
