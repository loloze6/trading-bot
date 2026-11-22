---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour fall that is large against the coin's usual 24-hour move, while its bar range over those 24 hours is above its 30-day average, the coin earns more than its usual drift over the next 14 days, only while its 24-hour range stays above its 30-day average. The wider that range against its average, the larger that excess.
Consequence: A trader would keep a panic-rebound position only as long as the range expansion lasts, and leave it once the market turns calm, where the book lost against the coin.
Why:
- F1: The book is a near-permanent long and its falls are the coins' falls. It holds a position on 85 % to 97 % of bars in every prior-30-day-return quintile, with mean allocation 0.74 to 1.09, and the median trade lasts 30.7 days. Its window sums track holding: w2 −0.51 against −0.46, w14 −0.65 against −0.52, w7 −0.34 against −0.58. The chained book's deepest fall is −74.2 % against a yearly return of 27.2 %, hence Calmar 0.37.
- F5: The book loses in calm stretches it holds through. With the 24-hour range ratio in its lowest quintile (0.16 to 0.62), the book makes −0.204 % a day against the coin's +0.058 %. In the highest quintile (above 1.23), it makes +0.287 % against the coin's +0.245 %.
