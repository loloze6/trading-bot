---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin's volatility over the last 7 days exceeds its volatility over the last 90 days, the higher its return over the next 14 days.
Consequence: A trader leans long a coin whose recent volatility has expanded well beyond its 90-day norm, and refuses longs in coins whose volatility has gone quiet.
Why:
- F1: Across every 84-bar grid point of every coin (about 1,500 cases), the ratio of the coin's 7-day (42-bar) volatility to its 90-day (540-bar) volatility predicts its excess return over the next 14 days. The Spearman rho with strength is 0.139 (p = 7e-8). The top volatility-ratio quintile averages +0.166 of a usual 14-day move (t 3.19, n 300) and the fourth quintile +0.131 (t 2.18), against −0.048, −0.092 and −0.058 for the three lowest. The rho is positive in 18 of the 19 coins (share 0.947).
- F3: The effect is not steady by year. The top volatility-ratio quintile scores +0.50 in 2023 and +0.43 in 2024, but −0.15 in 2021, −0.38 in 2025 and −0.35 in 2018.
