---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 28-day return, the larger its return over the next 5 days in the same direction, only while that 28-day return is a rise.
Consequence: A strong 4-week rise is a reason to stay long for the next week, while a 4-week fall gives no reason to go short, which removes the short side's 53 % fall from the book.
Why:
- F1: The failing Calmar comes from the short side. Before costs, the long positions alone earn 8.95 bps a day, with a yearly return of 33 %, a deepest fall of 24 % and a Calmar of 1.37. The short positions alone lose 0.36 bps a day, with a yearly return of -4 %, a deepest fall of 53 % and a Calmar of -0.08. Together, before costs, the book has a Calmar of 0.56 and a deepest fall of 50 %.
- F2: The book's deepest fall is 54.5 %. It lasts 1009 days, from w2 to w10. During it the short positions lost on all 6 coins: summed gains of -0.90 on LTC, -0.77 on XRP, -0.53 on BTC, -0.44 on ZEC, -0.42 on XMR and -0.13 on ETH. The long positions on BTC and ETH gained (+0.71, +0.13).
- F3: Bar by bar, long positions earn 17.9 bps a bar (t 5.17, 8705 bars). Short positions earn -0.68 bps a bar (t -0.26, 8622 bars), so they add risk with no gain.
- F4: On non-overlapping 5-day cases, continuation holds only after rises. On 28-day rises the slope of the demeaned 5-day return on the 28-day return is +0.025 (t 2.86, 1309 cases). On 28-day falls it has the wrong sign, -0.030 (t -1.36, 1246 cases). The sixth of cases with the deepest falls (mean 28-day return -25 %) is followed by a demeaned 5-day return of -0.00 %, while the sixth with the largest rises (+46 %) is followed by +1.08 % (t 1.85).
