---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week
line: 7.e profitable but not proven
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's 30-day return is positive, it rises more than its normal drift over the next three days, and the larger that 30-day return, the larger the rise.
Consequence: A trader holds the coin long while its 30-day return is positive, leans harder the stronger it is, and stands aside when it turns negative.
Why:
- F1: The book earns 0.119 % a day, and 0.0668 % of that (56 %) is the market's own rise, leaving 0.0522 % of timing; on the 9873 coin-days it is in, it holds about 1.00 of the book and earns 0.200 % a day against the coin's 0.167 %, and on the 7508 days it is out it earns 0.013 %.
- F2: The book is long on 83 % to 89 % of the bars where the 30-day return is positive (regime "trending"), depending on the coin, and on only 25 % to 33 % of the other bars, so in practice it is a long position held while the coin's 30-day return is positive.
- F3: On non-overlapping 3-day stretches, the coin's unusual move is +0.35 % (t 2.08, 2839 cases) when the 30-day return is positive and −0.35 % (t −2.37, 2885 cases) when it is not; on 7-day stretches it is +0.49 % (t 1.15) against −0.48 % (t −1.39).
- F4: By quintile of the 30-day return, the 3-day unusual move rises from −0.45 % in the second quintile to +0.20 % in the fourth and +0.62 % in the top one (mean 30-day return +51 %, t 1.70, 857 cases); the 7-day move goes from −1.10 % to +1.09 %; the rank correlation over all cases is weak (Spearman 0.010, p 0.51).
- F6: The profit sits in long holds: the longest quarter of trades (mean 38.6 days) carries 6931 of the 8396 summed net percentage points (83 %), and the top 10 trades carry 3395 (40 %); the median trade is +0.21 % and 52 % of trades win.
- F7: The gain is spread across coins and does not come from one of them: each coin's daily book mean is positive, from 0.080 % (LTC, t 1.28) to 0.164 % (ETH, t 2.66); XMR's uptrend 3-day move is negative (−0.22 %, t −0.70); the losing years 2018 (−0.15 % a day) and 2022 (−0.02 %) lost less than the coins did (−0.35 %, −0.19 %).
