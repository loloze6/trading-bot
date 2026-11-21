---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 28-day return, the larger its return over the next 5 days in the same direction, with a 28-day fall carrying on more the calmer the coin's daily swings over the past 20 days are against those of the past 60 days.
Consequence: A trader bets on a 4-week fall continuing only when it has been an orderly decline, and gives the bet less weight the more the recent swings have widened.
Why:
- F4: On non-overlapping 5-day cases, continuation holds only after rises. On 28-day rises the slope of the demeaned 5-day return on the 28-day return is +0.025 (t 2.86, 1309 cases). On 28-day falls it has the wrong sign, -0.030 (t -1.36, 1246 cases). The sixth of cases with the deepest falls (mean 28-day return -25 %) is followed by a demeaned 5-day return of -0.00 %, while the sixth with the largest rises (+46 %) is followed by +1.08 % (t 1.85).
- F5: After 28-day falls, whether the fall continues depends on how calm recent swings are. Where 20-day volatility is lowest against 60-day volatility, the next 5 days are -1.56 % against the coin's mean (t -2.66, 286 cases). In the middle third they are -0.84 % (t -1.41, 292 cases). In the highest third they are +0.42 % (t 0.55, 227 cases).
- F6: Bar by bar, short positions earn +11.8 bps a bar (t 2.46, 1519 bars) in the lowest third of 20-day to 60-day volatility. They earn -2.8 bps in the middle third and +0.4 bps in the highest third. In the highest third of 20-day volatility itself they earn -6.7 bps a bar (t -1.46).
- F2: The book's deepest fall is 54.5 %. It lasts 1009 days, from w2 to w10. During it the short positions lost on all 6 coins: summed gains of -0.90 on LTC, -0.77 on XRP, -0.53 on BTC, -0.44 on ZEC, -0.42 on XMR and -0.13 on ETH. The long positions on BTC and ETH gained (+0.71, +0.13).
