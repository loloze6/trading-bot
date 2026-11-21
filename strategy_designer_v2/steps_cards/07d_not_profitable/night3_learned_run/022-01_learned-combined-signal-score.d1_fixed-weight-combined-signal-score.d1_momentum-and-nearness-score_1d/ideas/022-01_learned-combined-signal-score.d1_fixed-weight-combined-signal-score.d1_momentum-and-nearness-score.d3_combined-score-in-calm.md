---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 28-day return and its closeness to its 90-day high are combined into one score, each weighted equally in its known direction, the coin's return over the next 5 days is higher the higher that score is, and the more so the lower the coin's 30-day volatility sits against its own history.
Consequence: Lean harder on a high score when the coin is calm, so that the gain per unit held rises where the move is largest.
Why:
- F2: The long side carries the whole gain and the short side causes the falls. The long bars summed +7.15 against −0.69 for the short bars, with fees of 0.30 and 0.25. On its own, the long side's daily chain earns 0.000408 a day, 14.9 % a year, with a deepest fall of 12.3 % (a Calmar of about 1.2). The short side's chain earns −0.000042 a day, −2.2 % a year, with a deepest fall of 31.1 %.
- F6: Long positions pay most while the coin's 30-day volatility is low against its own history. In the lowest volatility quartile a long bar earned 0.00139 a day, with a next-day coin return of +0.51 %. In the other three quartiles it earned 0.00034 to 0.00068.
- F7: Cost is not the cause. Per case, the total move of +0.89 % is 4.6 times the 0.19 % round trip, in line with the earlier finding (F11) that ideas larger than their cost can pay. What loses is the side the move goes against, the shorts.
