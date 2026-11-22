---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a fall over the next 5 days. The fall is largest where the 90-day fall is moderate, and it shrinks as the 90-day fall deepens into a crash.
Consequence: A trader would fade bounces in moderately falling coins, and refuse to fade them in coins that have already crashed, where bounces are followed by further rises.
Why:
- F3: The fade grows with the 90-day fall only up to a point, then turns. In the deepest 90-day-fall quintile (−80 % to −43 %) the cases lost −1.17 % over 5 days (t −2.02) and −2.85 % over 10 days. The middle quintile (−28 % to −19 %) gave +0.57 % in total and +1.33 % unusual (t 2.93).
- F1: The fade is real against the coin's drift but not in price: over the 2419 short cases the coin's 5-day move in the short direction is −0.19 % in total (t −0.84) and +0.55 % unusual (t 2.50). The book pays the total move, and that sits below zero before the 0.22 % cost of a trade, so the book loses (Sharpe −0.32, mean daily return −0.0002).
