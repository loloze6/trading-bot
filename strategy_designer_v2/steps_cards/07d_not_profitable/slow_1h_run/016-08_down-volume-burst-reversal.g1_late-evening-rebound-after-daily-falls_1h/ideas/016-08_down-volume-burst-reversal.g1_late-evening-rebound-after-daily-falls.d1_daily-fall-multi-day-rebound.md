---
brief: 016_grind-versus-jump-moves
source-idea: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls
line: 7.d not profitable
backtest: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the late-UTC-evening hours, the more a coin has fallen over its past 24 hours as of the 20:00 UTC close, the more it rises over the next 3 days.
Consequence: A trader would buy a coin that is down on the day at the 20:00 UTC close and hold it for days, paying one round trip for a rebound several times larger than the one-hour move that the fees now swallow.
Why:
- F1: Fees eat the book: summed over all held bars, the position's gain before costs is +1.32, while the fees sum to -8.36. Every coin's fees are 3 to 24 times its gross gain (for example LTC +0.063 against -1.50, BTC +0.318 against -1.37). This puts the mean daily return at -0.00041 and the Sharpe at -2.24.
- F2: The book holds for one hour only. Of 7,279 held bars, 7,225 sit on the 19:00-start bar; the median trade lasts 60 minutes; there are 7,238 trades. The average trade makes -0.095 % before fees, and its commission is 0.525. So each day pays a full round trip for a one-hour move.
- F3: The one-hour edge is too small for that cost. On 20:00-close decision bars, the deepest third of 24-hour falls beats the coin's mean by only +0.00050 over the next 1h. The fee costs about 0.00125 per unit of position traded, roughly 2.5 times that edge.
- F4: The rebound grows over days, measured on the deepest third of 24-hour falls (n ≈ 8,400 to 8,600 cases):
- F6: Over all 20:00-close bars, the reversal runs in both directions. The lowest fifth of 24h returns (mean -0.060) gains +0.0040 over 24h. The middle fifths gain about 0, at -0.0002 to -0.0002. So the information lies on the fall side and in the slow, multi-day part.
